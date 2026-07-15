// execution: 
//     gcc fork_and_wait.c -o fork_and_wait
//     ./fork_and_wait

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>

int main() {
    pid_t pid;

    printf("[Parent] Main process started. PID: %d\n", getpid());
    printf("[Parent] Cloning process via fork()...\n");

    pid = fork();

    if (pid < 0) {
        // Fork failed
        perror("Fork execution failed");
        exit(EXIT_FAILURE);
    } 
    else if (pid == 0) {
        // Child process execution path
        printf("   [Child] Hello from the child process! PID: %d, Parent PID: %d\n", getpid(), getppid());
        printf("   [Child] Simulating compute work for 2 seconds...\n");
        sleep(2);
        printf("   [Child] Work done. Exiting child process gracefully.\n");
        exit(42); // Exit status code handed back to parent
    } 
    else {
        // Parent process execution path (pid contains the child's PID)
        int status;
        printf("[Parent] Child process spawned with PID: %d. Waiting for child...\n", pid);
        
        // wait() blocks the parent until the child exits to clear its process table entry
        pid_t dead_child_pid = wait(&status);

        if (WIFEXITED(status)) {
            printf("[Parent] Child %d died gracefully with exit code: %d\n", dead_child_pid, WEXITSTATUS(status));
        }
    }

    return 0;
}