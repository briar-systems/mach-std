[std](../../README.md) / [net](../README.md) / [async](README.md) / **retired**

# std.net.async.retired

the openings detach retired, across every driver in the process

a driver knows only the sockets it has seen, so on its own it would take a
copy of a detached stream's old handle for a socket it had not met. detach
raises a floor for the native value here, and a driver reads the floor when it
meets a value under an opening it has no record of. openings only grow, so a
socket that later reuses the value is above the floor and passes.

a value keeps its entry for the life of the process, so the table never holds
more than one entry per native value that was ever detached

Source: [`src/net/async/retired.mach`](../../../../src/net/async/retired.mach)

| Functions | |
| :--- | :--- |
| [`reserve`](#reserve) | make sure retire of value cannot fail, before anything is given up |
| [`retire`](#retire) | refuse every handle of value at or below opening, on every driver |
| [`stale`](#stale) | whether a handle was retired on some driver |

---

## Functions

### reserve

```mach
pub fun reserve(value: usize) bool
```

make sure retire of value cannot fail, before anything is given up

| Parameter | |
| :--- | :--- |
| `value` | the native socket |
| **returns** | false when the table cannot grow, and nothing changes |

### retire

```mach
pub fun retire(value: usize, opening: u64)
```

refuse every handle of value at or below opening, on every driver. reserve
has run for value

### stale

```mach
pub fun stale(value: usize, opening: u64) bool
```

whether a handle was retired on some driver. a backend whose handles carry no
opening passes 0, which nothing retires

