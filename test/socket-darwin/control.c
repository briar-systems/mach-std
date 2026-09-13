#include <fcntl.h>
#include <stdio.h>
#include <sys/socket.h>
#include <sys/uio.h>
#include <unistd.h>

static int count_fds(void) {
    int limit = getdtablesize();
    if (limit <= 0) return -1;
    int count = 0;
    for (int fd = 0; fd < limit; ++fd) {
        if (fcntl(fd, F_GETFD) >= 0) ++count;
    }
    return count;
}

int main(void) {
    int pair[2];
    if (socketpair(AF_UNIX, SOCK_DGRAM, 0, pair)) return 1;
    struct iovec data = { .iov_base = "abcdefg", .iov_len = 7 };
    struct msghdr send = { .msg_iov = &data, .msg_iovlen = 1 };
    int before = count_fds();
    if (sendmsg(pair[0], &send, 0) != 7) return 3;
    char byte;
    data.iov_base = &byte;
    data.iov_len = 1;
    struct msghdr receive = { .msg_iov = &data, .msg_iovlen = 1 };
    ssize_t count = recvmsg(pair[1], &receive, 0);
    int after = count_fds();
    printf("ignored-control count=%zd flags=%d length=%u fd-delta=%d\n", count, receive.msg_flags, receive.msg_controllen, after - before);
    int bad = count != 1 || byte != 'a' || before < 0 || before != after;
    close(pair[0]); close(pair[1]);
    return bad ? 4 : 0;
}
