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