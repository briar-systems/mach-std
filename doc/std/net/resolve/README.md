[std](../../README.md) / [net](../README.md) / **resolve**

# std.net.resolve

bounded asynchronous system name resolution

every lookup runs under a cancellation scope and keeps one contract on every
platform: when the scope ends, the lookup returns within shared.POLL_MSEC
(10 ms) with the scope's reason, and holds nothing of the caller's
afterwards. what the system is still doing for it is the backend's business
and never reaches the caller. linux asks its nameservers itself and bounds
every wait by the poll, the TCP retry's connect included. windows runs
GetAddrInfoExW asynchronously into a request the library owns and asks
GetAddrInfoExCancel to end it. darwin runs getaddrinfo, which nothing can
interrupt, on a helper thread that owns the request and frees it when the
system lets it finish. an operation here hands its backend a scope of its
own, which the caller's scope, a token cancellation, the runtime and the
deadline all end

The directory's root module is [`std.net.resolve`](../resolve.md).

| Module | |
| :--- | :--- |
| [`conf`](conf.md) | resolv.conf resolver policy |
| [`darwin`](darwin.md) | darwin libsystem resolver adapter |
| [`hosts`](hosts.md) | hosts-file name lookup |
| [`lines`](lines.md) | bounded line iteration over resolver configuration files |
| [`linux`](linux.md) | linux native resolver adapter |
| [`lookup`](lookup.md) | DNS lookup over the target's configured nameservers |
| [`order`](order.md) | RFC 6724 destination address ordering |
| [`service`](service.md) | service name to port resolution |
| [`shared`](shared.md) | target resolver result ownership helpers |
| [`types`](types.md) | portable asynchronous resolver types |
| [`windows`](windows.md) | windows winsock system resolver adapter |
| [`wire`](wire.md) | DNS message encoding and decoding (RFC 1035) |

