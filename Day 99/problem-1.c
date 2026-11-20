/*
Question: Use malloc() to allocate structure memory dynamically and print details.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[50];
    int roll;
    float marks;
} Student;

int main(void) {
    Student *student = malloc(sizeof *student);
    char line[256];
    const char *details;

    if (student == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }
    if (fgets(line, sizeof line, stdin) == NULL) {
        fprintf(stderr, "Unable to read student details.\n");
        free(student);
        return 1;
    }

    details = strrchr(line, ':');
    if (details != NULL) ++details;
    else details = line;

    if (sscanf(details, " %49s %d %f", student->name,
               &student->roll, &student->marks) != 3) {
        fprintf(stderr, "Invalid student details.\n");
        free(student);
        return 1;
    }

    printf("Name: %s | Roll: %d | Marks: %g\n",
           student->name, student->roll, student->marks);
    free(student);
    return 0;
}
