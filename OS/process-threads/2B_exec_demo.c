// execution: 
//     gcc exec_target.c -o exec_target
//     gcc exec_demo.c -o exec_demo
//     ./exec_demo

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        printf("   [Child Launcher] About to replace execution image via execvp()...\n");
        
        // Arguments array must be NULL-terminated
        char *args[] = {"./exec_target", "ArgPassed1", "ArgPassed2", NULL};
        
        // execvp completely replaces the child process memory space with exec_target
        execvp(args[0], args);
        
        // If execvp succeeds, this next line is completely erased and NEVER runs
        perror("execvp failed to run");
        exit(EXIT_FAILURE);
    } 
    else {
        // Parent simply waits for the modified child to finish
        wait(NULL);
        printf("[Parent Launcher] Child process finished execution sequence.\n");
    }

    return 0;
}