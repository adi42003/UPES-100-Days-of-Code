/*
Question: Open an existing file in append mode and allow the user to enter a new line of text. Append the text at the end without overwriting existing content.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    FILE *file;
    char line[1000];

    if (fgets(line, sizeof(line), stdin) == NULL) return 1;
    line[strcspn(line, "\n")] = '\0';

    file = fopen("data.txt", "a");
    if (file == NULL) {
        puts("Unable to open data.txt");
        return 1;
    }

    fprintf(file, "%s\n", line);
    fclose(file);
    puts("File updated successfully with appended text.");
    return 0;
}
