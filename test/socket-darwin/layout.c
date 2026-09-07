#include <stddef.h>
#include <stdio.h>
#include <sys/socket.h>
#include <sys/uio.h>
#include <unistd.h>

#define CHECK(name, type) \
    _Static_assert(_Generic(&name, type: 1, default: 0), #name " signature"); \
    __typeof__(&name) sdk_##name = &name

CHECK(socketpair, int (*)(int, int, int, int *));
CHECK(getdtablesize, int (*)(void));
CHECK(socket, int (*)(int, int, int));
CHECK(bind, int (*)(int, const struct sockaddr *, socklen_t));
CHECK(listen, int (*)(int, int));
CHECK(accept, int (*)(int, struct sockaddr *, socklen_t *));
CHECK(connect, int (*)(int, const struct sockaddr *, socklen_t));
CHECK(sendto, ssize_t (*)(int, const void *, size_t, int, const struct sockaddr *, socklen_t));
CHECK(recvfrom, ssize_t (*)(int, void *, size_t, int, struct sockaddr *, socklen_t *));
CHECK(shutdown, int (*)(int, int));
CHECK(setsockopt, int (*)(int, int, int, const void *, socklen_t));
CHECK(getsockopt, int (*)(int, int, int, void *, socklen_t *));
CHECK(getsockname, int (*)(int, struct sockaddr *, socklen_t *));
CHECK(getpeername, int (*)(int, struct sockaddr *, socklen_t *));
CHECK(writev, ssize_t (*)(int, const struct iovec *, int));
CHECK(sendmsg, ssize_t (*)(int, const struct msghdr *, int));
CHECK(recvmsg, ssize_t (*)(int, struct msghdr *, int));

_Static_assert(SCM_RIGHTS == 1 && SOL_SOCKET == 0xffff, "rights header constants");
_Static_assert(MSG_TRUNC == 0x10 && MSG_CTRUNC == 0x20, "message truncation flags");
_Static_assert(AF_UNIX == 1, "local socket family");

int main(void) {
    printf("%zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu %zu\n",
        sizeof(struct iovec), _Alignof(struct iovec), offsetof(struct iovec, iov_base), offsetof(struct iovec, iov_len),
        sizeof(struct msghdr), _Alignof(struct msghdr), offsetof(struct msghdr, msg_name),
        offsetof(struct msghdr, msg_namelen), offsetof(struct msghdr, msg_iov), offsetof(struct msghdr, msg_iovlen),
        offsetof(struct msghdr, msg_control), offsetof(struct msghdr, msg_controllen), offsetof(struct msghdr, msg_flags),
        sizeof(socklen_t), sizeof(int), sizeof(ssize_t), (size_t)CMSG_SPACE(sizeof(int)), (size_t)CMSG_LEN(0));
    return 0;
}
