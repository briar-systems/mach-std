#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/random.h>

_Static_assert(_Generic(&getentropy, int (*)(void *, size_t): 1, default: 0), "getentropy signature");
_Static_assert(sizeof(size_t) == 8 && sizeof(int) == 4, "LP64 entropy widths");
__typeof__(&getentropy) sdk_getentropy = &getentropy;

static long result(int code) { return code == -1 ? -(long)errno : code; }

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "errors")) {
        unsigned char storage[257];
        memset(storage, 0xA5, sizeof(storage));
        long oversized = result(getentropy(storage, sizeof(storage)));
        long invalid = result(getentropy((void *)1, 1));
        long wrapper = result(getentropy((void *)1, 1));
        printf("errors oversized=%ld invalid=%ld wrapper=%ld\n", oversized, invalid, wrapper);
        if (oversized >= 0 || invalid >= 0 || wrapper != invalid) return 13;
        for (size_t i = 0; i < sizeof(storage); ++i) if (storage[i] != 0xA5) return 14;
        return 0;
    }
    if (!strcmp(argv[1], "smoke")) {
        const size_t sizes[] = {0, 1, 255, 256, 257, 512, 1025};
        for (size_t n = 0; n < sizeof(sizes) / sizeof(sizes[0]); ++n) {
            unsigned char storage[1027];
            memset(storage, 0xA5, sizeof(storage));
            size_t filled = 0;
            while (filled < sizes[n]) {
                size_t chunk = sizes[n] - filled;
                if (chunk > 256) chunk = 256;
                if (getentropy(storage + 1 + filled, chunk)) return 10;
                filled += chunk;
            }
            if (storage[0] != 0xA5) return 11;
            for (size_t i = sizes[n] + 1; i < sizeof(storage); ++i) if (storage[i] != 0xA5) return 11;
        }
        puts("smoke spans=7 guards=exact");
        return 0;
    }
    return 3;
}
