// execution: 
//     gcc syscall_copy.c -o syscall_copy
//     ./syscall_copy

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>   // Contains open() flags like O_RDONLY, O_WRONLY, O_CREAT

#define BUFFER_SIZE 64

int main() {
    int src_fd, dest_fd;
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read, bytes_written;

    // 1. Open source file in Read-Only mode
    src_fd = open("input_sample.txt", O_RDONLY);
    if (src_fd == -1) {
        perror("Error opening source file");
        exit(EXIT_FAILURE);
    }

    /*
     * 2. Open/Create destination file
     * O_WRONLY: Write-only mode
     * O_CREAT: Create file if it doesn't exist
     * O_TRUNC: Clear existing content if file exists
     * 0644: Permissions mode (Owner: Read/Write, Group/Others: Read-only)
     */
    dest_fd = open("output_cloned.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (dest_fd == -1) {
        perror("Error creating destination file");
        close(src_fd); // Don't leave file handles leaking!
        exit(EXIT_FAILURE);
    }

    // 3. Core I/O Stream Loop
    // read() returns the number of bytes read, 0 at EOF, or -1 on error
    while ((bytes_read = read(src_fd, buffer, BUFFER_SIZE)) > 0) {
        bytes_written = write(dest_fd, buffer, bytes_read);
        if (bytes_written == -1) {
            perror("Error writing to destination file");
            break;
        }
    }

    if (bytes_read == -1) {
        perror("Critical error encountered during read phase");
    }

    // 4. Release kernel file descriptors
    close(src_fd);
    close(dest_fd);

    printf("File copy pipeline executed. Verify 'output_cloned.txt'.\n");
    return 0;
}

/*******************************************************************************
 * DEEP-DIVE ARCHITECTURAL EXPLANATION: LOW-LEVEL FILE I/O MECHANICS
 *******************************************************************************
 *
 * This program implements a foundational file-copy utility entirely through 
 * low-level Unix system calls (`open`, `read`, `write`, `close`). By avoiding 
 * standard high-level abstractions like `fopen()` or `fscanf()`, this code 
 * interfaces directly with the operating system kernel's virtual file system.
 *
 * =============================================================================
 * 1. FILE DESCRIPTORS VS. C FILE POINTERS
 * =============================================================================
 * In standard C, files are treated as managed streams via `FILE *` pointers. 
 * Those pointers contain user-space buffers that group small operations 
 * together to minimize system performance hits. 
 * 
 * At the system call level, the kernel doesn't understand `FILE *`. Instead, it 
 * tracks open files using unique integer indices called **File Descriptors (FD)**.
 *   - When `open()` runs successfully, the kernel updates its internal System 
 *     File Table, assigns the file to the next lowest available slot integer 
 *     in the process descriptor list, and hands that integer back to you.
 *   - Standard input/output/error occupy FDs 0, 1, and 2. Therefore, `src_fd` 
 *     and `dest_fd` in this program will typically evaluate to 3 and 4.
 *
 * =============================================================================
 * 2. DECODING BITWISE FLAGS AND BITMASKS
 * =============================================================================
 * The second argument of the `open()` system call takes a configuration flag 
 * composed of individual bit positions. We combine these properties using the 
 * bitwise OR operator (`|`). 
 *
 * Here is what happens when the kernel processes `O_WRONLY | O_CREAT | O_TRUNC`:
 * 
 *  +-----------+-------------------------------------------------------------+
 *  | Flag Component | Underlying Kernel Action                                |
 *  +-----------+-------------------------------------------------------------+
 *  | O_RDONLY  | Allocates read-only access channels to the file descriptor.  |
 *  | O_WRONLY  | Allocates write-only access channels to the file descriptor. |
 *  | O_CREAT   | Checks if the file path exists. If not, instructs the file  |
 *  |           | system engine to instantiate a fresh inode entry.           |
 *  | O_TRUNC   | If the file exists, clips its length metric back down to 0, |
 *  |           | wiping out old contents instantly.                         |
 *  +-----------+-------------------------------------------------------------+
 *
 * =============================================================================
 * 3. DEMYSTIFYING THE OCTAL PERMISSION MASK (0644)
 * =============================================================================
 * When using the `O_CREAT` flag, you must provide a third argument specifying 
 * access restrictions in octal notation (indicated by the leading `0`). 
 * The system maps these numbers to Owner, Group, and World permissions:
 * 
 *              0        6         4         4
 *           (Octal)  (Owner)   (Group)   (Others)
 * 
 * Breaking down the components by their binary values (Read=4, Write=2, Exec=1):
 *   - Owner Permission (6): 4 + 2 = Read + Write permissions.
 *   - Group Permission (4): 4 = Read-Only permission.
 *   - Others Permission (4): 4 = Read-Only permission.
 * 
 * Note: The final applied bitwise mode is modified slightly by the process's 
 * internal execution environment mask (`umask`).
 *
 * =============================================================================
 * 4. THE CORE I/O PIPELINE ENGINE (THE WHILE LOOP MECHANICS)
 * =============================================================================
 * The core stream engine relies on a localized array block (`char buffer[64]`) 
 * acting as an explicit processing conveyor belt.
 * 
 * The loop statement condition handles data stream transitions dynamically:
 *   - `read(src_fd, buffer, BUFFER_SIZE)`: The kernel grabs up to 64 bytes out of 
 *     the source file, moves the internal file position cursor forward, copies 
 *     the data into our buffer array, and returns the count of fetched bytes.
 *   - **The Loop Exit Condition**: As long as it finds bytes, it returns a 
 *     positive integer. When it hits the true End of File (EOF), `read()` 
 *     returns `0`, cleanly breaking the loop. If a disk error occurs, it 
 *     returns `-1`.
 * 
 * Crucial Data Preservation Constraint:
 * Notice that `write()` uses `bytes_read` as its volume limit parameter, *not* 
 * `BUFFER_SIZE`. If the source file contains exactly 65 bytes, the first loop 
 * processes 64 bytes. The second loop processes the single remaining byte. 
 * If we mistakenly instructed `write()` to output `BUFFER_SIZE` (64) bytes on 
 * that second pass, the program would append 63 trailing bytes of uninitialized 
 * garbage memory data onto the destination file!
 *
 * =============================================================================
 * 5. CONTEXT PRESERVATION AND DESCRIPTOR LEAKS
 * =============================================================================
 * Operating systems restrict the maximum number of active file handles a 
 * single process can keep open at once (often capped at 1024 handles by default). 
 * 
 * If a program loops repeatedly, opening files without running `close()`, it 
 * causes a **File Descriptor Leak**. Once the table slots fill up completely, 
 * all subsequent `open()` statements will fail, returning `-1`. 
 * 
 * Notice that if creating the destination file fails, we explicitly call 
 * `close(src_fd);` before exiting to free that system resource safely.
 *
 *******************************************************************************/