[std](../../README.md) / [system](../README.md) / [os](README.md) / **errors**

# std.system.os.errors

the portable reading of a native code, written once over the selected OS's codes

each per-OS module forwards error_kind from here. linux and darwin return
negated errno values, and windows maps its native errors onto the same names.

Source: [`src/system/os/errors.mach`](../../../../src/system/os/errors.mach)

Uses types from [`std.io.error`](../../io/error.md).

| Functions | |
| :--- | :--- |
| [`error_kind`](#error_kind) | the portable kind of a native error code |

---

## Functions

### error_kind

```mach
pub fun error_kind(code: i64) std.io.error.Kind
```

the portable kind of a native error code

| Parameter | |
| :--- | :--- |
| `code` | a negative native code from the selected implementation |
| **returns** | its io.error kind, OTHER when no portable kind fits |

