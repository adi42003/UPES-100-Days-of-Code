/*
Question: Write a program to find the product of odd digits of a number.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    char number[1000];
    int oddDigits[1000], count = 0, product = 1, i;

    if (scanf("%999s", number) != 1) return 1;

    for (i = 0; number[i] != '\0'; i++) {
        if (number[i] >= '0' && number[i] <= '9') {
            int digit = number[i] - '0';
            if (digit % 2 == 1) {
                oddDigits[count++] = digit;
                product *= digit;
            }
        } else if (number[i] != '-' && number[i] != '+') {
            puts("Invalid number");
            return 1;
        }
    }

    if (count == 0) {
        puts("1 (no odd digits, assume 1)");
        return 0;
    }

    printf("%d (", product);
    for (i = 0; i < count; i++) {
        if (i > 0) putchar('*');
        printf("%d", oddDigits[i]);
    }
    puts(")");
    return 0;
}