#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <termios.h>

_Static_assert(_Generic(&tcgetattr,
    int (*)(int, struct termios *): 1, default: 0), "tcgetattr signature");
_Static_assert(_Generic(&tcsetattr,
    int (*)(int, int, const struct termios *): 1, default: 0), "tcsetattr signature");
_Static_assert(_Generic(&tcflush,
    int (*)(int, int): 1, default: 0), "tcflush signature");

int main(int argc, char **argv) {
    (void)argv;
    if (argc == 2) {
        struct termios settings;
        errno = 0;
        int got = tcgetattr(0, &settings);
        int get_error = errno;
        errno = 0;
        int dropped = tcflush(0, TCIFLUSH);
        int flush_error = errno;
        printf("%d %d %d %d\n", got, get_error, dropped, flush_error);
        return got != -1 || dropped != -1 || get_error <= 0 || flush_error <= 0;
    }
    printf("%zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %d %d %lu %lu %d %d %d\n",
        sizeof(struct termios), _Alignof(struct termios),
        offsetof(struct termios, c_iflag), offsetof(struct termios, c_oflag),
        offsetof(struct termios, c_cflag), offsetof(struct termios, c_lflag),
        offsetof(struct termios, c_cc), offsetof(struct termios, c_ispeed),
        offsetof(struct termios, c_ospeed), sizeof(((struct termios *)0)->c_cc),
        sizeof(tcflag_t), sizeof(speed_t), TCSAFLUSH, TCIFLUSH,
        (unsigned long)ICANON, (unsigned long)ECHO, VMIN, VTIME, ENOTTY);
    return 0;
}
