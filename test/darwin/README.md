# Darwin runtime and process probe

`verify.sh` builds `darwin_probe` against this checkout's std in both profiles
and observes it from outside the process: the exit status the kernel reports
for a `main` return, `os.exit`, `os.abort` (a SIGABRT death) and a panic
(255, with the message on stderr and nothing on stdout); the argument and
environment blocks the entry captured, printed back by the `args` subcommand;
and, through the `child` subcommand, the same contracts observed by a parent
that spawned the probe through the OS layer with `wait4`, a `dup2`-redirected
stdout pipe, an `execve` of a missing program (127), a `chdir` into a missing
directory (126) and a wait on a foreign pid (ECHILD).

It executes natively only: on a macos host, `verify.sh <mach> darwin-aarch64`
or `verify.sh <mach> darwin-x86_64` on the matching architecture. From any
other host, `verify.sh <mach> <darwin-target> --build-only` cross-builds both
profiles without running anything.
