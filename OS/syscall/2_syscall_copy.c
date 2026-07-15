// execution: 
//     gcc syscall_copy.c -o syscall_copy
//     ./syscall_copy

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>   // Contains open() flags like O_RDONLY, O_WRONLY, O_CREAT

#define BUFFER_SIZE 64

int main() {
    int src_fd, dest_fd;
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read, bytes_written;

    // 1. Open source file in Read-Only mode
    src_fd = open("input_sample.txt", O_RDONLY);
    if (src_fd == -1) {
        perror("Error opening source file");
        exit(EXIT_FAILURE);
    }

    /*
     * 2. Open/Create destination file
     * O_WRONLY: Write-only mode
     * O_CREAT: Create file if it doesn't exist
     * O_TRUNC: Clear existing content if file exists
     * 0644: Permissions mode (Owner: Read/Write, Group/Others: Read-only)
     */
    dest_fd = open("output_cloned.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (dest_fd == -1) {
        perror("Error creating destination file");
        close(src_fd); // Don't leave file handles leaking!
        exit(EXIT_FAILURE);
    }

    // 3. Core I/O Stream Loop
    // read() returns the number of bytes read, 0 at EOF, or -1 on error
    while ((bytes_read = read(src_fd, buffer, BUFFER_SIZE)) > 0) {
        bytes_written = write(dest_fd, buffer, bytes_read);
        if (bytes_written == -1) {
            perror("Error writing to destination file");
            break;
        }
    }

    if (bytes_read == -1) {
        perror("Critical error encountered during read phase");
    }

    // 4. Release kernel file descriptors
    close(src_fd);
    close(dest_fd);

    printf("File copy pipeline executed. Verify 'output_cloned.txt'.\n");
    return 0;
}