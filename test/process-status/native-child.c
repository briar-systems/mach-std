#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <windows.h>
#else
#include <signal.h>
#include <unistd.h>
#endif

int main(int argc, char **argv) {
    if (argc != 2) return 98;
#ifndef _WIN32
    if (strcmp(argv[1], "signal") == 0) {
        if (raise(SIGTERM) != 0) return 97;
        return 96;
    }
    if (strcmp(argv[1], "stop") == 0) {
        if (raise(SIGSTOP) != 0) return 95;
        for (;;) pause();
    }
#endif
    char *end = NULL;
    unsigned long long parsed = strtoull(argv[1], &end, 0);
    if (!end || *end || parsed > UINT32_MAX) return 94;
#ifdef _WIN32
    ExitProcess((UINT)parsed);
#else
    _exit((int)(parsed & 255));
#endif
}
