#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/sysctl.h>

_Static_assert(_Generic(&sysctlbyname, int (*)(const char *, void *, size_t *, void *, size_t): 1, default: 0), "sysctlbyname signature");
_Static_assert(sizeof(size_t) == 8 && sizeof(int) == 4, "LP64 CPU query widths");
__typeof__(&sysctlbyname) sdk_sysctlbyname = &sysctlbyname;

static long query(const char *name) {
    int count = 0;
    size_t length = sizeof(count);
    if (sysctlbyname(name, &count, &length, NULL, 0) || length != sizeof(count) || count < 1) return -1;
    return count;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "observe")) {
        long before = query("hw.activecpu");
        long middle = query("hw.activecpu");
        long after = query("hw.activecpu");
        long maximum = query("hw.ncpu");
        printf("observed before=%ld wrapper=%ld after=%ld maximum=%ld\n", before, middle, after, maximum);
        return before > 0 && middle > 0 && after > 0 && maximum > 0 ? 0 : 10;
    }
    if (!strcmp(argv[1], "errors")) {
        int count = 17;
        size_t length = sizeof(count);
        int result = sysctlbyname("mach.audit.nonexistent_cpu_key", &count, &length, NULL, 0);
        int error = errno;
        printf("error result=%d errno=%ld length=%zu count=%d\n", result, -(long)error, length, count);
        return result == -1 && error > 0 ? 0 : 11;
    }
    return 3;
}
