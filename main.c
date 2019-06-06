#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    char *name = "Howard";
    char *cpy_name = NULL;

    FILE * fd;
    size_t a = 5;

    printf("Start fopen...\n");
    fd = fopen("./.test", "w");
    printf("End fopen()...\n");
    fclose(fd);

    cpy_name = (char *) malloc(7 * sizeof(char));

    strcpy(cpy_name, name);
    printf("cpy_name: %s\n", cpy_name);
    if( strcmp(argv[1], "test") )
    {
        printf("Incorrect password\n");
    }
    else
    {
        printf("Correct password\n");
    }
    return 0;
}
