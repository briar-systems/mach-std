# Darwin socket boundary probe

`verify.py` checks the darwin socket boundary against the host SDK. Run it on a
native darwin host whose architecture matches the target, once per profile:

```sh
python3 test/socket-darwin/verify.py <mach> darwin-aarch64 debug
python3 test/socket-darwin/verify.py <mach> darwin-aarch64 release
```

`test/lib/darwin_fixture.py` owns how a darwin fixture is built and run: std
resolves from the tree under test through `../..`, the C oracles build with the host
SDK, and a pass prints one JSON record with the compiler, the std commit and every
check result. Any failure or timeout exits nonzero with the failing check.
Before each build it starts a compiler, holds it stopped and requires the compiler
census to report that process by PID, then stops it by that PID.
`test/lib/darwin-fixtures.py <mach> <target> <profile>` runs every fixture that owns
a `verify.py` and declares the target in its `mach.toml`.

The verifier checks:

- `layout.c` statically checks every public socket function signature it declares
  with `CHECK`, the control header ABI and the message flags. Its record layout
  output must equal `socket layout`.
- Each `CHECK` function binds exactly one symbol in the C object, and the Mach image
  imports that same spelling, so an SDK alias is caught.
- `errors` and `datagrams` exit zero and print nothing. `errors` covers invalid
  descriptors and out-of-range lengths. `datagrams` checks explicit destination and
  returned source lengths over local UDP with receive timeouts.
- `stream` prints the SO_KEEPALIVE value and length it read, which must equal what
  `layout.c option` reads natively. An enabled option need only be nonzero. The mode
  itself checks accepted flags, endpoint agreement, would-block and shutdown EOF.
- `vectors` saturates a bounded local socket buffer, compares every received byte
  and prints a positive partial count.
- `messages` checks scatter/gather, transferred descriptor ownership and payload
  truncation, then receives a plain datagram with a nil control buffer. Its count,
  flags, control length and descriptor delta must equal `control.c` on the same
  host. A nil control buffer requests no ancillary output, so `MSG_CTRUNC` is not
  required.
- `local-bytes`, `local-async` and `internet-async-capability` check the byte-only
  local contract and must print exactly their expected line. `local-bytes` reads a
  clean prefix, then refuses eight queued rights messages with an unchanged
  descriptor count and releases every queued pipe writer on close. `local-async`
  completes a read as unsupported with zero bytes, then closes. The internet backend
  refuses a local handle before claiming a token or slot, keeps EBADF for an invalid
  handle, and leaves the refused handle usable.

The fixture counts its own descriptors. Production never does. Darwin can install
an unreported descriptor when `SCM_RIGHTS` arrives with a nil control pointer, so
this raw boundary does not promise safe descriptor discard. The rights-transfer
case supplies a sufficient control buffer and closes what it receives.

The controls prove the verifier can fail on the paths it guards. Each builds a copy of
the std tree under test in a fresh directory with one source construct changed, named
in `verify.py` by its text. A construct that is not found exactly once fails the
verifier. Production source carries no injection hooks.

- `create-refusal` and `accept-refusal` exit 110 and 44 against the honest build. In a
  copy whose flag configuration returns EIO they pass: the output is the invalid
  sentinel and the descriptor count is unchanged. Removing only the cleanup close
  from the creation path makes `create-refusal` exit 111, and from the accept path
  makes `accept-refusal` exit 45, the descriptor leak.
- In a copy with the `MSG_PEEK` removed from the local receive, `local-bytes` exits 127.
  The receive consumes the queued rights with the clean prefix, so the prefix read is
  refused and the descriptors are no longer owned by the queue.

std's own socket, TCP, UDP and async tests run through `test/native/verify.sh` and
`mach test . --all` on darwin.
