// execution: 
//     gcc syscall_errors.c -o syscall_errors
//     ./syscall_errors

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>    // Gives access to the global, thread-safe 'errno' variable
#include <string.h>   // Gives access to strerror()

int main() {
    // Attempting to open a non-existent file to force a system call breakdown
    int fd = open("non_existent_secure_vault.txt", O_RDONLY);
    
    if (fd == -1) {
        printf("System call failed! Kernel modified global errno status flag.\n\n");
        
        // 1. Inspecting raw numerical error value
        printf("A. Raw errno integer value: %d\n", errno);
        
        // 2. Using strerror() to print descriptive string from the system dictionary
        printf("B. Translated error string: %s\n", strerror(errno));
        
        // 3. Using standard perror() which automatically appends the string context
        printf("C. Standard output via perror():\n   ");
        perror("Custom Log Context Tag");
    } else {
        close(fd);
    }

    return 0;
}