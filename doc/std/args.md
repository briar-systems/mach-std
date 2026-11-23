[std](README.md) / **args**

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

Source: [`src/args.mach`](../../src/args.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Args`](#args) | `rec` | the process arguments, borrowed from main's argc and argv |
| [`Cursor`](#cursor-1) | `rec` | an iterator over arguments |
| [`Flag`](#flag) | `rec` | one flag |
| [`Command`](#command) | `rec` | one command, a program's root or a command nested under another to any depth |
| [`Refused`](#refused) | `rec` | where a token was refused |
| [`Refusal`](#refusal) | `tag` | why parse refused the user's command line |
| [`Parsed`](#parsed) | `rec` | a command line read against a root command |
| [`Hit`](#hit) | `rec` | what one option was given |
| [`Values`](#values-1) | `rec` | a walk over one flag's occurrences, in argument order |
| [`Event`](#event) | `tag` | one step of a parsed line, in argument order |
| [`Walk`](#walk-1) | `rec` | a walk over a parsed line's operands and options in argument order, for a program whose options apply where they stand among its operands |

| On `Args` | |
| :--- | :--- |
| [`of`](#of) | view main's argc and argv |
| [`count`](#count) | the number of arguments, the program name included |
| [`get`](#get) | the argument at an index |
| [`cursor`](#cursor) | iterate arguments from an index |

| On `Cursor` | |
| :--- | :--- |
| [`next`](#next) | take the next argument |

| On `Flag` | |
| :--- | :--- |
| [`takes_value`](#takes_value) | whether a flag takes a value |

| On `Command` | |
| :--- | :--- |
| [`subcommand`](#subcommand) | the command nested under a command that a word names, by its name or one of its aliases |
| [`parse`](#parse) | read a command line against a root command |

| On `Parsed` | |
| :--- | :--- |
| [`command_at`](#command_at) | the command at a depth of the matched path |
| [`occurrences`](#occurrences) | how many times a flag occurred, under either spelling |
| [`given`](#given) | whether a flag occurred, negated or not |
| [`latest`](#latest) | the last occurrence of a flag |
| [`on`](#on) | whether a flag is on: it occurred and its last occurrence was not negated |
| [`value`](#value) | the value of a flag's last occurrence, nil when it had none or the flag did not occur |
| [`values`](#values) | walk a flag's occurrences, each as the line gave it, a negated or bare one with a nil value |
| [`walk`](#walk) | walk a parsed line |
| [`operand_count`](#operand_count) | the number of operands the line gave |
| [`operand`](#operand) | an operand, as given |
| [`rest`](#rest) | the arguments after a passthrough command's `--`, as given, empty when there are none |
| [`separator`](#separator) | the index of the `--` that ended the flags, or the argument count when none did |
| [`describe`](#describe) | write a refusal's message, the sentence a program reports it with, without a trailing newline |

| On `Values` | |
| :--- | :--- |
| [`next_value`](#next_value) | take the flag's next occurrence |

| On `Walk` | |
| :--- | :--- |
| [`step`](#step) | take the next event of a walk |

| Constants | |
| :--- | :--- |
| [`OPERANDS_ANY`](#constants) | the operand_max of a command that takes any number of operands |

---

## Args

```mach
pub rec Args {
    argc: usize;
    argv: **u8;
}
```

the process arguments, borrowed from main's argc and argv

| Field | Type | |
| :--- | :--- | :--- |
| `argc` | `usize` | number of arguments, the program name included |
| `argv` | `**u8` | the arguments, each a null-terminated string |

### of

```mach
pub fun of(argc: usize, argv: **u8) Args
```

view main's argc and argv

| Parameter | |
| :--- | :--- |
| `argc` | number of arguments |
| `argv` | the arguments |
| **returns** | the view |

### count

```mach
pub fun count(a: Args) usize
```

the number of arguments, the program name included

### get

```mach
pub fun get(a: Args, idx: usize) opt[str]
```

the argument at an index

| Parameter | |
| :--- | :--- |
| `a` | the arguments |
| `idx` | argument index, 0 the program name |
| **returns** | the argument, or none when the index is out of range |

### cursor

```mach
pub fun cursor(a: Args, start: usize) Cursor
```

iterate arguments from an index

| Parameter | |
| :--- | :--- |
| `a` | the arguments |
| `start` | index of the first argument to yield, 1 to skip the program name |
| **returns** | the cursor |

## Cursor

```mach
pub rec Cursor {
    args: Args;
    at:   usize;
}
```

an iterator over arguments

| Field | Type | |
| :--- | :--- | :--- |
| `args` | `Args` | the arguments being walked |
| `at` | `usize` | index of the next argument |

### next

```mach
pub fun next(c: *Cursor) opt[str]
```

take the next argument

| Parameter | |
| :--- | :--- |
| `c` | the cursor |
| **returns** | the argument, or none when they are exhausted |

## Flag

```mach
pub rec Flag {
    long:      str;
    short:     u8;
    value:     str;
    repeat:    bool;
    negatable: bool;
    help:      str;
}
```

one flag. a flag is its own identity: parse records the flag an option matched, and a program
asks for it by address, so one flag listed by several commands reads as one

| Field | Type | |
| :--- | :--- | :--- |
| `long` | `str` | the long spelling without its dashes, `out` for `--out`, nil for none |
| `short` | `u8` | the short spelling's byte, `o` for `-o`, 0 for none |
| `value` | `str` | the placeholder of the value the flag takes, as help prints it, nil or empty for a flag that takes none |
| `repeat` | `bool` | the flag is meant to occur more than once. parse accepts any number of occurrences of every flag, a single read answers the last, and help marks a repeating flag |
| `negatable` | `bool` | the long spelling also answers to `--no-` and the rest of it, an occurrence that reads as off and takes no value |
| `help` | `str` | one-line help text, nil or empty for none |

### takes_value

```mach
pub fun takes_value(f: *Flag) bool
```

whether a flag takes a value

## Command

```mach
pub rec Command {
    name:        str;
    aliases:     Slice[str];
    help:        str;
    usage:       str;
    flags:       Slice[*Flag];
    commands:    Slice[*Command];
    operand_min: usize;
    operand_max: usize;
    passthrough: bool;
}
```

one command, a program's root or a command nested under another to any depth

| Field | Type | |
| :--- | :--- | :--- |
| `name` | `str` | the command word. the root's is the program name refusals and help spell |
| `aliases` | `Slice[str]` | other words for the command |
| `help` | `str` | help text for the command, nil or empty for none |
| `usage` | `str` | the operand grammar help prints after the command words, nil or empty for none |
| `flags` | `Slice[*Flag]` | the flags read while the command is the one matched so far |
| `commands` | `Slice[*Command]` | the commands nested under it. a word in the operand place names one of them |
| `operand_min` | `usize` | fewest operands the command takes |
| `operand_max` | `usize` | most operands the command takes, OPERANDS_ANY for no bound |
| `passthrough` | `bool` | the arguments after `--` are neither flags nor operands but the rest, returned as given. without it they are operands |

### subcommand

```mach
pub fun subcommand(command: *Command, word: str) *Command
```

the command nested under a command that a word names, by its name or one of its aliases

| Parameter | |
| :--- | :--- |
| `command` | the command |
| `word` | a command word |
| **returns** | the nested command, or nil when none answers to the word |

### parse

```mach
pub fun parse(spec: *Command, a: Args) Parsed
```

read a command line against a root command. from argument 1 on, an option is read against the
flags of the command matched so far, and while that command has nested commands a word in the
operand place names one of them, which becomes the command matched. every other word is an
operand of the command matched, and `--` ends the flags. parse judges the user's line alone:
the commands are taken as the program wrote them

| Parameter | |
| :--- | :--- |
| `spec` | the root command, which outlives the result |
| `a` | the arguments, the program name at 0, which outlive the result |
| **returns** | the line read, its refusal none when it was read whole |

## Refused

```mach
pub rec Refused {
    idx:   usize;
    at:    usize;
    tok:   str;
    depth: usize;
}
```

where a token was refused

| Field | Type | |
| :--- | :--- | :--- |
| `idx` | `usize` | argument index of the token |
| `at` | `usize` | byte offset of the refused character in a short cluster, 0 for the whole token |
| `tok` | `str` | the token |
| `depth` | `usize` | the depth of the command the token was read against, 0 the root |

## Refusal

```mach
pub tag Refusal: u8 {
    unknown_flag:    Refused;
    missing_value:   Refused;
    unknown_command: Refused;
    operands:        usize;
}
```

why parse refused the user's command line. describe writes its message

| Case | Payload | |
| :--- | :--- | :--- |
| `unknown_flag` | `Refused` | an option names no flag of the command it was read against |
| `missing_value` | `Refused` | a flag that takes a value ends the line with no value after it |
| `unknown_command` | `Refused` | a word in a command's operand place names none of its nested commands |
| `operands` | `usize` | the matched command's operand count is outside its bounds, by the count given |

## Parsed

```mach
pub rec Parsed {
    args:    Args;
    root:    *Command;
    command: *Command;
    depth:   usize;
    sep:     usize;
    rest:    usize;
    refusal: opt[Refusal];
}
```

a command line read against a root command. it keeps no copy of the arguments, which every
query reads again, so the arguments and the commands outlive it

| Field | Type | |
| :--- | :--- | :--- |
| `args` | `Args` | the arguments, the program name at 0 |
| `root` | `*Command` | the root command |
| `command` | `*Command` | the command matched, the last of the path from the root |
| `depth` | `usize` | the number of command words matched below the root |
| `sep` | `usize` | index of the `--` that ended the flags, the argument count when none did |
| `rest` | `usize` | index of the first argument after a passthrough command's `--`, the argument count when there is none |
| `refusal` | `opt[Refusal]` | the first way the line is refused in argument order, an operand count last, none when it is read whole |

### command_at

```mach
pub fun command_at(p: *Parsed, depth: usize) *Command
```

the command at a depth of the matched path

| Parameter | |
| :--- | :--- |
| `p` | the parsed line |
| `depth` | 0 for the root, up to p.depth |
| **returns** | the command, or nil past the matched path |

### occurrences

```mach
pub fun occurrences(p: *Parsed, flag: *Flag) usize
```

how many times a flag occurred, under either spelling

### given

```mach
pub fun given(p: *Parsed, flag: *Flag) bool
```

whether a flag occurred, negated or not

### latest

```mach
pub fun latest(p: *Parsed, flag: *Flag) opt[Hit]
```

the last occurrence of a flag

| Parameter | |
| :--- | :--- |
| `p` | the parsed line |
| `flag` | the flag |
| **returns** | the occurrence, none when the flag did not occur |

### on

```mach
pub fun on(p: *Parsed, flag: *Flag) bool
```

whether a flag is on: it occurred and its last occurrence was not negated

### value

```mach
pub fun value(p: *Parsed, flag: *Flag) str
```

the value of a flag's last occurrence, nil when it had none or the flag did not occur

### values

```mach
pub fun values(p: *Parsed, flag: *Flag) Values
```

walk a flag's occurrences, each as the line gave it, a negated or bare one with a nil value

### walk

```mach
pub fun walk(p: *Parsed) Walk
```

walk a parsed line

### operand_count

```mach
pub fun operand_count(p: *Parsed) usize
```

the number of operands the line gave

### operand

```mach
pub fun operand(p: *Parsed, n: usize) opt[str]
```

an operand, as given

| Parameter | |
| :--- | :--- |
| `p` | the parsed line |
| `n` | the operand's position among the operands, 0 the first |
| **returns** | the operand, or none when there are not that many |

### rest

```mach
pub fun rest(p: *Parsed) Slice[str]
```

the arguments after a passthrough command's `--`, as given, empty when there are none

### separator

```mach
pub fun separator(p: *Parsed) usize
```

the index of the `--` that ended the flags, or the argument count when none did

### describe

```mach
pub fun describe(p: *Parsed, w: *Writer) err[WriteError]
```

write a refusal's message, the sentence a program reports it with, without a trailing newline

| Parameter | |
| :--- | :--- |
| `p` | the parsed line |
| `w` | where the message is written |
| **returns** | ok, nothing written when the line has no refusal, or the write that failed |

## Hit

```mach
pub rec Hit {
    flag:  *Flag;
    idx:   usize;
    at:    usize;
    on:    bool;
    value: str;
}
```

what one option was given

| Field | Type | |
| :--- | :--- | :--- |
| `flag` | `*Flag` | the flag the option names |
| `idx` | `usize` | argument index of the option |
| `at` | `usize` | byte offset of its character in a short cluster, 0 for a long option |
| `on` | `bool` | false only for a negated flag |
| `value` | `str` | the value given, nil when none was |

## Values

```mach
pub rec Values {
    scan: Scan;
    flag: *Flag;
}
```

a walk over one flag's occurrences, in argument order

| Field | Type | |
| :--- | :--- | :--- |
| `scan` | `Scan` | the scan of the parsed line |
| `flag` | `*Flag` | the flag walked |

### next_value

```mach
pub fun next_value(w: *Values) opt[Hit]
```

take the flag's next occurrence

| Parameter | |
| :--- | :--- |
| `w` | the walk |
| **returns** | the occurrence, or none when the flag occurs no more |

## Event

```mach
pub tag Event: u8 {
    done;
    operand: usize;
    hit:     Hit;
}
```

one step of a parsed line, in argument order

| Case | Payload | |
| :--- | :--- | :--- |
| `done` |  | no arguments remain |
| `operand` | `usize` | an operand, by argument index |
| `hit` | `Hit` | an option, a flag that takes a value with nothing after it giving a nil value |

## Walk

```mach
pub rec Walk {
    scan: Scan;
}
```

a walk over a parsed line's operands and options in argument order, for a program whose options
apply where they stand among its operands. command words and refused tokens are skipped

### step

```mach
pub fun step(w: *Walk) Event
```

take the next event of a walk

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `OPERANDS_ANY` | `usize` | `0xffffffff` | the operand_max of a command that takes any number of operands |

