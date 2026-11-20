/*
Question: Write a program to take an integer array as input. Only one element will be repeated. Print the repeated element. Try to find the result in one single iteration.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    int n, values[1000], i, j;

    if (scanf("%d", &n) != 1 || n < 2 || n > 1000) return 1;

    for (i = 0; i < n; i++) {
        if (scanf("%d", &values[i]) != 1) return 1;

        for (j = 0; j < i; j++) {
            if (values[j] == values[i]) {
                printf("%d\n", values[i]);
                return 0;
            }
        }
    }

    puts("-1");
    return 0;
}