// execution: 
//     gcc syscall_loop.c -o syscall_loop
//     ./syscall_loop

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int main() {
    int fd = open("input_sample.txt", O_RDONLY);
    if (fd == -1) {
        perror("Failed to open asset file");
        return 1;
    }

    // Intentionally small buffer chunk to force loop cycles
    char chunk_buffer[10]; 
    ssize_t bytes_read;
    int loop_counter = 1;

    printf("--- Beginning Chunk Processing Stream ---\n");

    while ((bytes_read = read(fd, chunk_buffer, sizeof(chunk_buffer))) > 0) {
        printf("\n[Chunk #%d | Bytes Pulled: %ld]\n", loop_counter++, bytes_read);
        
        // Write the pulled chunk straight out to stdout
        write(1, "Data: \"", 7);
        write(1, chunk_buffer, bytes_read);
        write(1, "\"\n", 2);
    }

    if (bytes_read == 0) {
        printf("\n--- End of File (EOF) reached successfully. ---\n");
    } else if (bytes_read == -1) {
        perror("Stream failure error");
    }

    close(fd);
    return 0;
}

/*******************************************************************************
 * DEEP-DIVE ARCHITECTURAL EXPLANATION: CHUNKED I/O STREAMING & BUFFER MECHANICS
 *******************************************************************************
 *
 * This program demonstrates how operating systems slice up and stream large 
 * files using small, localized memory windows. By limiting our stack buffer to 
 * a tiny size (10 bytes), we force our program into a deterministic cyclical 
 * pattern that highlights the exact internal behaviors of low-level system calls.
 *
 * =============================================================================
 * 1. THE ARCHITECTURE OF CHUNKED STREAMING (THE MOVING CURSOR)
 * =============================================================================
 * When a process opens a file, the OS kernel sets up an internal tracking variable 
 * called the **File Offset** (or read/write cursor). This cursor initially points 
 * to byte 0 of the file.
 * 
 * Every time `read(fd, chunk_buffer, 10)` runs:
 *   1. The kernel copies *up to* 10 bytes starting from the current cursor position 
 *      and dumps them directly into `chunk_buffer`.
 *   2. The kernel automatically shifts the file offset forward by the exact number 
 *      of bytes successfully processed.
 *   3. The loop evaluates the return value (`bytes_read`) and cycles back. 
 * 
 * Because the kernel retains this offset across execution contexts, subsequent 
 * iterations automatically resume exactly where the previous chunk left off, 
 * eliminating any risk of duplicate processing or infinite loop traps.
 *
 * =============================================================================
 * 2. THE DANGER ZONE: STRINGS VS. RAW MEMORY BYTES
 * =============================================================================
 * One of the most critical structural details of this code is that `chunk_buffer` 
 * **does not contain a null terminator (`\0`)** inside the loop! 
 * 
 * High-level C string functions (like `printf("%s")`, `strlen()`, or `strcpy()`) 
 * are blindly designed to keep scanning memory until they crash into a `\0`. If 
 * you try to print our buffer using `printf("Data: %s", chunk_buffer);`, you will 
 * get data corruption. The program will print out your 10 bytes, followed by 
 * whatever random garbage memory happens to sit behind it on the stack frame.
 * 
 * Why does `write(1, chunk_buffer, bytes_read);` work perfectly without a `\0`?
 * Because `write()` is a raw system call that does not care about string patterns. 
 * It relies entirely on explicit math: it targets a starting address in memory 
 * (`chunk_buffer`) and counts forward by the exact number of indices given 
 * (`bytes_read`). It leaves no room for memory overflow boundaries.
 *
 * =============================================================================
 * 3. HANDLING THE TAIL END RESIDUE (THE LAST REMAINDER CHUNK)
 * =============================================================================
 * Files are rarely perfectly divisible by a fixed buffer size. Let's trace what 
 * happens if your `input_sample.txt` file contains exactly 23 bytes of data:
 * 
 *  +---------+------------+----------------------+----------------------------+
 *  | Loop #  | Bytes Read | File Offset (Cursor) | Internal Action            |
 *  +---------+------------+----------------------+----------------------------+
 *  | Cycle 1 | 10 Bytes   | 0 -> 10              | Full buffer transfer       |
 *  | Cycle 2 | 10 Bytes   | 10 -> 20             | Full buffer transfer       |
 *  | Cycle 3 | 3 Bytes    | 20 -> 23             | Pulls the final 3 bytes    |
 *  | Cycle 4 | 0 Bytes    | 23 (EOF Reached)     | Loop terminates cleanly    |
 *  +---------+------------+----------------------+----------------------------+
 * 
 * Look at **Cycle 3**: `read()` asks for 10 bytes, but the file runs dry after 
 * matching only 3. Instead of crashing, `read()` populates `bytes_read` with `3`.
 * 
 * Because our subsequent write command uses `bytes_read` rather than `sizeof(chunk_buffer)`, 
 * it correctly outputs only those 3 valid bytes. The remaining 7 slots in our 
 * buffer array contain lingering residual data from Cycle 2, which is safely 
 * ignored rather than duplicated.
 *
 * =============================================================================
 * 4. SYNCHRONIZATION AND FLUSHING: MIXING printf() AND write()
 * =============================================================================
 * This code mixes two distinct layers of output operations: `printf()` (buffered 
 * C library function) and `write()` (unbuffered kernel system call).
 * 
 *   - `write()` immediately shifts bytes across the user-kernel split to the screen.
 *   - `printf()` saves up characters inside a temporary user-space memory cache 
 *     called the Standard Output Buffer, flushing it to hardware only when it 
 *     encounters a newline (`\n`).
 * 
 * Notice that we explicitly end our tracking `printf()` string with `\n` right 
 * before calling `write()`. If we omitted the `\n` in the print statement, the 
 * system's output stream could become visually desynchronized—causing the raw 
 * `write()` data to print onto the screen *before* the diagnostic text that was 
 * technically invoked before it!
 *
 *******************************************************************************/