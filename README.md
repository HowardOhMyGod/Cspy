# Cspy
A C function call hooking generator using python.

## Project Structure
| File | Usage | Output |
| -------- | -------- |-------- |
| `api.yml`     | Define target functions you wanna hook| -
| `hook_compile.py`     | Generate API hooking function from api.yml | `hook.c`
| `hook.c`     | This file will be compiled as .so to insert into LD_PRELOAD | `hook.so`
| `main.c`     | Main program to be hooked | `main`
| `makefile`     | Compile main.c and hook.c | `hook.so, main`
| `run.sh`     | Run main with hooking functions | `log_profile`
| `log_profile`     | Function hooking logs. Format:  [return] func_name p_name=p_value | -

## Example

### log_prpfile
Hooking `strcpy` and `strcmp`
```
[Howard] strcpy str1=Howard,str2=Howard
[0] strcmp str1=test,str2=test
```

## Hook Functions
|API                                                                                                                                     |Header                                |Type      |
|----------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|----------|
|struct dirent *readdir(DIR *dirp);                                                                                                      |#include <dirent.h>                   |file      |
|FILE *fopen(const char *pathname, const char *mode);                                                                                    |#include <stdio.h>                    |file      |
|FILE *fdopen(int fd, const char *mode);                                                                                                 |#include <stdio.h>                    |file      |
|size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream)                                                                 |#include <stdio.h>                    |file      |
|size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);                                                                       |#include <stdio.h>                    |file      |
|int fclose(FILE *stream);                                                                                                               |#include <stdio.h>                    |file      |
|int remove(const char *pathname);                                                                                                       |#include <stdio.h>                    |file      |
|int rename(const char *oldpath, const char *newpath);                                                                                   |#include <stdio.h>                    |file      |
|int mkdir(const char *pathname, mode_t mode);                                                                                           |#include <sys/stat.h> <sys/types.h>   |file      |
|DIR *opendir(const char *name);                                                                                                         |#include <sys/types.h> <dirent.h>     |file      |
|int link(const char *oldpath, const char *newpath);                                                                                     |#include <unistd.h>                   |file      |
|int unlink(const char *pathname);                                                                                                       |#include <unistd.h>                   |file      |
|int rmdir(const char *pathname);                                                                                                        |#include <unistd.h>                   |file      |
|int chdir(const char *path);                                                                                                            |#include <unistd.h>                   |file      |
|char *getcwd(char *buf, size_t size);                                                                                                   |#include <unistd.h>                   |file      |
|int symlink(const char *target, const char *linkpath);                                                                                  |#include <unistd.h>                   |file      |
|ssize_t readlink(const char *pathname, char *buf, size_t bufsiz);                                                                       |#include <unistd.h>                   |file      |
|int truncate(const char *path, off_t length);                                                                                           |#include <unistd.h> <sys/types.h>     |file      |
|int socket(int domain, int type, int protocol);                                                                                         |#include <sys/types.h> <sys/socket.h> |network   |
|int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);                                                                   |#include <sys/types.h> <sys/socket.h> |network   |
|int listen(int sockfd, int backlog);                                                                                                    |#include <sys/types.h> <sys/socket.h> |network   |
|int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);                                                                      |#include <sys/types.h> <sys/socket.h> |network   |
|int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);                                                                |#include <sys/types.h> <sys/socket.h> |network   |
|ssize_t send(int sockfd, const void *buf, size_t len, int flags);                                                                       |#include <sys/types.h> <sys/socket.h> |network   |
|ssize_t sendto(int sockfd, const void *buf, size_t len, int flags, const struct sockaddr *dest_addr, socklen_t addrlen);                |#include <sys/types.h> <sys/socket.h> |network   |
|ssize_t sendmsg(int sockfd, const struct msghdr *msg, int flags);                                                                       |#include <sys/types.h> <sys/socket.h> |network   |
|ssize_t recv(int sockfd, void *buf, size_t len, int flags);                                                                             |#include <sys/types.h> <sys/socket.h> |network   |
|ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags, struct sockaddr *src_addr, socklen_t *addrlen);                          |#include <sys/types.h> <sys/socket.h> |network   |
|ssize_t recvmsg(int sockfd, struct msghdr *msg, int flags);                                                                             |#include <sys/types.h> <sys/socket.h> |network   |
|int gethostname(char *name, size_t len);                                                                                                |#include <unistd.h>                   |network   |
|int sethostname(const char *name, size_t len);                                                                                          |#include <unistd.h>                   |network   |
|char *getenv(const char *name);                                                                                                         |#include <stdlib.h>                   |others    |
|int setenv(const char *name, const char *value, int overwrite);                                                                         |#include <stdlib.h>                   |others    |
|int unsetenv(const char *name);                                                                                                         |#include <stdlib.h>                   |others    |
|int putenv(char *string);                                                                                                               |#include <stdlib.h>                   |others    |
|unsigned int sleep(unsigned int seconds);                                                                                               |#include <stdlib.h>                   |others    |
|void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);                                                       |#include <sys/mman.h>                 |others    |
|int uname(struct utsname *buf);                                                                                                         |#include <sys/utsname.h>              |others    |
|time_t time(time_t *t);                                                                                                                 |#include <time.h>                     |others    |
|char *ctime(const time_t *timep);                                                                                                       |#include <time.h>                     |others    |
|int nanosleep(const struct timespec *req, struct timespec *rem);                                                                        |#include <time.h>                     |others    |
|struct passwd *getpwuid(uid_t uid);
int getpwuid_r(uid_t uid, struct passwd *pwd, char *buffer, size_t bufsize, struct passwd **result);|#include <pwd.h>                      |permission|
|struct spwd *getspnam(const char *name);                                                                                                |#include <shadow.h>                   |permission|
|struct spwd *getspent(void);                                                                                                            |#include <shadow.h>                   |permission|
|int chmod(const char *pathname, mode_t mode);                                                                                           |#include <sys/stat.h>                 |permission|
|int fchmod(int fd, mode_t mode);                                                                                                        |#include <sys/stat.h>                 |permission|
|struct passwd *getpwnam(const char *name);                                                                                              |#include <sys/types.h> <pwd.h>        |permission|
|mode_t umask(mode_t mask);                                                                                                              |#include <sys/types.h> <sys/stat.h>   |permission|
|int access(const char *pathname, int mode);                                                                                             |#include <unistd.h>                   |permission|
|int chown(const char *pathname, uid_t owner, gid_t group);                                                                              |#include <unistd.h>                   |permission|
|char *getlogin(void);                                                                                                                   |#include <unistd.h>                   |permission|
|uid_t getuid(void);                                                                                                                     |#include <unistd.h> <sys/types.h>     |permission|
|int setuid(uid_t uid);                                                                                                                  |#include <unistd.h> <sys/types.h>     |permission|
|int setgid(gid_t gid);                                                                                                                  |#include <unistd.h> <sys/types.h>     |permission|
|typedef void (*sighandler_t)(int);                                                                                                      |#include <signal.h>                   |process   |
|int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);                                                                        |#include <signal.h>                   |process   |
|int system(const char *command);                                                                                                        |#include <stdlib.h>                   |process   |
|void exit(int status);                                                                                                                  |#include <stdlib.h>                   |process   |
|int getrlimit(int resource, struct rlimit *rlim);                                                                                       |#include <sys/time.h> <sys/resource.h>|process   |
|int setrlimit(int resource, const struct rlimit *rlim)                                                                                  |#include <sys/time.h> <sys/resource.h>|process   |
|int kill(pid_t pid, int sig);                                                                                                           |#include <sys/types.h> <signal.h>     |process   |
|pid_t wait(int *wstatus);                                                                                                               |#include <sys/types.h> <sys/wait.h>   |process   |
|pid_t waitpid(pid_t pid, int *wstatus, int options);                                                                                    |#include <sys/types.h> <sys/wait.h>   |process   |
|pid_t fork(void);                                                                                                                       |#include <sys/types.h> <unistd.h>     |process   |
|int execl(const char *pathname, const char *arg, .../* (char  *) NULL */);                                                              |#include <unistd.h>                   |process   |
|int execlp(const char *file, const char *arg, ... /* (char  *) NULL */);                                                                |#include <unistd.h>                   |process   |
|int execle(const char *pathname, const char *arg, ...  /*, (char *) NULL, char * const envp[] */);                                      |#include <unistd.h>                   |process   |
|int execv(const char *pathname, char *const argv[]);                                                                                    |#include <unistd.h>                   |process   |
|int execvp(const char *file, char *const argv[]);                                                                                       |#include <unistd.h>                   |process   |
|int execvpe(const char *file, char *const argv[], char *const envp[]);                                                                  |#include <unistd.h>                   |process   |
|int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine) (void *), void *arg)                           |#include <pthread.h>                  |thread    |
|void pthread_exit(void *retval);                                                                                                        |#include <pthread.h>                  |thread    |
|int pthread_join(pthread_t thread, void **retval);                                                                                      |#include <pthread.h>                  |thread    |
