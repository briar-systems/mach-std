[std](../../README.md) / [runtime](../README.md) / **stack**

# std.runtime.stack

the stack left on the calling thread

a reader whose recursion depth follows its input asks remaining() on each step
and refuses once it drops under a margin of its choosing, so no fixed nesting
bound or linker stack reserve has to be sized for the deepest input.

the bounds are read once per thread by std.system.os and each call is a
subtraction from the caller's frame: linux records the main thread's at entry
(the top of its mapping less the RLIMIT_STACK soft limit) and a spawned
thread's in its block, darwin records libpthread's in the block when it is
installed, and windows reads StackBase and DeallocationStack from the TEB.
the count runs to the base of the stack's reservation, including any guard
pages the OS keeps there, so the margin a caller keeps must cover those.

the bounds are unknown, and remaining() is none, where std did not record
them: under an unlimited stack rlimit on linux's main thread, and on a linux
thread std did not create or whose thread pointer a program loader owns

The directory's root module is [`std.runtime.stack`](../stack.md).

| Module | |
| :--- | :--- |
| [`tests`](tests.md) | std.runtime.stack on the main thread and on a spawned one |

