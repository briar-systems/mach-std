[std](../README.md) / [chrono](README.md) / **format**

# std.chrono.format

date and time formatting

provides formatters for standard time representations.
intended usage: `use fmt: std.chrono.format;` then `fmt.rfc3339(dt, buf, len)`.

Source: [`src/chrono/format.mach`](../../../src/chrono/format.mach)

| Functions | |
| :--- | :--- |
| [`rfc3339`](#rfc3339) | write a Datetime as RFC 3339 into a buffer |
| [`rfc3339_date`](#rfc3339_date) | write a Date as RFC 3339 full-date into a buffer |
| [`rfc2822`](#rfc2822) | write a Datetime as RFC 2822 into a buffer |
| [`unix_sec`](#unix_sec) | write seconds as decimal Unix timestamp into a buffer |

---

## Functions

### rfc3339

```mach
pub fun rfc3339(dt: Datetime, buf: *u8, len: usize) usize
```

write a Datetime as RFC 3339 into a buffer

output: YYYY-MM-DDTHH:MM:SSZ, YYYY-MM-DDTHH:MM:SS+HH:MM,
or with fractional seconds when nsec != 0.

| Parameter | |
| :--- | :--- |
| `dt` | datetime to format |
| `buf` | output buffer (at least 36 bytes) |
| `len` | buffer length |
| **returns** | bytes written (excluding null terminator), 0 if buffer too small or the offset is a day or more either way |

### rfc3339_date

```mach
pub fun rfc3339_date(d: Date, buf: *u8, len: usize) usize
```

write a Date as RFC 3339 full-date into a buffer

output: YYYY-MM-DD

| Parameter | |
| :--- | :--- |
| `d` | date to format |
| `buf` | output buffer (at least 11 bytes) |
| `len` | buffer length |
| **returns** | bytes written (excluding null terminator), 0 if buffer too small |

### rfc2822

```mach
pub fun rfc2822(dt: Datetime, buf: *u8, len: usize) usize
```

write a Datetime as RFC 2822 into a buffer

output: Fri, 13 Feb 2009 23:31:30 +0000

| Parameter | |
| :--- | :--- |
| `dt` | datetime to format |
| `buf` | output buffer (at least 32 bytes) |
| `len` | buffer length |
| **returns** | bytes written (excluding null terminator), 0 if buffer too small or the offset's hours do not fit two digits |

### unix_sec

```mach
pub fun unix_sec(sec: i64, buf: *u8, len: usize) usize
```

write seconds as decimal Unix timestamp into a buffer

| Parameter | |
| :--- | :--- |
| `sec` | seconds since epoch |
| `buf` | output buffer (at least 21 bytes) |
| `len` | buffer length |
| **returns** | bytes written (excluding null terminator), 0 if buffer too small |

