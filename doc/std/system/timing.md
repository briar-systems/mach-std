[std](../README.md) / [system](README.md) / **timing**

# std.system.timing

the data-independent-timing mode the processor provides, as a run-time query

constant-time code is constant time on some processors only under a mode
the processor or system provides. on aarch64 that is PSTATE.DIT, which each
soft constant-time function switches for itself where the processor
provides it and the process may switch it (see std.system.dit). `mode`
answers from the hardware alone. no other target has a mode a process can
set (x86-64's DOITM is the kernel's to configure), so there the answer is
UNAVAILABLE.

Source: [`src/system/timing.mach`](../../../src/system/timing.mach)

| Functions | |
| :--- | :--- |
| [`mode`](#mode) | whether the processor provides the timing mode |

| Constants | |
| :--- | :--- |
| [`AVAILABLE`](#constants) | the processor provides the mode and the process may switch it |
| [`UNAVAILABLE`](#constants) | the processor or target does not provide a mode the process can switch |

---

## Functions

### mode

```mach
pub fun mode() i64
```

whether the processor provides the timing mode

| Parameter | |
| :--- | :--- |
| **returns** | AVAILABLE or UNAVAILABLE |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `AVAILABLE` | `i64` | `0` | the processor provides the mode and the process may switch it |
| `UNAVAILABLE` | `i64` | `1` | the processor or target does not provide a mode the process can switch |

