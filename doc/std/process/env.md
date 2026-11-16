[std](../README.md) / [process](README.md) / **env**

# std.process.env

environment variable access

Source: [`src/process/env.mach`](../../../src/process/env.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`EnvError`](#enverror) | `tag` | why an environment read failed |
| [`Listed`](#listed) | `tag` | one entry of the UTF-8 environment listing, mirroring std.filesystem's Listed |

| On `EnvError` | |
| :--- | :--- |
| [`compare_names`](#compare_names) | compare complete variable names in UTF-8, returning -1, 0, or 1 |
| [`compare_names_native`](#compare_names_native) | compare complete variable names in native units as given, returning -1, 0, or 1, the one order every name comparison runs |
| [`get`](#get) | read an environment variable into a buffer |
| [`get_native`](#get_native) | get in the host's native units: name and value are std.runtime.native units and cap and the length count units, so a value with no UTF-8 spelling, which get refuses, is read as it is |
| [`value`](#value) | read an environment variable into a freshly allocated string |
| [`current_dir`](#current_dir) | read the current working directory into a freshly allocated string |
| [`environ`](#environ) | the environment in UTF-8, one projection of environ_native |

| On `Listed` | |
| :--- | :--- |
| [`environ_dnit`](#environ_dnit) | release a listing environ returned: every entry, then the vector |

| Functions | |
| :--- | :--- |
| [`environ_native`](#environ_native) | the environment in native units, the one capture: at startup on linux and darwin, at first use on windows, where hidden drive-current-directory entries are left out (see std.system.os.environ_native) |

---

## EnvError

```mach
pub tag EnvError: u8 {
    native: i64;
    alloc:  std.allocator.Error;
    changed;
    unavailable;
}
```

why an environment read failed

| Case | Payload | |
| :--- | :--- | :--- |
| `native` | `i64` | the platform refused the read; the negative errno |
| `alloc` | `std.allocator.Error` | the owned copy could not be acquired |
| `changed` |  | the variable changed between the probe and the exact read |
| `unavailable` |  | there is no environment capture to list, before runtime init or when windows cannot read its block |

### compare_names

```mach
pub fun compare_names(left: str, right: str) res[i32, EnvError]
```

compare complete variable names in UTF-8, returning -1, 0, or 1

each name is converted once into native units and compared by
compare_names_native, so the two forms order every pair alike. a nil name is
empty. on windows a name that is not UTF-8 or too long to convert, or a
refused allocation, is the native error

### compare_names_native

```mach
pub fun compare_names_native(left: *Unit, left_length: usize, right: *Unit, right_length: usize) res[i32, EnvError]
```

compare complete variable names in native units as given, returning -1, 0,
or 1, the one order every name comparison runs

linux and darwin compare bytes, a shorter name first when it prefixes the
other. windows compares UTF-16 units with the operating system's ordinal
case table, case ignored and nothing converted, so a name holding unpaired
surrogates compares like any other

| Parameter | |
| :--- | :--- |
| `left` | the left name in std.runtime.native units, not terminated |
| `left_length` | its length in units, any pointer when zero |
| `right` | the right name in std.runtime.native units, not terminated |
| `right_length` | its length in units, any pointer when zero |
| **returns** | the order, or the native E2BIG for a length past the platform limit: the i32 maximum on windows, the isize maximum elsewhere |

### get

```mach
pub fun get(name: str, buf: *u8, cap: usize) res[opt[usize], EnvError]
```

read an environment variable into a buffer

when the value fits (length \< cap) it is copied and null-terminated.
the full value length is always reported, so length >= cap signals
truncation (buffer contents unspecified) and length + 1 is the capacity
to retry with. an unset variable is absence, not a failure.

| Parameter | |
| :--- | :--- |
| `name` | variable name |
| `buf` | destination buffer |
| `cap` | buffer capacity in bytes |
| **returns** | the full length of the value excluding the terminator, absent when the variable is unset, or the native failure |

### get_native

```mach
pub fun get_native(name: *Unit, buf: *Unit, cap: usize) res[opt[usize], EnvError]
```

get in the host's native units: name and value are std.runtime.native units
and cap and the length count units, so a value with no UTF-8 spelling, which
get refuses, is read as it is. linux and darwin units are bytes, so there the
two are one read

| Parameter | |
| :--- | :--- |
| `name` | nul-terminated variable name in native units |
| `buf` | destination buffer |
| `cap` | buffer capacity in units |
| **returns** | the full length of the value in units excluding the terminator, absent when the variable is unset, or the native failure |

### value

```mach
pub fun value(a: *std.allocator.Allocator, name: str) res[opt[OwnedString], EnvError]
```

read an environment variable into a freshly allocated string

probes with a small stack buffer and retries once with an exact allocation
when the value is larger, so the common case costs one read and values of
any length resolve correctly. the retry is bounded: a variable that is
unset or longer at the second read is reported as `changed` rather than
read a third time.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| `name` | variable name |
| **returns** | the owned value (extent is the length plus the terminator), absent when the variable is unset, or the failure |

### current_dir

```mach
pub fun current_dir(a: *std.allocator.Allocator) res[OwnedString, EnvError]
```

read the current working directory into a freshly allocated string

probes with a stack buffer and retries once with an exact allocation when
the path is longer; a path that grew again between the reads is `changed`.

| Parameter | |
| :--- | :--- |
| `a` | allocator for the result |
| **returns** | the owned working directory path, or the native or allocation failure |

### environ

```mach
pub fun environ(a: *std.allocator.Allocator) res[Vector[Listed], EnvError]
```

the environment in UTF-8, one projection of environ_native

for reading and editing variables. it is not for passing the environment on:
std.process.exec.Environment.inherit hands a child this process's own,
unconverted. every entry of the capture is listed, in its order. on windows
an entry with no UTF-8 spelling is listed in place as unspellable with its
native name, never dropped and never failing the listing. linux and darwin
entries are bytes and are listed as given. the vector, every variable and
every native name are owned by the caller and released with environ_dnit

| Parameter | |
| :--- | :--- |
| `a` | allocator for the vector and every entry |
| **returns** | the entries in order, or why they could not be listed, with nothing left allocated |

## Listed

```mach
pub tag Listed: u8 {
    variable:    str;
    unspellable: NativeName;
}
```

one entry of the UTF-8 environment listing, mirroring std.filesystem's Listed

| Case | Payload | |
| :--- | :--- | :--- |
| `variable` | `str` | the entry as NAME=value in UTF-8 |
| `unspellable` | `NativeName` | an entry with no UTF-8 spelling, which only windows can hold, as its variable name in native units, which get_native reads |

### environ_dnit

```mach
pub fun environ_dnit(listed: *Vector[Listed])
```

release a listing environ returned: every entry, then the vector

## Functions

### environ_native

```mach
pub fun environ_native() **Unit
```

the environment in native units, the one capture: at startup on linux and
darwin, at first use on windows, where hidden drive-current-directory entries
are left out (see std.system.os.environ_native)

| Parameter | |
| :--- | :--- |
| **returns** | nil-terminated array of nul-terminated NAME=value entries in std.runtime.native units, kept for the life of the process, or nil when the environment is unavailable (e.g. before runtime init) |

