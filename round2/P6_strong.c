#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void) {
    char name[64];

    printf("Enter your name: ");
    
    // Safely read input with a limit of 64 bytes
    if (fgets(name, sizeof(name), stdin) == NULL) {
        fprintf(stderr, "Error: Failed to read input from standard input.\n");
        return 1;
    }

    size_t len = strlen(name);

    // Check if the input exceeded the buffer size (no newline found and not EOF)
    if (len > 0 && name[len - 1] != '\n') {
        fprintf(stderr, "Error: Input exceeds the 64-byte buffer limit.\n");
        
        // Clear the remaining characters from the input buffer
        int c;
        while ((c = getchar()) != '\n' && c != EOF);
        return 1;
    } 
    else if (len > 0) {
        // Remove the trailing newline character for clean output formatting
        name[len - 1] = '\0';
        len--;
    }

    // Validate that all characters are strictly ASCII
    for (size_t i = 0; i < len; i++) {
        // Casting to unsigned char prevents undefined behavior with signed chars
        if (!isascii((unsigned char)name[i])) {
            fprintf(stderr, "Error: Non-ASCII characters detected in input.\n");
            return 1;
        }
    }

    // Success
    printf("Hello, %s!\n", name);
    return 0;
}