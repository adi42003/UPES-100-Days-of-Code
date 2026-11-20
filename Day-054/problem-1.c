/*
Question: Write a Program to take a positive integer n as input, and find the pivot integer x such that the sum of all elements between 1 and x inclusively equals the sum of all elements between x and n inclusively. Print the pivot integer x. If no such integer exists, print -1. Assume that it is guaranteed that there will be at most one pivot integer for the given input.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    long long n,x;
    if(scanf("%lld",&n)!=1 || n<1) return 1;
    for(x=1;x<=n;x++) {
        long long left=x*(x+1)/2;
        long long right=n*(n+1)/2-(x-1)*x/2;
        if(left==right) { printf("%lld\n",x); return 0; }
    }
    puts("-1");
    return 0;
}
