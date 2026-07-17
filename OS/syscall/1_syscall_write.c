// execution:
//     gcc syscall_write.c -o syscall_write
//     ./syscall_write

#include <unistd.h>  // Contains write() and standard file descriptor macros
#include <string.h>  // Contains strlen()

int main() {
    char message[] = "Direct kernel write sequence initiated...\n";
    
    /*
     * write() syntax: write(int fd, const void *buf, size_t count)
     * 1 = Standard Output (stdout)
     * message = Pointer to the character buffer array
     * strlen(message) = Exact count of bytes to push
     */
    ssize_t bytes_written = write(1, message, strlen(message));
    
    // Check if system call executed successfully (-1 indicates failure)
    if (bytes_written == -1) {
        return 1;
    }

    char success_msg[] = "Bytes successfully delivered to screen without printf().\n";
    write(1, success_msg, strlen(success_msg));

    return 0;
}

/*******************************************************************************
 * DEEP-DIVE ARCHITECTURAL EXPLANATION: Bypassing glibc via Raw System Calls
 *******************************************************************************
 *
 * This code strips away the usual high-level abstractions of C programming to 
 * communicate directly with the Operating System kernel. Instead of asking a 
 * standard library helper like `printf()` to output text, it performs a raw 
 * 'write' system call.
 *
 * =============================================================================
 * 1. THE GREAT DIVIDE: USER SPACE VS. KERNEL SPACE
 * =============================================================================
 * Modern operating systems enforce a strict security boundary between user 
 * applications and core system hardware:
 * 
 *   - User Space (Ring 3): Where your program lives. It is untrusted, sandboxed, 
 *     and forbidden from talking directly to hardware like monitors or disks.
 *   - Kernel Space (Ring 0): The core OS engine. It has absolute, unrestricted 
 *     access to the underlying physical hardware.
 * 
 * When you run `write(1, ...)`, your program cannot print to the screen on its 
 * own. Instead, it triggers a hardware trap instruction (a CPU context switch). 
 * The execution pauses in User Space, leaps across the boundary into Kernel Space, 
 * lets the OS copy the string to the display hardware, and then leaps back.
 *
 * =============================================================================
 * 2. UNDER THE HOOD: printf() VS. write()
 * =============================================================================
 * Beginners often think `printf()` is how C writes data. In reality, `printf()` 
 * is just an elaborate wrapper function provided by the C Standard Library 
 * (`glibc`). Here is what happens under the hood:
 *
 *   - `printf("%d\n", value)`: Parses format specifiers, allocates a hidden 
 *     memory buffer, translates integers into text characters, and stores them. 
 *     Only when the buffer is full, or a newline `\n` is detected, does `printf()` 
 *     internally drop down and invoke the raw `write()` system call anyway!
 * 
 *   - `write()`: Bypasses all parsing, buffering, and formatting overhead. It 
 *     takes the raw data exactly as it sits in memory and immediately forces a 
 *     kernel switch. It is faster, raw, and unbuffered.
 *
 * =============================================================================
 * 3. DECODING THE MAGIC NUMBERS: FILE DESCRIPTORS
 * =============================================================================
 * In Unix-like operating systems, *"everything is a file"*. To read or write to 
 * anything (a text file, a network socket, a terminal screen), you use an 
 * integer index known as a **File Descriptor (FD)**.
 * 
 * When any new process spawns, the kernel automatically opens three fundamental 
 * standard data streams for it:
 * 
 *  +----+-----------------+-----------------+---------------------------------+
 *  | FD | Stream Name     | POSIX Macro     | Hardware Routing Target         |
 *  +----+-----------------+-----------------+---------------------------------+
 *  | 0  | Standard Input  | STDIN_FILENO    | Reads input from the Keyboard   |
 *  | 1  | Standard Output | STDOUT_FILENO   | Prints normal output to Screen  |
 *  | 2  | Standard Error  | STDERR_FILENO   | Prints errors instantly to Screen|
 *  +----+-----------------+-----------------+---------------------------------+
 * 
 * In this code, we passed `1` as the first argument, instructing the kernel to 
 * target the terminal console's standard output pipeline.
 *
 * =============================================================================
 * 4. THE MECHANICS OF ssize_t AND RETURN TRACKING
 * =============================================================================
 * Notice that `write()` does not return a normal `int`; it returns an `ssize_t`. 
 * 
 *   - `size_t`  is an *unsigned* integer type used to represent sizes.
 *   - `ssize_t` is a *signed* size type (Signed Size Type). 
 * 
 * Why signed? Because system calls need a universal way to report devastating 
 * failures. If `write()` successfully outputs your data, it returns the positive 
 * count of bytes actually written. If the terminal line suddenly disconnects, 
 * the disk fills up, or you pass an invalid memory address, `write()` returns `-1`.
 * 
 * When a `-1` is returned, the kernel also populates a global system variable 
 * named `errno` with a specific error code (like `EBADF` for a bad file descriptor), 
 * allowing developers to diagnose exactly why the hardware connection failed.
 *
 *******************************************************************************/