/*
Question: Store employee data in a binary file using fwrite() and read using fread().
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[50];
    int id;
    double salary;
} Employee;

static int parseEmployee(const char *line, Employee *employee) {
    const char *details = strrchr(line, ':');
    if (details != NULL) ++details;
    else details = line;

    return sscanf(details, " %49s %d %lf", employee->name,
                  &employee->id, &employee->salary) == 3;
}

int main(void) {
    Employee employee, storedEmployee;
    char input[256];
    FILE *file;

    if (fgets(input, sizeof input, stdin) == NULL ||
        !parseEmployee(input, &employee)) {
        fprintf(stderr, "Invalid employee details.\n");
        return EXIT_FAILURE;
    }

    file = fopen("employee.dat", "wb");
    if (file == NULL) {
        perror("Unable to open employee.dat for writing");
        return EXIT_FAILURE;
    }
    if (fwrite(&employee, sizeof employee, 1, file) != 1) {
        perror("Unable to write employee data");
        fclose(file);
        return EXIT_FAILURE;
    }
    if (fclose(file) != 0) {
        perror("Unable to close employee.dat");
        return EXIT_FAILURE;
    }

    file = fopen("employee.dat", "rb");
    if (file == NULL) {
        perror("Unable to open employee.dat for reading");
        return EXIT_FAILURE;
    }
    if (fread(&storedEmployee, sizeof storedEmployee, 1, file) != 1) {
        fprintf(stderr, "Unable to read employee data.\n");
        fclose(file);
        return EXIT_FAILURE;
    }
    if (fclose(file) != 0) {
        perror("Unable to close employee.dat");
        return EXIT_FAILURE;
    }

    printf("Employee data read from file:\n");
    printf("Name: %s | ID: %d | Salary: %.2f\n",
           storedEmployee.name, storedEmployee.id,
           storedEmployee.salary);
    return EXIT_SUCCESS;
}
