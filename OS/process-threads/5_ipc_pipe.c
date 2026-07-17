// execution: 
//     gcc ipc_pipe.c -o ipc_pipe && ./ipc_pipe

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int main() {
    int pipe_fds[2]; // Array to hold two file descriptors (0 for read, 1 for write)
    pid_t pid;
    char write_message[] = "Systems Pipeline Online. Secure Token: Alpha-99";
    char read_buffer[100];

    // Create pipe channel before executing fork()
    if (pipe(pipe_fds) == -1) {
        perror("Pipeline creation failed");
        return 1;
    }

    pid = fork();

    if (pid == 0) {
        // --- CHILD PROCESS: READER ---
        // Close the unused write end of the pipe channel
        close(pipe_fds[1]); 

        printf("   [Child Reader] Waiting to read bytes from kernel pipe channel...\n");
        int bytes_read = read(pipe_fds[0], read_buffer, sizeof(read_buffer) - 1);
        
        if (bytes_read > 0) {
            read_buffer[bytes_read] = '\0'; // Ensure clean string termination
            printf("   [Child Reader] Payload successfully intercept: \"%s\"\n", read_buffer);
        }

        close(pipe_fds[0]); // Close read descriptor when finished
        exit(EXIT_SUCCESS);
    } 
    else {
        // --- PARENT PROCESS: WRITER ---
        // Close the unused read end of the pipe channel
        close(pipe_fds[0]);

        printf("[Parent Writer] Streaming message payload into the pipe channel...\n");
        write(pipe_fds[1], write_message, strlen(write_message) + 1);
        
        close(pipe_fds[1]); // Close write descriptor, sending EOF to child reader
        wait(NULL);         // Clean up child process
        printf("[Parent Writer] Transaction verified. System clearing execution loops.\n");
    }

    return 0;
}

/*******************************************************************************
 * DEEP-DIVE ARCHITECTURAL EXPLANATION: INTER-PROCESS COMMUNICATION (IPC) VIA PIPES
 *******************************************************************************
 *
 * This program demonstrates one-way (unidirectional) Inter-Process Communication 
 * using a native Unix pipe. It allows a parent process to stream raw bytes 
 * directly out of its isolated memory space and into the brain of a child process.
 *
 * =============================================================================
 * 1. WHAT IS A UNIX PIPE & WHERE DOES IT LIVE?
 * =============================================================================
 * A pipe is not a file on your disk drive. It is a shared, unidirectional data 
 * buffer managed entirely inside the **Kernel Memory Space**. It operates strictly 
 * on a FIFO (First-In, First-Out) model. 
 * 
 * To interact with this kernel buffer, the operating system gives the program 
 * two file descriptors packed into an integer array (`int pipe_fds[2]`). 
 * 
 * You can memorize which index does what using this standard Unix cheat sheet:
 *   - pipe_fds[0]: The **READ** end (Think of '0' as an O-shaped mouth taking data IN).
 *   - pipe_fds[1]: The **WRITE** end (Think of '1' as a straight pen pushing data OUT).
 *
 * =============================================================================
 * 2. THE CRITICAL CHRONOLOGY: CALLING pipe() BEFORE fork()
 * =============================================================================
 * The execution order here is mathematically mandatory. The program must call 
 * `pipe(pipe_fds)` *before* it calls `fork()`. 
 * 
 *   - If you call `pipe()` BEFORE `fork()`: The parent opens the descriptors. 
 *     When `fork()` clones the process, the child inherits exact duplicates of 
 *     those file descriptors. Both processes now have hooks pointing to the 
 *     **exact same kernel buffer**, creating a bridge.
 * 
 *   - If you call `pipe()` AFTER `fork()`: The parent creates a pipe for itself, 
 *     and the child creates a completely separate, isolated pipe for itself. 
 *     They will have no shared bridge, making communication impossible.
 *
 * =============================================================================
 * 3. THE ABSOLUTE MYSTERY: WHY MUST WE CLOSE THE UNUSED ENDS?
 * =============================================================================
 * New C programmers often wonder why lines like `close(pipe_fds[1]);` are forced 
 * into the code. Since a pipe is unidirectional, keeping unused ends open causes 
 * critical structural failures:
 * 
 *   A. Why the Child Reader closes its WRITE end (`pipe_fds[1]`):
 *      The `read()` system call is designed to block and wait for data until 
 *      it receives an **EOF (End of File)** marker. The kernel *only* transmits 
 *      an EOF marker when **every single open write descriptor** for that pipe 
 *      across the entire system is closed. 
 *      If the child forgets to close its inherited write descriptor, the system 
 *      sees that a writer is still alive (the child itself!). The `read()` call 
 *      will freeze and hang forever, causing a permanent deadlock.
 * 
 *   B. Why the Parent Writer closes its READ end (`pipe_fds[0]`):
 *      If a process attempts to write to a pipe that has no active readers 
 *      anywhere in the system, it triggers a kernel panic event for that process. 
 *      The kernel drops a `SIGPIPE` signal on the writer, violently crashing 
 *      the program with a "Broken Pipe" error. Closing the read end keeps 
 *      the descriptor tables clean and leak-free.
 *
 * =============================================================================
 * 4. SYNCHRONIZATION AND MECHANICS
 * =============================================================================
 * Pipes have built-in smart synchronization timing:
 * 
 *   - **If the Child runs first:** It hits `read()`. Because the pipe is currently 
 *     empty, the OS kernel sleeps the child process. It consumes 0% CPU.
 *   - **When the Parent catches up:** It executes `write()`, dumping the string 
 *     into the kernel buffer. The moment data drops in, the kernel instantly 
 *     wakes up the sleeping child.
 *   - The child reads the bytes out of the stream, appends a null terminator (`\0`) 
 *     to format it safely as a standard C-string, and cleanly exits.
 *
 *******************************************************************************/