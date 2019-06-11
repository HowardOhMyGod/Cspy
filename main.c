#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dirent.h>
#include <shadow.h>
#include <time.h>


void tester (void);
void directory(void);
void permission(void);
void others(void);

// directoru-related operation
void directory(void) {
    DIR *dp;
    struct dirent *dirp;
    char* test_dir = "./dir_test";
    int c = 0;

    if ((dp = opendir(test_dir)) == NULL) {
        printf("can’t open %s\n", test_dir);
        exit(1);
    }

    printf("opendir...\n");
    while ((dirp = readdir(dp)) != NULL) {
        printf("c: %d\n", ++c);
        printf("%s\n", dirp->d_name);
    }
    printf("11 Closing dir...\n");
    closedir(dp);
    printf("Closing dir...\n");
}

void permission(void) {
    struct spwd *pwd;

    pwd = getspent();
}

void others(void) {
    struct timespec reqtp, r;
    int res;

    reqtp.tv_sec = 5;
    reqtp.tv_nsec = 0;
    res = nanosleep(&reqtp, NULL);
    printf("res: %d\n", res);
    printf("PATH : %s\n", getenv("PATH"));
}

void tester (void) {
    directory();
    // permission();
    others();
}

int main(int argc, char *argv[])
{
    char *name = "Howard";
    char *cpy_name = NULL;

    FILE * fd;
    size_t a = 5;

    fd = fopen("./.test", "w");
    fclose(fd);

    cpy_name = (char *) malloc(7 * sizeof(char));

    strcpy(cpy_name, name);
    printf("cpy_name: %s\n", cpy_name);
    if( strcmp("test", "test") )
    {
        printf("Incorrect password\n");
    }
    else
    {
        printf("Correct password\n");
    }

    tester();
    return 0;
}
