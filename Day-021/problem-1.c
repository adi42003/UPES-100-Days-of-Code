/*
Question: Write a program to swap the first and last digit of a number.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    char number[1000]; int length; char temp;
    if(scanf("%999s",number)!=1) return 1;
    length=(int)strlen(number);
    if(length>1) { temp=number[0]; number[0]=number[length-1]; number[length-1]=temp; }
    puts(number);
    return 0;
}
