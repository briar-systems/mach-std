#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

_Static_assert(_Generic(&fdopendir, DIR *(*)(int): 1, default: 0), "fdopendir signature");
_Static_assert(_Generic(&readdir, struct dirent *(*)(DIR *): 1, default: 0), "readdir signature");
_Static_assert(_Generic(&closedir, int (*)(DIR *): 1, default: 0), "closedir signature");
_Static_assert(offsetof(struct dirent, d_ino) == 0 && offsetof(struct dirent, d_seekoff) == 8, "directory identity offsets");
_Static_assert(offsetof(struct dirent, d_reclen) == 16 && offsetof(struct dirent, d_namlen) == 18, "directory length offsets");
_Static_assert(offsetof(struct dirent, d_type) == 20 && offsetof(struct dirent, d_name) == 21, "directory name offset");
_Static_assert(sizeof(((struct dirent *)0)->d_reclen) == 2 && sizeof(((struct dirent *)0)->d_namlen) == 2, "directory length widths");
_Static_assert(F_DUPFD_CLOEXEC == 67 && FD_CLOEXEC == 1, "descriptor flags");

static __attribute__((used)) struct dirent *sdk_readdir(DIR *stream) {
    return readdir(stream);
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "layout")) {
        printf("layout inode=%zu seek=%zu record=%zu length=%zu type=%zu name=%zu alignment=%zu nominal=%zu\n",
            offsetof(struct dirent, d_ino), offsetof(struct dirent, d_seekoff), offsetof(struct dirent, d_reclen),
            offsetof(struct dirent, d_namlen), offsetof(struct dirent, d_type), offsetof(struct dirent, d_name),
            _Alignof(struct dirent), sizeof(((struct dirent *)0)->d_name));
        return 0;
    }
    if (!strcmp(argv[1], "errors")) {
        int fd = open("directory-native-file", O_CREAT | O_EXCL | O_RDWR, 0600);
        if (fd < 0) return 10;
        int duplicate = fcntl(fd, F_DUPFD_CLOEXEC, 0);
        if (duplicate < 0) return 11;
        errno = 0;
        DIR *stream = fdopendir(duplicate);
        int code = stream ? 0 : -errno;
        int owned = fcntl(duplicate, F_GETFD);
        int original = fcntl(fd, F_GETFD);
        if (stream) closedir(stream);
        else if (close(duplicate)) return 12;
        if (close(fd) || unlink("directory-native-file")) return 13;
        printf("errors regular=%d duplicate_owned=%d original_owned=%d\n", code, owned >= 0, original >= 0);
        return code != -ENOTDIR || owned < 0 || original < 0;
    }
    return 3;
}
