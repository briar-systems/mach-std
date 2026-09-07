#include <sys/event.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/types.h>
#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

_Static_assert(_Generic(&kqueue, int (*)(void): 1, default: 0), "kqueue signature");
_Static_assert(_Generic(&kevent, int (*)(int, const struct kevent *, int, struct kevent *, int, const struct timespec *): 1, default: 0), "kevent signature");
_Static_assert(sizeof(int) == 4 && sizeof(intptr_t) == 8 && sizeof(uintptr_t) == 8, "LP64 widths");
_Static_assert(sizeof(struct kevent) == 32 && _Alignof(struct kevent) == 4, "native record extent");
_Static_assert(offsetof(struct kevent, ident) == 0 && offsetof(struct kevent, filter) == 8 && offsetof(struct kevent, flags) == 10 && offsetof(struct kevent, fflags) == 12 && offsetof(struct kevent, data) == 16 && offsetof(struct kevent, udata) == 24, "native record fields");
_Static_assert(sizeof(struct timespec) == 16 && offsetof(struct timespec, tv_sec) == 0 && offsetof(struct timespec, tv_nsec) == 8, "timespec fields");
_Static_assert(EVFILT_READ == -1 && EVFILT_WRITE == -2 && EVFILT_USER == -10, "filter constants");
_Static_assert(EV_ADD == 1 && EV_DELETE == 2 && EV_ONESHOT == 16 && EV_CLEAR == 32 && EV_ERROR == 0x4000 && EV_EOF == 0x8000 && NOTE_TRIGGER == 0x01000000, "event constants");
_Static_assert(AF_UNIX == 1 && SOCK_STREAM == 1 && FD_CLOEXEC == 1, "fixture constants");

static int errors(void) {
    struct kevent out = {0}, change;
    struct timespec timeout = {0};
    int r = kevent(-1, NULL, 0, &out, 1, &timeout);
    int polled = r == -1 ? -errno : 0;
    EV_SET(&change, 0, EVFILT_READ, EV_ADD | EV_ONESHOT, 0, 0, (void *)1);
    r = kevent(-1, &change, 1, NULL, 0, NULL);
    int watched = r == -1 ? -errno : 0;
    EV_SET(&change, 0, EVFILT_READ, EV_DELETE, 0, 0, NULL);
    r = kevent(-1, &change, 1, NULL, 0, NULL);
    int removed = r == -1 ? -errno : 0;
    EV_SET(&change, 1, EVFILT_USER, 0, NOTE_TRIGGER, 0, NULL);
    r = kevent(-1, &change, 1, NULL, 0, NULL);
    int woken = r == -1 ? -errno : 0;
    printf("errors poll=%d watch=%d unwatch=%d wake=%d\n", polled, watched, removed, woken);
    return polled != -EBADF || watched != -EBADF || removed != -EBADF || woken != -EBADF;
}

static int events(void) {
    int q = kqueue(), pair[2];
    struct kevent change[2], out[2];
    struct timespec timeout = {0};
    if (q == -1 || socketpair(AF_UNIX, SOCK_STREAM, 0, pair)) return 10;
    EV_SET(&change[0], pair[0], EVFILT_READ, EV_ADD | EV_ONESHOT, 0, 0, (void *)101);
    EV_SET(&change[1], pair[0], EVFILT_WRITE, EV_ADD | EV_ONESHOT, 0, 0, (void *)101);
    if (kevent(q, change, 2, NULL, 0, NULL) || write(pair[1], "x", 1) != 1) return 11;
    int n = kevent(q, NULL, 0, out, 2, &timeout), seen = 0;
    if (n != 2) return 12;
    for (int i = 0; i < n; i++) {
        if (out[i].udata != (void *)101) return 13;
        if (out[i].filter == EVFILT_READ && out[i].data >= 1) seen |= 1;
        if (out[i].filter == EVFILT_WRITE && out[i].data >= 0) seen |= 2;
    }
    if (seen != 3 || kevent(q, NULL, 0, out, 2, &timeout) != 0) return 14;
    if (close(pair[0]) || close(pair[1]) || close(q)) return 15;
    puts("native readiness and oneshot passed");
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "errors")) return errors();
    if (!strcmp(argv[1], "events")) return events();
    if (!strcmp(argv[1], "layout")) {
        printf("layout size=%zu ident=%zu filter=%zu flags=%zu fflags=%zu data=%zu udata=%zu alignment=%zu\n", sizeof(struct kevent), offsetof(struct kevent, ident), offsetof(struct kevent, filter), offsetof(struct kevent, flags), offsetof(struct kevent, fflags), offsetof(struct kevent, data), offsetof(struct kevent, udata), _Alignof(struct kevent));
        printf("timeout size=%zu sec=%zu nsec=%zu alignment=%zu\n", sizeof(struct timespec), offsetof(struct timespec, tv_sec), offsetof(struct timespec, tv_nsec), _Alignof(struct timespec));
        return 0;
    }
    return 3;
}
