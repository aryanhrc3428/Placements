// execution: 
//     gcc syscall_errors.c -o syscall_errors
//     ./syscall_errors

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>    // Gives access to the global, thread-safe 'errno' variable
#include <string.h>   // Gives access to strerror()

int main() {
    // Attempting to open a non-existent file to force a system call breakdown
    int fd = open("non_existent_secure_vault.txt", O_RDONLY);
    
    if (fd == -1) {
        printf("System call failed! Kernel modified global errno status flag.\n\n");
        
        // 1. Inspecting raw numerical error value
        printf("A. Raw errno integer value: %d\n", errno);
        
        // 2. Using strerror() to print descriptive string from the system dictionary
        printf("B. Translated error string: %s\n", strerror(errno));
        
        // 3. Using standard perror() which automatically appends the string context
        printf("C. Standard output via perror():\n   ");
        perror("Custom Log Context Tag");
    } else {
        close(fd);
    }

    return 0;
}

/*******************************************************************************
 * DEEP-DIVE ARCHITECTURAL EXPLANATION: UNIX KERNEL ERROR MANAGEMENT
 *******************************************************************************
 *
 * This program demonstrates how modern operating system kernels communicate 
 * hardware, file system, and permission failures back up to user applications. 
 * Instead of crashing blindly, system calls leverage a unified diagnostic framework 
 * built around `errno`.
 *
 * =============================================================================
 * 1. THE ARCHITECTURE OF ERRNO (THE GLOBAL SIGNAL FLAG)
 * =============================================================================
 * When a low-level system call (like `open()`, `read()`, or `fork()`) encounters 
 * a structural barrier, it follows a strict sequence:
 *   1. It immediately halts execution in Kernel Space.
 *   2. It maps the root cause of the failure to a standard system integer constant.
 *   3. It writes that integer value into a special variable named `errno`.
 *   4. It switches context back to User Space and returns `-1` (or `NULL` for pointers).
 * 
 * Historically, `errno` was a plain global integer (`int errno;`). In modern 
 * multi-threaded architectures, a shared global variable would cause severe data 
 * corruption—Thread A might fail an operation, but before it can read `errno`, 
 * Thread B might execute a different failed call and overwrite the value.
 * 
 * To solve this, `errno` is engineered as a **Thread-Local Macro Variable**. Under 
 * the hood, it resolves to a unique, thread-safe function call or storage pointer 
 * (like `*__errno_location()`). Every thread has its own isolated error box.
 *
 * =============================================================================
 * 2. DECODING THE CONSTANTS: WHAT HAPPENED HERE?
 * =============================================================================
 * In this specific code, we forced a failure by passing a non-existent file name. 
 * The system maps this failure to the numeric value `2`, which represents the 
 * POSIX macro constant **`ENOENT`** (Error No Entity / File not found).
 * 
 * Here are a few common foundational kernel error numbers you will encounter:
 * 
 *  +-------+------------+-----------------------------------------------------+
 *  | Value | Macro Name | Human-Readable Description                          |
 *  +-------+------------+-----------------------------------------------------+
 *  | 1     | EPERM      | Operation not permitted (Root privileges missing)    |
 *  | 2     | ENOENT     | No such file or directory                           |
 *  | 5     | EIO        | Input/output error (Physical hardware failure)       |
 *  | 9     | EBADF      | Bad file descriptor (Operating on a closed handle)  |
 *  | 13    | EACCES     | Permission denied (Read/Write bit access violation) |
 *  | 22    | EINVAL     | Invalid argument passed to system call              |
 *  +-------+------------+-----------------------------------------------------+
 *
 * =============================================================================
 * 3. THE DIAGNOSTIC ARSENAL: strerror() VS. perror()
 * =============================================================================
 * Once `errno` captures a failure state, the application has multiple ways to 
 * interpret and format the numeric data:
 * 
 *   A. `strerror(int errnum)` (Functional String Mapping):
 *      - Located in `<string.h>`, this function performs an internal dictionary 
 *        lookup against the operating system's local language translation table.
 *      - It returns a clean pointer to a static description string. 
 *      - **Use Case**: Excellent when you need complete control over formatting, 
 *        such as constructing custom log strings or broadcasting error payloads 
 *        over network sockets.
 * 
 *   B. `perror(const char *s)` (Automated Diagnostic Tool):
 *      - Located in `<stdio.h>`, this function handles formatting and output 
 *        simultaneously, reducing the developer's work to a single line.
 *      - It automatically prints your custom string argument tag, appends a 
 *        colon and space (`: `), inserts the text translation of the current 
 *        `errno` state, and forces a trailing newline (`\n`).
 *      - **Crucial Hardware Routing**: Unlike `printf()`, which streams to 
 *        Standard Output (FD 1), `perror()` explicitly bypasses user buffering 
 *        and streams directly to **Standard Error (FD 2)**. This ensures error logs 
 *        appear on the screen immediately even if stdout is redirected to a file.
 *
 * =============================================================================
 * 4. THE TIME-SENSITIVITY PRINCIPLE: THE CACHING CONSTRAINT
 * =============================================================================
 * Successful system calls **never** clear or reset `errno` back to `0`. If a 
 * program runs a system call that fails, `errno` updates to the error code. If 
 * the program subsequently executes five successful system calls, `errno` will 
 * *still* hold that old error number!
 * 
 * Therefore, you must only inspect `errno` immediately after a system call 
 * explicitly returns an unambiguous error signal (like `-1`). 
 * 
 * If you need to perform processing steps before logging the error, you should 
 * instantly cache the value to prevent intermediate operations from corrupting it:
 * 
 *   int fd = open("file.txt", O_RDONLY);
 *   if (fd == -1) {
 *       int saved_errno = errno; // Caching the data immediately
 *       printf("Doing unrelated cleanup work here...\n"); 
 *       // The cleanup work might overwrite 'errno', but 'saved_errno' is safe!
 *       logger_dispatch(strerror(saved_errno));
 *   }
 *
 *******************************************************************************/