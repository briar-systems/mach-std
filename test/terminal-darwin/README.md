# Darwin terminal contract probe

`verify.py` checks the darwin terminal contract against a real pseudoterminal. Run
it on a native darwin host whose architecture matches the target, once per profile:

```sh
python3 test/terminal-darwin/verify.py <mach> darwin-aarch64 debug
python3 test/terminal-darwin/verify.py <mach> darwin-aarch64 release
```

`test/lib/darwin_fixture.py` owns how a darwin fixture is built and run: std
resolves from the tree under test through `../..`, the C oracles build with the host
SDK, and a pass prints one JSON record with the compiler, the std commit and every
check result. Any failure or timeout exits nonzero with the failing check.
`test/lib/darwin-fixtures.py <mach> <target> <profile>` runs every fixture.

The verifier always supplies a PTY for terminal behavior. A separate pipe carries
phase acknowledgements, so test commands never become terminal input. The verifier
keeps the slave descriptor and compares every termios field before, during and after
raw mode. Kernel queue counts acknowledge input arrival before the child polls or
flushes it. Nonterminal behavior is a distinct run with stdin on `/dev/null`.

It checks:

- `layout.c` statically checks the typed C signatures of `tcgetattr`, `tcsetattr`
  and `tcflush`. Its termios layout and constants output must equal `terminal layout`.
- `/dev/null` rejects raw mode and flushing with the same errors as the native C
  calls in `layout.c nonterminal`. The wrappers keep those negative errno codes in
  `TermError.native`, leave raw mode inactive and permit an inactive disable. A
  closed input descriptor produces a poll error carrying `EBADF`.
- Raw mode clears only `ICANON` and `ECHO` and sets `VMIN` and `VTIME` to zero.
- Enabling with `TCSAFLUSH` removes earlier queued input.
- Polling returns an available byte and then reports an empty queue.
- Flushing removes queued input and still permits subsequent input.
- Disabling restores the complete original settings and flushes unread input.
- Repeated enable and disable calls preserve the existing state contract.
