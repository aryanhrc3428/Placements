// execution: 
//     gcc syscall_loop.c -o syscall_loop
//     ./syscall_loop

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int main() {
    int fd = open("input_sample.txt", O_RDONLY);
    if (fd == -1) {
        perror("Failed to open asset file");
        return 1;
    }

    // Intentionally small buffer chunk to force loop cycles
    char chunk_buffer[10]; 
    ssize_t bytes_read;
    int loop_counter = 1;

    printf("--- Beginning Chunk Processing Stream ---\n");

    while ((bytes_read = read(fd, chunk_buffer, sizeof(chunk_buffer))) > 0) {
        printf("\n[Chunk #%d | Bytes Pulled: %ld]\n", loop_counter++, bytes_read);
        
        // Write the pulled chunk straight out to stdout
        write(1, "Data: \"", 7);
        write(1, chunk_buffer, bytes_read);
        write(1, "\"\n", 2);
    }

    if (bytes_read == 0) {
        printf("\n--- End of File (EOF) reached successfully. ---\n");
    } else if (bytes_read == -1) {
        perror("Stream failure error");
    }

    close(fd);
    return 0;
}