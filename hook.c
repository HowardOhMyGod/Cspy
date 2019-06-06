
#include <stdio.h>
#include <dlfcn.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

typedef int (*STRCMP) (const char*, const char*);

int strcmp(const char* str1, const char* str2) {
    char log[80];
    int ret;

    int my_fd;
    my_fd = open("./log_profile", O_WRONLY | O_CREAT | O_APPEND);

    void *handle = NULL;
    STRCMP old_func = NULL;

    handle = dlopen("libc.so.6", RTLD_LAZY);
    old_func = (STRCMP) dlsym(handle, "strcmp");
    ret = old_func(str1,str2);

    // return data
    printf("%d", ret);

    // function name and params
    printf("strcmp str1=%s,str2=%s\n", str1, str2);
    sprintf(log, "strcmp str1=%s,str2=%s\n", str1, str2);
    write(my_fd, log, strlen(log));
    close(my_fd);

    return ret;
}

typedef char* (*STRCPY) (const char*, const char*);

char* strcpy(const char* str1, const char* str2) {
    char log[80];
    char* ret;

    int my_fd;
    my_fd = open("./log_profile", O_WRONLY | O_CREAT | O_APPEND);

    void *handle = NULL;
    STRCPY old_func = NULL;

    handle = dlopen("libc.so.6", RTLD_LAZY);
    old_func = (STRCPY) dlsym(handle, "strcpy");
    ret = old_func(str1,str2);

    // return data
    printf("%s", ret);

    // function name and params
    printf("strcpy str1=%s,str2=%s\n", str1, str2);
    sprintf(log, "strcpy str1=%s,str2=%s\n", str1, str2);
    write(my_fd, log, strlen(log));
    close(my_fd);

    return ret;
}

