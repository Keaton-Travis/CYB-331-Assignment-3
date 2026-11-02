#include <stdio.h>
#include <string.h>

int main() {
    char name[50];

    // Prompt the user for their name
    printf("Enter your name: ");
    
    // Read string input including spaces safely
    if (fgets(name, sizeof(name), stdin) != NULL) {
        // Remove trailing newline character if present
        name[strcspn(name, "\n")] = '\0';
        
        // Print the greeting
        printf("Hello, %s! Welcome to C programming.\n", name);
    }

    return 0;
}