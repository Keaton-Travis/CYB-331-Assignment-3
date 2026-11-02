#include <stdio.h>
#include <string.h>

int main() {
    char name[100];

    // Ask the user for their name
    printf("Enter your name: ");
    
    // Read the input safely, including spaces
    if (fgets(name, sizeof(name), stdin) != NULL) {
        // Remove the trailing newline character added by fgets
        name[strcspn(name, "\n")] = '\0';
        
        // Print the greeting
        printf("Hello, %s! It's great to meet you.\n", name);
    }

    return 0;
}