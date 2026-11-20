/*
Question: Write a program to find the roots of a quadratic equation and categorize them.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    double a,b,c,d,x1,x2;
    if(scanf("%lf %lf %lf",&a,&b,&c)!=3 || a==0) return 1;
    d=b*b-4*a*c;
    if(d>0) {
        x1=(-b+sqrt(d))/(2*a); x2=(-b-sqrt(d))/(2*a);
        printf("Roots are real and different: %.0f, %.0f\n",x1,x2);
    } else if(fabs(d)<1e-9) {
        x1=-b/(2*a); printf("Roots are real and same: %.0f\n",x1);
    } else printf("Roots are complex\n");
    return 0;
}
