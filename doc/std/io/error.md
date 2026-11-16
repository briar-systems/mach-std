[std](../README.md) / [io](README.md) / **error**

# std.io.error

normalized I/O errors with target detail and operation context

this module is portable. translating a native code into an Error belongs to
the OS layer (std.system.os.error)

Source: [`src/io/error.mach`](../../../src/io/error.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Kind`](#kind) | `def` |  |
| [`Operation`](#operation) | `def` |  |
| [`Error`](#error) | `rec` |  |

| On `Kind` | |
| :--- | :--- |
| [`INTERRUPTED`](#kind), [`WOULD_BLOCK`](#kind), [`TIMEOUT`](#kind), [`CANCELLED`](#kind), [`REFUSED`](#kind), [`RESET`](#kind), [`ABORTED`](#kind), [`CLOSED`](#kind), [`ADDRESS_IN_USE`](#kind), [`UNREACHABLE`](#kind), [`PERMISSION`](#kind), [`RESOURCE_EXHAUSTED`](#kind), [`INVALID`](#kind), [`UNSUPPORTED`](#kind), [`OTHER`](#kind), [`NOT_FOUND`](#kind), [`EXISTS`](#kind), [`NOT_DIRECTORY`](#kind), [`IS_DIRECTORY`](#kind), [`NOT_EMPTY`](#kind), [`NAME_TOO_LONG`](#kind), [`BUSY`](#kind), [`IO`](#kind), [`RANGE`](#kind), [`NO_CHILD`](#kind), [`LOOP`](#kind) | |
| [`make`](#make) | an error std raised itself, with no native code behind it |
| [`kind_name`](#kind_name) | the name of a kind, for messages about an error with no native code |

| On `Operation` | |
| :--- | :--- |
| [`OP_UNKNOWN`](#operation), [`OP_OPEN`](#operation), [`OP_CLOSE`](#operation), [`OP_READ`](#operation), [`OP_WRITE`](#operation), [`OP_CREATE`](#operation), [`OP_BIND`](#operation), [`OP_LISTEN`](#operation), [`OP_ACCEPT`](#operation), [`OP_CONNECT`](#operation), [`OP_RECEIVE`](#operation), [`OP_SEND`](#operation), [`OP_SHUTDOWN`](#operation), [`OP_OPTION`](#operation), [`OP_SEEK`](#operation), [`OP_SYNC`](#operation), [`OP_SUBMIT`](#operation), [`OP_WAIT`](#operation), [`OP_WAKE`](#operation) | |
| [`OP_LOCK`](#operation) | pinning memory resident, refused when the host will not lock it |

| On `Error` | |
| :--- | :--- |
| [`retryable`](#retryable) | |

---

## Kind

```mach
pub def Kind: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `INTERRUPTED` | `0` |  |
| `WOULD_BLOCK` | `1` |  |
| `TIMEOUT` | `2` |  |
| `CANCELLED` | `3` |  |
| `REFUSED` | `4` |  |
| `RESET` | `5` |  |
| `ABORTED` | `6` |  |
| `CLOSED` | `7` |  |
| `ADDRESS_IN_USE` | `8` |  |
| `UNREACHABLE` | `9` |  |
| `PERMISSION` | `10` |  |
| `RESOURCE_EXHAUSTED` | `11` |  |
| `INVALID` | `12` |  |
| `UNSUPPORTED` | `13` |  |
| `OTHER` | `14` |  |
| `NOT_FOUND` | `15` |  |
| `EXISTS` | `16` |  |
| `NOT_DIRECTORY` | `17` |  |
| `IS_DIRECTORY` | `18` |  |
| `NOT_EMPTY` | `19` |  |
| `NAME_TOO_LONG` | `20` |  |
| `BUSY` | `21` |  |
| `IO` | `22` |  |
| `RANGE` | `23` |  |
| `NO_CHILD` | `24` |  |
| `LOOP` | `25` |  |

### make

```mach
pub fun make(kind: Kind, operation: Operation) Error
```

an error std raised itself, with no native code behind it

| Parameter | |
| :--- | :--- |
| `kind` | the portable classification |
| `operation` | the operation that failed |
| **returns** | the error, with code and cleanup_code 0 |

### kind_name

```mach
pub fun kind_name(kind: Kind) str
```

the name of a kind, for messages about an error with no native code

## Operation

```mach
pub def Operation: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `OP_UNKNOWN` | `0` |  |
| `OP_OPEN` | `1` |  |
| `OP_CLOSE` | `2` |  |
| `OP_READ` | `3` |  |
| `OP_WRITE` | `4` |  |
| `OP_CREATE` | `5` |  |
| `OP_BIND` | `6` |  |
| `OP_LISTEN` | `7` |  |
| `OP_ACCEPT` | `8` |  |
| `OP_CONNECT` | `9` |  |
| `OP_RECEIVE` | `10` |  |
| `OP_SEND` | `11` |  |
| `OP_SHUTDOWN` | `12` |  |
| `OP_OPTION` | `13` |  |
| `OP_SEEK` | `14` |  |
| `OP_SYNC` | `15` |  |
| `OP_SUBMIT` | `16` |  |
| `OP_WAIT` | `17` |  |
| `OP_WAKE` | `18` |  |
| `OP_LOCK` | `19` | pinning memory resident, refused when the host will not lock it |

## Error

```mach
pub rec Error {
    kind:      Kind;
    code:      i64;
    operation: Operation;
    # first secondary cleanup failure, zero when none was observed
    cleanup_code: i64;
}
```

### retryable

```mach
pub fun retryable(error: Error) bool
```

