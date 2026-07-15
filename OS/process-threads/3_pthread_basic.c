// execution: 
//     gcc pthread_basic.c -o pthread_basic -lpthread
//     ./pthread_basic

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

// The entry routine function for our custom thread
void* async_worker(void* arg) {
    int input_val = *(int*)arg;
    printf("   [Thread Worker] Running thread task. Received payload: %d\n", input_val);
    sleep(1);
    
    // Allocate heap data to return value safely back to main scope
    int* result = malloc(sizeof(int));
    *result = input_val * 10;
    
    printf("   [Thread Worker] Task complete. Returning value...\n");
    pthread_exit((void*)result);
}

int main() {
    pthread_t thread_id;
    int data_payload = 45;
    void* thread_return_ptr;

    printf("[Main System] Spawning worker thread...\n");

    // Create the thread (pass the pointer to function and the address of arguments)
    if (pthread_create(&thread_id, NULL, async_worker, &data_payload) != 0) {
        perror("Failed to create thread");
        return 1;
    }

    printf("[Main System] Thread running. Waiting via pthread_join()...\n");
    
    // pthread_join blocks main execution until the thread safely terminates
    pthread_join(thread_id, &thread_return_ptr);

    int final_output = *(int*)thread_return_ptr;
    printf("[Main System] Thread collected. Result payload calculation: %d\n", final_output);

    // Clean up heap data allocated by the thread worker
    free(thread_return_ptr);
    return 0;
}