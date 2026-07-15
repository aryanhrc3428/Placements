// execution: 
//     gcc ipc_pipe.c -o ipc_pipe
//     ./ipc_pipe

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