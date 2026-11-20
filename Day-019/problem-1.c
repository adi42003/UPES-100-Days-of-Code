/*
Question: Write a program to find the LCM of two numbers.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    long long a,b,x,y,t;
    if(scanf("%lld %lld",&a,&b)!=2) return 1;
    x=llabs(a); y=llabs(b);
    if(x==0||y==0) { puts("0"); return 0; }
    a=x; b=y;
    while(b) { t=a%b; a=b; b=t; }
    printf("%lld\n",(x/a)*y);
    return 0;
}
