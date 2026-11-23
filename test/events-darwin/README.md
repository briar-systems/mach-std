# Darwin completion boundary probe

`verify.py` checks the darwin io queue (`kqueue`, `kevent`) behind std's
completion runtime against the host SDK. Run it on a native darwin host whose architecture matches the target, once per
profile, or run every darwin fixture with `test/lib/darwin-fixtures.py`:

```sh
python3 test/events-darwin/verify.py <mach> darwin-aarch64 debug
python3 test/events-darwin/verify.py <mach> darwin-aarch64 release
```

- `native.c` statically checks the SDK's `kqueue` and `kevent` signatures, the
  filter and flag constants and the `struct kevent` and `timespec` layouts.
- `events layout` must print the SDK's extent and offsets. Mach's record is aligned
  more strictly than Apple's packed four bytes, so alignment is not compared.
- `events errors` drives every queue operation on a closed queue: each returns the
  `EBADF` `native.c errors` prints and leaves the output untouched, and nil output,
  zero and oversized capacities and empty interest are `EINVAL`.
- `events nil` requires every operation on a nil queue to be `EINVAL`.
- `events events` covers simultaneous read and write readiness with distinct
  contexts, one-shot consumption, rearming, deletion, end of stream, wake, a
  zero-count poll, `FD_CLOEXEC` on the queue and the descriptor count after close.
- `events handshake` blocks a poll with no timeout and has a thread wake it once
  the verifier writes to its stdin.

std's async tests exercise the same backend through its callers under
`mach test . --all` on darwin.
