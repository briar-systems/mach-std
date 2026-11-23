[std](../README.md) / [chrono](README.md) / **date**

# std.chrono.date

calendar date and datetime types with civil date math

Date represents a calendar date (year, month, day) and TimeOfDay a reading of
the clock (hour, minute, second, nanosecond), each with nothing else.
LocalDatetime is the two together with no UTC offset, a wall-clock reading
that names no instant until an offset is chosen. Datetime adds the UTC offset
it was read at, so it names one instant and keeps the offset beside it.

Source: [`src/chrono/date.mach`](../../../src/chrono/date.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Date`](#date) | `rec` | a calendar date without time-of-day or timezone |
| [`TimeOfDay`](#timeofday) | `rec` | a time of day without a date or UTC offset |
| [`LocalDatetime`](#localdatetime) | `rec` | a calendar date with time-of-day and no UTC offset |
| [`Datetime`](#datetime) | `rec` | a calendar date with time-of-day and UTC offset |

| On `Date` | |
| :--- | :--- |
| [`date_is_valid`](#date_is_valid) | report whether d names a day of the proleptic Gregorian calendar |
| [`local_datetime`](#local_datetime) | join a date and a time of day into a local datetime |
| [`date_from_time`](#date_from_time) | extract the UTC date from a Time |
| [`date_to_time`](#date_to_time) | convert a Date to a Time at midnight UTC |

| On `TimeOfDay` | |
| :--- | :--- |
| [`time_of_day_is_valid`](#time_of_day_is_valid) | report whether t is a reading of the clock |

| On `LocalDatetime` | |
| :--- | :--- |
| [`local_datetime_is_valid`](#local_datetime_is_valid) | report whether ldt is a valid date and time of day, as the two are alone |
| [`local_date`](#local_date) | the date of a local datetime |
| [`local_time_of_day`](#local_time_of_day) | the time of day of a local datetime |
| [`local_with_offset`](#local_with_offset) | read a local datetime at a UTC offset |

| On `Datetime` | |
| :--- | :--- |
| [`datetime_is_valid`](#datetime_is_valid) | report whether dt names an instant |
| [`datetime_local`](#datetime_local) | the wall-clock reading of a datetime, its offset dropped |
| [`datetime_from_time`](#datetime_from_time) | extract a UTC Datetime from a Time |
| [`datetime_with_offset`](#datetime_with_offset) | extract a Datetime from a Time with a UTC offset |
| [`datetime_to_time`](#datetime_to_time) | convert a Datetime back to a Time instant |

| Functions | |
| :--- | :--- |
| [`is_leap_year`](#is_leap_year) | report whether year is a leap year |
| [`days_in_month`](#days_in_month) | return the number of days in a given month |
| [`floor_div`](#floor_div) | divide rounding toward negative infinity |
| [`civil_to_days`](#civil_to_days) | count the days from 1970-01-01 to a date of the proleptic Gregorian calendar |

---

## Date

```mach
pub rec Date {
    year:  i64;
    month: i64;
    day:   i64;
}
```

a calendar date without time-of-day or timezone

| Field | Type | |
| :--- | :--- | :--- |
| `year` | `i64` | year (e.g. 2025) |
| `month` | `i64` | month [1, 12] |
| `day` | `i64` | day of month [1, 31] |

### date_is_valid

```mach
pub fun date_is_valid(d: Date) bool
```

report whether d names a day of the proleptic Gregorian calendar

| Parameter | |
| :--- | :--- |
| `d` | date to test |
| **returns** | true if month is in [1, 12] and day within that month's length |

### local_datetime

```mach
pub fun local_datetime(d: Date, t: TimeOfDay) LocalDatetime
```

join a date and a time of day into a local datetime

| Parameter | |
| :--- | :--- |
| `d` | the date |
| `t` | the time of day |
| **returns** | the local datetime holding both |

### date_from_time

```mach
pub fun date_from_time(t: Time) Date
```

extract the UTC date from a Time

| Parameter | |
| :--- | :--- |
| `t` | time instant |
| **returns** | UTC calendar date |

### date_to_time

```mach
pub fun date_to_time(d: Date) Time
```

convert a Date to a Time at midnight UTC

| Parameter | |
| :--- | :--- |
| `d` | date to convert |
| **returns** | time instant at 00:00:00 UTC on the given date |

## TimeOfDay

```mach
pub rec TimeOfDay {
    hour:   i64;
    minute: i64;
    second: i64;
    nsec:   i64;
}
```

a time of day without a date or UTC offset

| Field | Type | |
| :--- | :--- | :--- |
| `hour` | `i64` | hour [0, 23] |
| `minute` | `i64` | minute [0, 59] |
| `second` | `i64` | second [0, 60], 60 in a leap second |
| `nsec` | `i64` | nanoseconds within second [0, 999999999] |

### time_of_day_is_valid

```mach
pub fun time_of_day_is_valid(t: TimeOfDay) bool
```

report whether t is a reading of the clock

a second of 60 is accepted at any minute: with no date and no offset there is
nothing to place it against, and some offset puts a leap second at each minute

| Parameter | |
| :--- | :--- |
| `t` | time of day to test |
| **returns** | true if every field is within its range |

## LocalDatetime

```mach
pub rec LocalDatetime {
    year:   i64;
    month:  i64;
    day:    i64;
    hour:   i64;
    minute: i64;
    second: i64;
    nsec:   i64;
}
```

a calendar date with time-of-day and no UTC offset

| Field | Type | |
| :--- | :--- | :--- |
| `year` | `i64` | year (e.g. 2025) |
| `month` | `i64` | month [1, 12] |
| `day` | `i64` | day of month [1, 31] |
| `hour` | `i64` | hour [0, 23] |
| `minute` | `i64` | minute [0, 59] |
| `second` | `i64` | second [0, 60], 60 in a leap second |
| `nsec` | `i64` | nanoseconds within second [0, 999999999] |

### local_datetime_is_valid

```mach
pub fun local_datetime_is_valid(ldt: LocalDatetime) bool
```

report whether ldt is a valid date and time of day, as the two are alone

| Parameter | |
| :--- | :--- |
| `ldt` | local datetime to test |
| **returns** | true if its date and its time of day are each valid |

### local_date

```mach
pub fun local_date(ldt: LocalDatetime) Date
```

the date of a local datetime

| Parameter | |
| :--- | :--- |
| `ldt` | local datetime |
| **returns** | its year, month and day |

### local_time_of_day

```mach
pub fun local_time_of_day(ldt: LocalDatetime) TimeOfDay
```

the time of day of a local datetime

| Parameter | |
| :--- | :--- |
| `ldt` | local datetime |
| **returns** | its hour, minute, second and nanoseconds |

### local_with_offset

```mach
pub fun local_with_offset(ldt: LocalDatetime, offset: i64) Datetime
```

read a local datetime at a UTC offset

| Parameter | |
| :--- | :--- |
| `ldt` | the wall-clock reading |
| `offset` | UTC offset in seconds it was read at |
| **returns** | the datetime naming that instant, its fields those of ldt |

## Datetime

```mach
pub rec Datetime {
    year:           i64;
    month:          i64;
    day:            i64;
    hour:           i64;
    minute:         i64;
    second:         i64;
    nsec:           i64;
    offset:         i64;
    offset_unknown: bool;
}
```

a calendar date with time-of-day and UTC offset

| Field | Type | |
| :--- | :--- | :--- |
| `year` | `i64` | year (e.g. 2025) |
| `month` | `i64` | month [1, 12] |
| `day` | `i64` | day of month [1, 31] |
| `hour` | `i64` | hour [0, 23] |
| `minute` | `i64` | minute [0, 59] |
| `second` | `i64` | second [0, 60], 60 only in a leap second (see datetime_is_valid) |
| `nsec` | `i64` | nanoseconds within second [0, 999999999] |
| `offset` | `i64` | UTC offset in seconds (0 = UTC, 3600 = +01:00, -18000 = -05:00) |
| `offset_unknown` | `bool` | the fields are in UTC and the local offset is not known (RFC 3339 section 4.3, written -00:00); offset is then 0 |

### datetime_is_valid

```mach
pub fun datetime_is_valid(dt: Datetime) bool
```

report whether dt names an instant

the offset is less than a day either way, and 0 when it is unknown, and a
second of 60 falls where a
leap second can: the second after 23:59:59 UTC on the last day of a month,
moved by the offset (RFC 3339, section 5.7). whether that month had one is
the IERS's to announce, and is not checked

| Parameter | |
| :--- | :--- |
| `dt` | datetime to test |
| **returns** | true if its fields, its offset and any leap second are valid |

### datetime_local

```mach
pub fun datetime_local(dt: Datetime) LocalDatetime
```

the wall-clock reading of a datetime, its offset dropped

| Parameter | |
| :--- | :--- |
| `dt` | datetime |
| **returns** | its fields without the offset |

### datetime_from_time

```mach
pub fun datetime_from_time(t: Time) Datetime
```

extract a UTC Datetime from a Time

| Parameter | |
| :--- | :--- |
| `t` | time instant |
| **returns** | UTC datetime |

### datetime_with_offset

```mach
pub fun datetime_with_offset(t: Time, offset: i64) Datetime
```

extract a Datetime from a Time with a UTC offset

| Parameter | |
| :--- | :--- |
| `t` | time instant |
| `offset` | UTC offset in seconds |
| **returns** | datetime adjusted to the given offset |

### datetime_to_time

```mach
pub fun datetime_to_time(dt: Datetime) Time
```

convert a Datetime back to a Time instant

| Parameter | |
| :--- | :--- |
| `dt` | datetime to convert |
| **returns** | time instant (UTC) |

## Functions

### is_leap_year

```mach
pub fun is_leap_year(year: i64) bool
```

report whether year is a leap year

| Parameter | |
| :--- | :--- |
| `year` | year to test |
| **returns** | true if year is a leap year |

### days_in_month

```mach
pub fun days_in_month(year: i64, month: i64) i64
```

return the number of days in a given month

| Parameter | |
| :--- | :--- |
| `year` | year (needed for February) |
| `month` | month [1, 12] |
| **returns** | number of days in the month |

### floor_div

```mach
pub fun floor_div(a: i64, b: i64) i64
```

divide rounding toward negative infinity

| Parameter | |
| :--- | :--- |
| `a` | dividend |
| `b` | divisor, nonzero |
| **returns** | the largest integer not above a / b |

### civil_to_days

```mach
pub fun civil_to_days(y: i64, m: i64, d: i64) i64
```

count the days from 1970-01-01 to a date of the proleptic Gregorian calendar

| Parameter | |
| :--- | :--- |
| `y` | year |
| `m` | month [1, 12] |
| `d` | day of month [1, 31] |
| **returns** | days since the unix epoch, negative before it |

