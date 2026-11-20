/*
Question: Take two structs as input and check if they are identical.
*/

#include <stdio.h>
#include <string.h>

typedef struct {
    char name[50];
    int roll;
    float marks;
} Student;

static int readStudent(Student *student) {
    char line[256];
    const char *details;

    if (fgets(line, sizeof line, stdin) == NULL) return 0;
    details = strrchr(line, ':');
    if (details != NULL) ++details;
    else details = line;

    return sscanf(details, " %49s %d %f", student->name,
                  &student->roll, &student->marks) == 3;
}

int main(void) {
    Student first, second;

    if (!readStudent(&first) || !readStudent(&second)) {
        fprintf(stderr, "Invalid student details.\n");
        return 1;
    }

    if (strcmp(first.name, second.name) == 0 &&
        first.roll == second.roll && first.marks == second.marks)
        printf("Same\n");
    else
        printf("Different\n");

    return 0;
}
