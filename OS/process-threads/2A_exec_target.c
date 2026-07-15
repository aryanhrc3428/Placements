#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    printf("   [Target Program] Custom executable active! PID: %d\n", getpid());
    
    // Print arguments passed from the launcher process
    for(int i = 0; i < argc; i++) {
        printf("   [Target Program] Argument [%d]: %s\n", i, argv[i]);
    }

    return 0;
}