#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <unistd.h>

#define CHECK(name, type) \
    _Static_assert(_Generic(&name, type: 1, default: 0), #name " signature"); \
    __typeof__(&name) sdk_##name = &name

CHECK(mmap, void *(*)(void *, size_t, int, int, int, off_t));
CHECK(munmap, int (*)(void *, size_t));
CHECK(mprotect, int (*)(void *, size_t, int));
CHECK(mlock, int (*)(const void *, size_t));
CHECK(munlock, int (*)(const void *, size_t));
CHECK(madvise, int (*)(void *, size_t, int));
CHECK(msync, int (*)(void *, size_t, int));

_Static_assert(sizeof(size_t) == 8 && sizeof(off_t) == 8 && sizeof(int) == 4, "LP64 VM widths");
_Static_assert((off_t)-1 < 0 && MAP_FAILED == (void *)-1, "native offset and failure sentinel");
_Static_assert(PROT_NONE == 0 && PROT_READ == 1 && PROT_WRITE == 2, "protection flags");
_Static_assert(MAP_SHARED == 1 && MAP_PRIVATE == 2 && MAP_ANON == 0x1000, "mapping flags");
_Static_assert(MS_SYNC == 0x10 && MADV_NORMAL == 0, "sync and advice flags");

static long result(int code) { return code == -1 ? -(long)errno : code; }

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "layout")) {
        printf("%zu %zu %zu %zu\n", sizeof(size_t), sizeof(off_t), sizeof(int), sizeof(void *));
        return 0;
    }
    long page = sysconf(_SC_PAGESIZE);
    if (page <= 0) return 3;
    unsigned char *data = mmap(NULL, (size_t)page, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    if (data == MAP_FAILED) return 4;
    if (!strcmp(argv[1], "errors")) {
        long protect = result(mprotect((void *)1, (size_t)page, PROT_READ));
        long unmap = result(munmap((void *)1, (size_t)page));
        long lock = result(mlock(data, SIZE_MAX - (size_t)page));
        long unlock = result(munlock(data, SIZE_MAX - (size_t)page));
        long advice = result(madvise(data, (size_t)page, -1));
        long sync = result(msync((void *)1, (size_t)page, MS_SYNC));
        printf("errors protect=%ld unmap=%ld lock=%ld unlock=%ld advice=%ld sync=%ld\n", protect, unmap, lock, unlock, advice, sync);
        if (munmap(data, (size_t)page)) return 5;
        return protect < 0 && unmap < 0 && lock < 0 && unlock < 0 && advice < 0 && sync < 0 ? 0 : 6;
    }
    if (!strcmp(argv[1], "released")) {
        if (mprotect(data, (size_t)page, PROT_READ)) return 12;
        if (munmap(data, (size_t)page)) return 13;
        long released = result(mprotect(data, (size_t)page, PROT_READ));
        printf("released protect=%ld\n", released);
        return released < 0 ? 0 : 14;
    }
    if (!strcmp(argv[1], "access")) {
        long lock = result(mlock(data, (size_t)page));
        long unlock = result(munlock(data, (size_t)page));
        long advice = result(madvise(data, (size_t)page, MADV_NORMAL));
        printf("access lock=%ld unlock=%ld advice=%ld\n", lock, unlock, advice);
        if (munmap(data, (size_t)page)) return 7;
        return lock == 0 && unlock == 0 && advice == 0 ? 0 : 8;
    }
    if (!strcmp(argv[1], "denied")) {
        if (mprotect(data, (size_t)page, PROT_READ)) return 9;
        if (write(1, "fault-ready\n", 12) != 12) return 10;
        *(volatile unsigned char *)data = 99;
        return 43;
    }
    munmap(data, (size_t)page);
    return 11;
}
