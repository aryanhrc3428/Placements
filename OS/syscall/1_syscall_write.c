// execution:
//     gcc syscall_write.c -o syscall_write
//     ./syscall_write

#include <unistd.h>  // Contains write() and standard file descriptor macros
#include <string.h>  // Contains strlen()

int main() {
    char message[] = "Direct kernel write sequence initiated...\n";
    
    /*
     * write() syntax: write(int fd, const void *buf, size_t count)
     * 1 = Standard Output (stdout)
     * message = Pointer to the character buffer array
     * strlen(message) = Exact count of bytes to push
     */
    ssize_t bytes_written = write(1, message, strlen(message));
    
    // Check if system call executed successfully (-1 indicates failure)
    if (bytes_written == -1) {
        return 1;
    }

    char success_msg[] = "Bytes successfully delivered to screen without printf().\n";
    write(1, success_msg, strlen(success_msg));

    return 0;
}