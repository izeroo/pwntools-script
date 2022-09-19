#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void backdoor() {
    printf("Now entering backdoor...\n");
    execve("/bin/sh", 0, 0);
    printf("Leaving backdoor...\n");
}

void menu() {
    printf("1. write\n");
    printf("2. read\n");
    printf("3. exit\n");
    printf("your choice: ");
}
int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    int choice;
    char buffer[16];
    for (;;) {
        menu();
        scanf("%d", &choice);
        if (choice == 1) {
            printf("input something: ");
            read(0, buffer, 0x64);
        } else if (choice == 2) {
            printf("your input:  %s\n", buffer);
        } else if (choice == 3) {
            printf("exit\n");
            return 0;
        } else {
            printf("Wrong input!!!!\n");
        }
    }
}
