/*
Question: Write a program to find the HCF (GCD) of two numbers.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    int a,b,t;
    if(scanf("%d %d",&a,&b)!=2) return 1;
    a=abs(a); b=abs(b);
    while(b!=0) { t=a%b; a=b; b=t; }
    printf("%d\n",a);
    return 0;
}
