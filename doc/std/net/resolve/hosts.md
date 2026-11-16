[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **hosts**

# std.net.resolve.hosts

hosts-file name lookup

Source: [`src/net/resolve/hosts.mach`](../../../../src/net/resolve/hosts.mach)

Uses types from [`std.io.error`](../../io/error.md), [`std.net.ip`](../ip.md).

| Type | | |
| :--- | :--- | :--- |
| [`Lookup`](#lookup) | `rec` | one in-progress hosts lookup accumulating matches in file order |

| On `Lookup` | |
| :--- | :--- |
| [`scan_line`](#scan_line) | fold one hosts line into the lookup |
| [`collect`](#collect) | collect every hosts-file address for the lookup's hostname, in file order |

---

## Lookup

```mach
pub rec Lookup {
    hostname:           str;
    want_v4:            bool;
    want_v6:            bool;
    addrs:              *std.net.ip.Addr;
    capacity:           usize;
    count:              usize;
    canonical:          *u8;
    canonical_capacity: usize;
}
```

one in-progress hosts lookup accumulating matches in file order

| Field | Type | |
| :--- | :--- | :--- |
| `hostname` | `str` | name to match, case-insensitively want_v4, want_v6:   family filter applied while collecting |
| `addrs` | `*std.net.ip.Addr` | caller storage for matched addresses |
| `capacity` | `usize` | slots in addrs |
| `count` | `usize` | matches written so far |
| `canonical` | `*u8` | first name of the first matching line, nul-terminated; empty until a line matches. nil to skip collection |
| `canonical_capacity` | `usize` | bytes available at canonical |

### scan_line

```mach
pub fun scan_line(lookup: *Lookup, line: *u8)
```

fold one hosts line into the lookup

### collect

```mach
pub fun collect(lookup: *Lookup) res[usize, std.io.error.Error]
```

collect every hosts-file address for the lookup's hostname, in file order

a missing hosts file is zero matches; a file that cannot be opened, read or
closed is the failure, with the matches collected before it kept in
lookup.addrs

| Parameter | |
| :--- | :--- |
| **returns** | number of addresses written to lookup.addrs, or the failure |

