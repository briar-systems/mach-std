#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char **argv) {
    char root[] = "/tmp/mach-qemu-mode-XXXXXX";
    if (!mkdtemp(root)) return 10;
    int fd = open(root, O_RDONLY | O_DIRECTORY | O_CLOEXEC);
    if (fd < 0 || mkdirat(fd, "child", 0000) != 0) return 11;
    errno = 0;
    long result = syscall(452, fd, "child", 0700, AT_SYMLINK_NOFOLLOW);
    int saved = errno;
    struct stat metadata;
    if (fstatat(fd, "child", &metadata, AT_SYMLINK_NOFOLLOW)) return 12;
    printf("directory result=%ld errno=%d mode=%o\n", result, saved, metadata.st_mode & 0777);
    int expect_missing = argc == 2 && strcmp(argv[1], "enosys") == 0;
    if (expect_missing) {
        if (result != -1 || saved != ENOSYS || (metadata.st_mode & 0777) != 0) return 20;
    } else {
        if (result != 0 || (metadata.st_mode & 0777) != 0700) return 21;
        if (symlinkat("child", fd, "link")) return 22;
        errno = 0;
        result = syscall(452, fd, "link", 0777, AT_SYMLINK_NOFOLLOW);
        saved = errno;
        if (fstatat(fd, "child", &metadata, AT_SYMLINK_NOFOLLOW)) return 23;
        printf("symlink result=%ld errno=%d target-mode=%o\n", result, saved, metadata.st_mode & 0777);
        if (result != -1 || saved != EOPNOTSUPP || (metadata.st_mode & 0777) != 0700) return 24;
        if (unlinkat(fd, "link", 0)) return 25;
    }
    if (unlinkat(fd, "child", AT_REMOVEDIR) || close(fd) || rmdir(root)) return 26;
    return 0;
}
