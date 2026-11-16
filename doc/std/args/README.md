[std](../README.md) / **args**

# std.args

command-line arguments as views, and a parser that reads them against declared commands

the process arguments are the argc and argv std.runtime hands main. this
module borrows them and allocates nothing. on windows the runtime splits the
wide command line by the post-2008 msvcrt rules and converts each argument to
UTF-8, so a program reads the same argv bytes on every host. an unpaired
surrogate, which a windows argument may hold, arrives as U+FFFD, one per code
unit, so such an argument does not round-trip to the native name. the
arguments as the host passed them, UTF-16 on windows and bytes elsewhere, are
in std.runtime.native.

a program describes its command line as data: a root Command, Commands nested
under it to any depth, and the Flags each one reads. parse reads the arguments
against the root into a Parsed, which records the command path matched and the
first refusal of the user's input. it keeps no copy of what it read: every
query reads the arguments again, so the parser needs no storage from the
caller. parse judges the user's line alone, never the description, and imposes
no shape on a program's command line: a program declares its own `--help`,
`--version` and exit codes, and decides what a refusal costs.

a flag is spelled long, `--name`, short, `-c` with one byte, or both. a long
flag that takes a value reads `--name value` or `--name=value`, and a
negatable one also answers to `--no-name`, which reads as off. a token with
one dash is a cluster of short spellings read left to right: a flag that takes
no value is one occurrence and reading goes on, a flag that takes a value ends
the cluster and the rest of the token, verbatim, is its value, so `-o=x` gives
`=x` and `-vv` is two occurrences of `-v`. a short flag that takes a value
with nothing left takes the next argument. a lone `-` is an operand, and `--`
ends the flags: the arguments after it are operands, or the rest of a
passthrough command, returned as given. std.args.help renders a neutral page
from the same records for a program that wants one.

The directory's root module is [`std.args`](../args.md).

| Module | |
| :--- | :--- |
| [`help`](help.md) | a neutral help page rendered from the records std.args reads a command line against |

