# Darwin terminal contract probe

This native Darwin probe requires a real pseudoterminal. A separate pipe carries
phase acknowledgements, so test commands never become terminal input. The host
retains the slave descriptor and compares every termios field before, during and
after raw mode. Kernel queue counts acknowledge input arrival before the child
polls or flushes it. Timeouts diagnose a stalled phase and never count as success.

The probe checks:

- The SDK termios layout, constants and typed C function signatures against Mach.
- `/dev/null` rejects raw mode and flushing with the same producer errors as the
  native C calls. The wrappers preserve those negative-errno messages, leave raw
  mode inactive and permit an inactive disable. A closed input descriptor produces
  a poll error.
- Raw mode clears only `ICANON` and `ECHO` and sets `VMIN` and `VTIME` to zero.
- Enabling with `TCSAFLUSH` removes earlier queued input.
- Polling returns an available byte and then reports an empty queue.
- Flushing removes queued input and still permits subsequent input.
- Disabling restores the complete original settings and flushes unread input.
- Repeated enable and disable calls preserve the existing state contract.

On each Darwin architecture, copy this fixture into an owned project directory
and snapshot the exact standard library manifest and `src` tree into `dep/std`.
Build `layout.c` with the native SDK using `xcrun clang -std=c11 -Wall -Wextra
-Werror layout.c -o layout`. Build the Mach artifact with both `debug` and
`release` profiles, explicit `-o bin/terminal`, and the matching `darwin-x86_64`
or `darwin-aarch64` target.
Then run `python3 verify.py bin/terminal ./layout` after each build. The runner
must record the exact compiler and std source, a clear compiler-process census
before every Mach build or test, and both profile results.

The host probe always supplies a PTY for terminal behavior. A missing PTY is a
failure. Nonterminal behavior is a distinct invocation with stdin connected to
`/dev/null`.
