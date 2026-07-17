// execution: 
//     gcc pthread_mutex.c -o pthread_mutex -lpthread
//     ./pthread_mutex

#include <stdio.h>
#include <pthread.h>

long long global_counter = 0;
pthread_mutex_t lock_gate; // Mutex variable allocation

void* incrementer_routine(void* arg) {
    for (int i = 0; i < 1000000; i++) {
        // --- CRITICAL SECTION START ---
        // Comment out lock and unlock lines to see data corruption via race conditions!
        pthread_mutex_lock(&lock_gate);
        
        global_counter++; // Modifying shared memory
        
        pthread_mutex_unlock(&lock_gate);
        // --- CRITICAL SECTION END ---
    }
    return NULL;
}

int main() {
    pthread_t thread1, thread2;

    // Initialize the mutex lock asset
    pthread_mutex_init(&lock_gate, NULL);

    printf("[System Init] Starting 2 threads. Target count target: 2000000\n");

    pthread_create(&thread1, NULL, incrementer_routine, NULL);
    pthread_create(&thread2, NULL, incrementer_routine, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("[System Finalized] Value of counter: %lld\n", global_counter);

    // Destroy the mutex asset
    pthread_mutex_destroy(&lock_gate);
    return 0;
}

/*******************************************************************************
 * DEEP-DIVE ARCHITECTURAL EXPLANATION: THREAD SYNCHRONIZATION VIA MUTEXES
 *******************************************************************************
 *
 * This code demonstrates how to protect shared memory allocations from data 
 * corruption using a Mutex (short for "Mutual Exclusion"). Without synchronization, 
 * concurrent execution paths will inevitably step on each other's toes.
 *
 * =============================================================================
 * 1. THE PROBLEM: RACE CONDITIONS & THE ILLUSION OF "global_counter++"
 * =============================================================================
 * In C code, `global_counter++` looks like a single, instantaneous action. 
 * At the hardware layer, the CPU cannot modify a variable inside system RAM 
 * directly. It must break this instruction down into three separate assembly steps:
 * 
 *   Step 1 (Read):  Load the current value of `global_counter` from RAM into a CPU register.
 *   Step 2 (Mod):   Increment the value inside that CPU register by 1.
 *   Step 3 (Write): Write the new value from the register back into the RAM address.
 * 
 * If two threads execute this simultaneously without a mutex, a context switch 
 * can happen mid-operation, resulting in an overwritten data collision:
 * 
 *   Thread 1: Reads counter (Value = 10)
 *   Thread 2: Reads counter (Value = 10)
 *   Thread 1: Increments register to 11
 *   Thread 1: Writes 11 to RAM
 *   Thread 2: Increments register to 11
 *   Thread 2: Writes 11 to RAM  <-- Data Corruption! Both threads ran, but 1 increment was lost.
 * 
 * This scenario—where the final output depends entirely on the unpredictable 
 * timing of thread execution scheduling—is called a **Race Condition**.
 *
 * =============================================================================
 * 2. THE CRITICAL SECTION
 * =============================================================================
 * A "Critical Section" is any segment of code that reads or updates a shared 
 * resource (like global variables, linked lists, or file descriptors) that must 
 * not be concurrently accessed by multiple threads. 
 * 
 * In this file, the critical section is tightly bounded:
 *   
 *   pthread_mutex_lock(&lock_gate);   // <-- Gate closes
 *   global_counter++;                 // <-- CRITICAL SECTION
 *   pthread_mutex_unlock(&lock_gate); // <-- Gate opens
 *
 * =============================================================================
 * 3. HOW THE MUTEX ACTS AS A BOUNCER
 * =============================================================================
 * A mutex functions like a digital key card to a single-occupancy restroom. 
 * 
 *   - When Thread 1 reaches `pthread_mutex_lock()`, it checks if the lock is open. 
 *     If it is, Thread 1 claims ownership atomically (an un-interruptible hardware 
 *     operation) and enters the room.
 * 
 *   - If Thread 2 arrives while Thread 1 holds the lock, `pthread_mutex_lock()` 
 *     blocks Thread 2. The OS kernel shifts Thread 2 into a 'Waiting/Blocked' 
 *     queue, putting it to sleep so it consumes 0% CPU while waiting.
 * 
 *   - When Thread 1 finishes, it executes `pthread_mutex_unlock()`. The kernel 
 *     wakes up Thread 2, which then steps up, locks the gate, and processes its loop.
 *
 * =============================================================================
 * 4. INITIALIZATION, DESTRUCTION, AND THE NULL ATTRIBUTE
 * =============================================================================
 * Like threads, mutexes have lifecycle management requirements:
 * 
 *   - `pthread_mutex_init(&lock_gate, NULL);`
 *     Allocates the necessary OS kernel primitives for the lock. The second 
 *     parameter takes a `pthread_mutexattr_t*` pointer. Passing `NULL` tells the 
 *     OS to use standard defaults. Advanced applications pass attributes here 
 *     to configure distinct mutex styles:
 *       * PTHREAD_MUTEX_ERRORCHECK: Throws an explicit error if a thread tries 
 *         to lock a mutex it already owns, preventing permanent deadlocks.
 *       * PTHREAD_MUTEX_RECURSIVE: Allows the same thread to safely lock the 
 *         same mutex multiple times consecutively (useful in recursive algorithms).
 * 
 *   - `pthread_mutex_destroy(&lock_gate);`
 *     Deregisters the structural footprint from the kernel process tables. Trying 
 *     to destroy a locked mutex or one that threads are actively waiting on 
 *     results in undefined crash behaviors.
 *
 *******************************************************************************/