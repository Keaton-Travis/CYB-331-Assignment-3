#include <stdio.h>

int main() {
    char name[10];

    // Prompt the user for their name (unsafe: no boundary checks)
    printf("Enter your name: ");
    scanf("%s", name);

    // Print the greeting
    printf("Hello, %s!\n", name);

    return 0;
}