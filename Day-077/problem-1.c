/*
Question: Write a program that reads text from input.txt, converts all lowercase letters to uppercase, and writes the result to output.txt.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    FILE *inputFile, *outputFile;
    int ch;

    inputFile = fopen("input.txt", "r");
    if (inputFile == NULL) {
        puts("Cannot open input.txt");
        return 1;
    }

    outputFile = fopen("output.txt", "w");
    if (outputFile == NULL) {
        fclose(inputFile);
        return 1;
    }

    while ((ch = fgetc(inputFile)) != EOF)
        fputc(toupper((unsigned char)ch), outputFile);

    fclose(inputFile);
    fclose(outputFile);
    puts("Conversion completed. Output written to output.txt");
    return 0;
}
