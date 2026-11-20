/*
Question: Use pointer to struct to modify and display data using -> operator.
*/

#include <stdio.h>
#include <string.h>

typedef struct {
    char name[50];
    int roll;
    float marks;
} Student;

int main(void) {
    Student student = {"", 0, 0.0f};
    Student *ptr = &student;
    char line[256];
    const char *details;

    if (fgets(line, sizeof line, stdin) == NULL) {
        fprintf(stderr, "Unable to read student details.\n");
        return 1;
    }

    details = strrchr(line, ':');
    if (details != NULL) ++details;
    else details = line;

    /* Update each structure member through the structure pointer. */
    if (sscanf(details, " %49s %d %f", ptr->name,
               &ptr->roll, &ptr->marks) != 3) {
        fprintf(stderr, "Invalid student details.\n");
        return 1;
    }

    printf("Modified Data: Name: %s | Roll: %d | Marks: %g\n",
           ptr->name, ptr->roll, ptr->marks);
    return 0;
}
