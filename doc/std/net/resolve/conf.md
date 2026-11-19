[std](../../README.md) / [net](../README.md) / [resolve](README.md) / **conf**

# std.net.resolve.conf

resolv.conf resolver policy

Source: [`src/net/resolve/conf.mach`](../../../../src/net/resolve/conf.mach)

Uses types from [`std.io.error`](../../io/error.md), [`std.net.ip`](../ip.md).

| Type | | |
| :--- | :--- | :--- |
| [`Config`](#config) | `rec` | parsed resolver policy with glibc-compatible defaults and caps |

| On `Config` | |
| :--- | :--- |
| [`defaults`](#defaults), [`search_domain`](#search_domain) | |
| [`parse_line`](#parse_line) | fold one configuration line into config; comments and noise are skipped |
| [`finish`](#finish) | a configuration with no reachable nameserver falls back to loopback, matching every mainstream resolver's behavior |
| [`load`](#load) | load the target resolver policy from /etc/resolv.conf |

| Constants | |
| :--- | :--- |
| [`DNS_PORT`](#constants), [`MAX_NAMESERVERS`](#constants), [`MAX_SEARCH`](#constants), [`MAX_NAME`](#constants) | |

---

## Config

```mach
pub rec Config {
    nameservers:      [3]std.net.ip.Endpoint;
    nameserver_count: usize;
    search:           [1524]u8;
    search_count:     usize;
    ndots:            u32;
    timeout_ms:       u64;
    attempts:         u32;
    rotate:           bool;
}
```

parsed resolver policy with glibc-compatible defaults and caps

| Field | Type | |
| :--- | :--- | :--- |
| `nameservers` | `[3]std.net.ip.Endpoint` | servers queried in order (rotated when rotate is set) |
| `nameserver_count` | `usize` | valid entries in nameservers |
| `search` | `[1524]u8` | MAX_SEARCH nul-terminated slots of MAX_NAME bytes each |
| `search_count` | `usize` | valid slots in search |
| `ndots` | `u32` | dot threshold selecting literal-first lookup order |
| `timeout_ms` | `u64` | per-request wait before the next server is tried, within the lookup's scope |
| `attempts` | `u32` | full passes over the nameserver list |
| `rotate` | `bool` | start each lookup at a different server |

### defaults

```mach
pub fun defaults(config: *Config)
```

### search_domain

```mach
pub fun search_domain(config: *Config, index: usize) *u8
```

### parse_line

```mach
pub fun parse_line(config: *Config, line: *u8)
```

fold one configuration line into config; comments and noise are skipped

### finish

```mach
pub fun finish(config: *Config)
```

a configuration with no reachable nameserver falls back to loopback,
matching every mainstream resolver's behavior

### load

```mach
pub fun load(config: *Config) err[std.io.error.Error]
```

load the target resolver policy from /etc/resolv.conf

a missing file is the defaults; a file that cannot be opened, read or
closed is the failure, with the defaults and whatever was parsed before
the failure left in `config`.

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `DNS_PORT` | `u16` | `53` |  |
| `MAX_NAMESERVERS` | `usize` | `3` |  |
| `MAX_SEARCH` | `usize` | `6` |  |
| `MAX_NAME` | `usize` | `254` |  |

