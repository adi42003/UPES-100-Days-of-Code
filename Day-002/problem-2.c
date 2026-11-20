/*
Question: Write a program to calculate the area and circumference of a circle given its radius.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    double r, pi=3.141592653589793;
    if (scanf("%lf", &r) != 1) return 1;
    printf("Area=%.2f, Circumference=%.2f\n", pi*r*r, 2*pi*r);
    return 0;
}
