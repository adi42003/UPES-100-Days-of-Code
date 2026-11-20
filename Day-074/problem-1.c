/*
Question: Take two filenames from the user – a source file and a destination file. Copy all the content from the source file to the destination file using fgetc() and fputc().
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    char sourceName[256], destinationName[256];
    int ch;
    FILE *sourceFile, *destinationFile;

    if (scanf("%255s %255s", sourceName, destinationName) != 2) return 1;

    sourceFile = fopen(sourceName, "r");
    if (sourceFile == NULL) {
        puts("Cannot open source file");
        return 1;
    }

    destinationFile = fopen(destinationName, "w");
    if (destinationFile == NULL) {
        fclose(sourceFile);
        puts("Cannot create destination file");
        return 1;
    }

    while ((ch = fgetc(sourceFile)) != EOF)
        fputc(ch, destinationFile);

    fclose(sourceFile);
    fclose(destinationFile);
    printf("File copied successfully to %s\n", destinationName);
    return 0;
}
