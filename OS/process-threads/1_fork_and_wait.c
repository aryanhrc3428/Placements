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

/*******************************************************************************
 * DEEP-DIVE ARCHITECTURAL EXPLANATION
 *******************************************************************************
 *
 * 1. THE MECHANICS OF fork()
 * ==========================
 * When `pid = fork()` is executed, the Operating System kernel completely clones 
 * the parent process—duplicating its memory space, execution state, and variables. 
 * Crucially, ONE process enters the fork call, but TWO distinct processes exit it.
 *
 * To distinguish identity, the OS returns different values to the `pid` variable:
 *   - In the Child Process: `pid` becomes 0. It enters the `else if (pid == 0)` block.
 *   - In the Parent Process: `pid` becomes the actual PID of the newly created child. 
 *     It enters the `else` block.
 *
 * 2. HOW DOES wait(&status) WORK?
 * ===============================
 * A common misconception is that the `&status` variable handles the waiting logic. 
 * It does not. The `&status` parameter is simply an empty destination memory slot 
 * (an envelope) that the parent hands over to the Operating System kernel.
 *
 * Behind the scenes:
 *   - The Parent process executes `wait(&status)`. The OS intercepts this and moves 
 *     the parent from the 'Running' queue to a 'Blocked/Sleeping' queue. The parent 
 *     is completely frozen and uses 0% CPU.
 *   - The Child process wakes up from its 2-second sleep, runs its code, and invokes 
 *     `exit(42)`. This triggers a hardware interrupt.
 *   - The OS Kernel catches the child's termination, extracts the exit payload (42), 
 *     and directly overwrites the memory space pointed to by `&status` inside the 
 *     parent's scope.
 *   - The OS Kernel then moves the parent back to the 'Running' queue. The parent 
 *     unblocks and processes the data using standard bitmask macros:
 *       * WIFEXITED(status)  -> Validates if the child exited normally on its own.
 *       * WEXITSTATUS(status)-> Isolates and extracts the raw integer status code (42).
 *
 * 3. WHAT IF THE CHILD FINISHES BEFORE THE PARENT CALLS wait()?
 * =============================================================
 * If execution speeds vary and the child finishes its work while the parent is 
 * busy doing something else *before* reaching the `wait()` statement:
 *
 *   - The child process executes `exit(42)`. The OS instantly destroys almost all 
 *     of its active footprints (RAM allocations, hardware hooks, open descriptors).
 *   - However, the OS leaves a small structural receipt in its internal "Process Table". 
 *     This state is designated as a ZOMBIE process (flagged as 'Z' or 'defunct'). 
 *     It remains dead but unpurged so its final data isn't lost.
 *   - When the parent finally executes `wait(&status)`, the OS checks the table, sees 
 *     the zombie child waiting, and immediately extracts the saved data.
 *   - The `wait()` call returns INSTANTLY without putting the parent to sleep, and 
 *     the zombie process entry is permanently purged from the system table.
 *
 *******************************************************************************/