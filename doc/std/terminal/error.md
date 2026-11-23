[std](../README.md) / [terminal](README.md) / **error**

# std.terminal.error

terminal outcomes shared by std.terminal and its per-os backends

lives in its own module so the parent and the backends name one tag without
a circular import, the same split std.terminal.key makes for Key.

Source: [`src/terminal/error.mach`](../../../src/terminal/error.mach)

Uses types from [`std.io.error`](../io/error.md), [`std.terminal.key`](key.md).

| Type | | |
| :--- | :--- | :--- |
| [`TermError`](#termerror) | `tag` | every way a terminal operation can fail |
| [`Operation`](#operation) | `def` | the outcome of a mode or queue control call |
| [`Poll`](#poll) | `def` | the outcome of one poll: a waiting key, absence when the queue is empty, or the native read failure |

| On `TermError` | |
| :--- | :--- |
| [`code`](#code) | the native code behind a terminal failure |

---

## TermError

```mach
pub tag TermError: u8 {
    native: std.io.error.Error;
}
```

every way a terminal operation can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `native` | `std.io.error.Error` | the terminal call failed; payload carries the native failure, its operation being OP_OPTION for a mode or queue control call and OP_READ for a poll |

### code

```mach
pub fun code(e: TermError) i64
```

the native code behind a terminal failure

## Operation

```mach
pub def Operation: err[TermError]
```

the outcome of a mode or queue control call

## Poll

```mach
pub def Poll: res[opt[std.terminal.key.Key], TermError]
```

the outcome of one poll: a waiting key, absence when the queue is empty, or
the native read failure

