// execution: 
//     gcc pthread_custom.c -o pthread_custom -lpthread
//     ./pthread_custom

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sched.h>   // Required for structural scheduling parameters
#include <unistd.h>

void* async_worker(void* arg) {
    printf("   [Thread Worker] Running with specialized attribute profiles...\n");
    sleep(1);
    printf("   [Thread Worker] Task completed smoothly.\n");
    return NULL;
}

int main() {
    pthread_t thread_id;
    pthread_attr_t my_custom_attr; // 1. Create the attribute structure variable

    // 2. Initialize the attribute object with standard operating system defaults
    pthread_attr_init(&my_custom_attr);
    
    // =====================================================================
    // VARIATION 1: DETACH STATE CONFIGURATION
    // =====================================================================
    // Changes whether the thread needs to be reaped via pthread_join().
    // Options: PTHREAD_CREATE_JOINABLE (Default) or PTHREAD_CREATE_DETACHED
    printf("[Main System] Configuring thread as DETACHED...\n");
    pthread_attr_setdetachstate(&my_custom_attr, PTHREAD_CREATE_DETACHED);


    // =====================================================================
    // VARIATION 2: CUSTOM STACK SIZE ALLOCATION
    // =====================================================================
    // Overrides the standard OS allocation size (which is usually 2MB - 8MB).
    // Highly critical for low-RAM embedded hardware or memory-bound apps.
    size_t custom_stack = 512 * 1024; // Shrink stack down to 512 Kilobytes
    printf("[Main System] Adjusting stack limits to %zu bytes...\n", custom_stack);
    pthread_attr_setstacksize(&my_custom_attr, custom_stack);


    // =====================================================================
    // VARIATION 3: SCHEDULING POLICY & REAL-TIME CPU PRIORITY
    // =====================================================================
    // Adjusts how the OS kernel schedules this thread relative to others.
    // Policies: SCHED_OTHER (Default normal), SCHED_FIFO (Real-time First-In-First-Out), 
    //           SCHED_RR (Real-time Round-Robin).
    // Note: Real-time profiles typically require superuser/root permissions.
    printf("[Main System] Tuning real-time execution priority profiles...\n");
    
    // Step A: Set scheduling engine model to Round Robin
    pthread_attr_setschedpolicy(&my_custom_attr, SCHED_RR);

    // Step B: Assign execution weight priority (scale ranges from 1 to 99)
    struct sched_param priority_param;
    priority_param.sched_priority = 50; 
    pthread_attr_setschedparam(&my_custom_attr, &priority_param);
    
    // Step C: Force thread to respect these explicit rules instead of inheriting parent states
    pthread_attr_setinheritsched(&my_custom_attr, PTHREAD_EXPLICIT_SCHED);


    // =====================================================================
    // 4. Pass the POINTER to the customized configurations into pthread_create
    // =====================================================================
    if (pthread_create(&thread_id, &my_custom_attr, async_worker, NULL) != 0) {
        perror("Failed to instantiate thread with given customization profile");
        pthread_attr_destroy(&my_custom_attr);
        return 1;
    }

    // =====================================================================
    // 5. Clean up the configuration container wrapper safely
    // =====================================================================
    // Crucial Note: This does NOT impact or kill the live running thread! 
    // It simply frees the temporary settings memory footprint we generated.
    pthread_attr_destroy(&my_custom_attr); 

    // Because the thread is detached, we cannot call pthread_join().
    // We pause the main thread briefly to allow the background thread to finish.
    sleep(2);
    printf("[Main System] Shutdown complete.\n");
    return 0;
}

/*******************************************************************************
 * DEEP-DIVE ARCHITECTURAL EXPLANATION: THE CUSTOMIZATION VARIATIONS
 *******************************************************************************
 *
 * A `pthread_attr_t` object is an internal opaque structural bitmask. Think of 
 * it as a configuration profile selector. By default, `pthread_create` provides 
 * standard choices, but manual configurations alter fundamental behaviors:
 *
 * =============================================================================
 * 1. DETACH STATE VARIATIONS (`pthread_attr_setdetachstate`)
 * =============================================================================
 * Under normal system behavior (`PTHREAD_CREATE_JOINABLE`), a thread mimics a 
 * child process. When it dies, it becomes a zombie until the parent runs 
 * `pthread_join()`. This holds onto internal OS descriptor tables.
 *
 * By overriding this with `PTHREAD_CREATE_DETACHED`:
 *   - The thread acts as an isolated daemon worker.
 *   - The split second it returns or hits `pthread_exit()`, the OS completely 
 *     purges its stack frames and tracking indices.
 *   - Perfect for fire-and-forget routines (e.g., logging tasks, background 
 *     network heartbeats).
 *
 * =============================================================================
 * 2. STACK SIZE VARIATIONS (`pthread_attr_setstacksize`)
 * =============================================================================
 * When a thread spins up, the OS slices out a specific segment of virtual address 
 * space for its stack frame (where local processing variables and function calls 
 * are kept). On Linux, this defaults to a massive 8 Megabytes.
 *
 * If your architecture needs to launch 1,000 threads simultaneously, that configuration 
 * requires 8 Gigabytes of memory just to instantiate the threads! 
 *   - By dialing it down using `pthread_attr_setstacksize`, you optimize space.
 *   - Shrinking it to 512KB means 1,000 threads now consume only 500 Megabytes.
 *   - Caution: Setting this value too low causes immediate "Stack Overflow" 
 *     segmentation faults if your thread runs deep recursive functions.
 *
 * =============================================================================
 * 3. SCHEDULING & PRIORITY VARIATIONS (`pthread_attr_setschedpolicy`)
 * =============================================================================
 * Standard threads run on time-sharing models (`SCHED_OTHER`). The OS switches 
 * execution contexts back and forth dynamically, ensuring no process hogs the CPU.
 *
 * Real-time variations change the execution rules:
 *   - `SCHED_FIFO` (First-In, First-Out): Once this thread starts running on a CPU core, 
 *     it *cannot* be preempted by standard applications. It runs until it completes 
 *     its task, sleeps, or voluntarily yields.
 *   - `SCHED_RR` (Round-Robin): Real-time threads share processing slices evenly 
 *     amongst other high-priority tasks, but run circles around standard apps.
 * 
 * The `sched_priority` value defines which thread wins the execution race. If a 
 * priority 50 thread wakes up while a priority 10 thread is running, the kernel 
 * immediately stops the priority 10 thread mid-instruction to let the priority 50 
 * thread take control.
 *
 *******************************************************************************/