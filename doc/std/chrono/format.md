[std](../README.md) / [chrono](README.md) / **format**

# std.chrono.format

date and time formatting and reading

provides formatters for standard time representations, and the reader of the
RFC 3339 forms they write.
intended usage: `use fmt: std.chrono.format;` then
`fmt.rfc3339(dt, fmt.Fraction.digits{3}, buf, len)`.

Source: [`src/chrono/format.mach`](../../../src/chrono/format.mach)

| Type | | |
| :--- | :--- | :--- |
| [`ReadError`](#readerror) | `tag` | every way reading a date or time can fail |
| [`Stamp`](#stamp) | `tag` | a date or time value in one of the forms RFC 3339 builds |
| [`Fraction`](#fraction) | `tag` | how a writer spells the fraction of a second, which RFC 3339 leaves to it |
| [`StampRead`](#stampread) | `rec` | a value read and the bytes it took |

| On `Fraction` | |
| :--- | :--- |
| [`rfc3339`](#rfc3339) | write a Datetime as RFC 3339 into a buffer |
| [`rfc3339_time`](#rfc3339_time) | write a TimeOfDay as RFC 3339 partial-time into a buffer |
| [`rfc3339_local`](#rfc3339_local) | write a LocalDatetime as RFC 3339 full-date and partial-time into a buffer |

| On `StampRead` | |
| :--- | :--- |
| [`read_rfc3339`](#read_rfc3339) | read the RFC 3339 date or time value at the start of a span |

| Functions | |
| :--- | :--- |
| [`rfc3339_date`](#rfc3339_date) | write a Date as RFC 3339 full-date into a buffer |
| [`rfc2822`](#rfc2822) | write a Datetime as RFC 2822 into a buffer |
| [`unix_sec`](#unix_sec) | write seconds as decimal Unix timestamp into a buffer |

---

## ReadError

```mach
pub tag ReadError: u8 {
    syntax: usize;
    range:  usize;
}
```

every way reading a date or time can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `syntax` | `usize` | the byte at the payload offset is not what the grammar allows there: a missing digit, separator or offset, or the text ends early |
| `range` | `usize` | the field starting at the payload offset is outside its range: a month past 12, a day past its month's length, an hour past 23, a minute past 59, a second past 60, or a second of 60 where no leap second can fall |

## Stamp

```mach
pub tag Stamp: u8 {
    date:     Date;
    time:     TimeOfDay;
    local:    LocalDatetime;
    datetime: Datetime;
}
```

a date or time value in one of the forms RFC 3339 builds

| Case | Payload | |
| :--- | :--- | :--- |
| `date` | `Date` | full-date: a calendar date |
| `time` | `TimeOfDay` | partial-time: a time of day |
| `local` | `LocalDatetime` | full-date, separator, partial-time: a local datetime (ISO 8601's form without an offset) |
| `datetime` | `Datetime` | date-time: a datetime with its offset |

## Fraction

```mach
pub tag Fraction: u8 {
    shortest;
    digits:              u8;
    digits_unless_whole: u8;
}
```

how a writer spells the fraction of a second, which RFC 3339 leaves to it

| Case | Payload | |
| :--- | :--- | :--- |
| `shortest` |  | the fewest digits that hold nsec exactly, none for a whole second: what reads back to the same value |
| `digits` | `u8` | exactly this many digits, 0 to 9, nsec past them truncated and zeros written, so every value has one width |
| `digits_unless_whole` | `u8` | this many digits as `digits` writes them, and none when they are all zero |

### rfc3339

```mach
pub fun rfc3339(dt: Datetime, fraction: Fraction, buf: *u8, len: usize) usize
```

write a Datetime as RFC 3339 into a buffer

output: YYYY-MM-DDTHH:MM:SS, the fraction of a second as `fraction` states
it, then the offset: Z for a known offset of zero (RFC 3339's spelling of
UTC, which +00:00 means too), -00:00 for an unknown one, else +HH:MM or
-HH:MM. reads back through read_rfc3339 to the same fields when the fraction
keeps every digit of nsec

| Parameter | |
| :--- | :--- |
| `dt` | datetime to format |
| `fraction` | how the fraction of a second is written |
| `buf` | output buffer (at least 36 bytes) |
| `len` | buffer length |
| **returns** | bytes written (excluding null terminator), 0 if buffer too small, the year is outside [0, 9999], the offset is not a whole number of minutes, the fraction asks for more than 9 digits, or dt is not valid (datetime_is_valid) |

### rfc3339_time

```mach
pub fun rfc3339_time(t: TimeOfDay, fraction: Fraction, buf: *u8, len: usize) usize
```

write a TimeOfDay as RFC 3339 partial-time into a buffer

output: HH:MM:SS, the fraction of a second as `fraction` states it

| Parameter | |
| :--- | :--- |
| `t` | time of day to format |
| `fraction` | how the fraction of a second is written |
| `buf` | output buffer (at least 19 bytes) |
| `len` | buffer length |
| **returns** | bytes written (excluding null terminator), 0 if buffer too small, the fraction asks for more than 9 digits, or t is not valid (time_of_day_is_valid) |

### rfc3339_local

```mach
pub fun rfc3339_local(ldt: LocalDatetime, fraction: Fraction, buf: *u8, len: usize) usize
```

write a LocalDatetime as RFC 3339 full-date and partial-time into a buffer

output: YYYY-MM-DDTHH:MM:SS, the fraction of a second as `fraction` states
it, and no offset

| Parameter | |
| :--- | :--- |
| `ldt` | local datetime to format |
| `fraction` | how the fraction of a second is written |
| `buf` | output buffer (at least 30 bytes) |
| `len` | buffer length |
| **returns** | bytes written (excluding null terminator), 0 if buffer too small, the year is outside [0, 9999], the fraction asks for more than 9 digits, or ldt is not valid (local_datetime_is_valid) |

## StampRead

```mach
pub rec StampRead {
    stamp: Stamp;
    size:  usize;
}
```

a value read and the bytes it took

### read_rfc3339

```mach
pub fun read_rfc3339(s: *u8, len: usize) res[StampRead, ReadError]
```

read the RFC 3339 date or time value at the start of a span

reads the longest of the four forms there: a full-date, a partial-time, or a
full-date and partial-time joined by T, t or a space (the readability form
RFC 3339 section 5.6 permits) and then either an offset or none. a space
joins them only when a partial-time's hour and colon follow it, so a date
followed by a space and other text is a date. a T or t commits to a time.
Z, z and +00:00 are UTC, and -00:00 is UTC with the local offset unknown
(RFC 3339 section 4.3), read as offset 0 with offset_unknown set. fraction digits past the ninth are read and dropped, never rounded.
every field is checked against its range (date_is_valid,
time_of_day_is_valid, datetime_is_valid), so a value is refused, never
normalized.

| Parameter | |
| :--- | :--- |
| `s` | the span's bytes |
| `len` | the span's length |
| **returns** | the value and the bytes it took, or the failure positioned in the span |

## Functions

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
| **returns** | bytes written (excluding null terminator), 0 if buffer too small, the year is outside [0, 9999], or d is not valid (date_is_valid) |

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
| **returns** | bytes written (excluding null terminator), 0 if buffer too small, the offset's hours do not fit two digits, or the offset is not a whole number of minutes |

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

