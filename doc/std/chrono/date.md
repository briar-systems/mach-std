[std](../README.md) / [chrono](README.md) / **date**

# std.chrono.date

calendar date and datetime types with civil date math

Date represents a calendar date (year, month, day).
Datetime extends Date with time-of-day and UTC offset.

Source: [`src/chrono/date.mach`](../../../src/chrono/date.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Date`](#date) | `rec` | a calendar date without time-of-day or timezone |
| [`Datetime`](#datetime) | `rec` | a calendar date with time-of-day and UTC offset |

| On `Date` | |
| :--- | :--- |
| [`date_from_time`](#date_from_time) | extract the UTC date from a Time |
| [`date_to_time`](#date_to_time) | convert a Date to a Time at midnight UTC |

| On `Datetime` | |
| :--- | :--- |
| [`datetime_from_time`](#datetime_from_time) | extract a UTC Datetime from a Time |
| [`datetime_with_offset`](#datetime_with_offset) | extract a Datetime from a Time with a UTC offset |
| [`datetime_to_time`](#datetime_to_time) | convert a Datetime back to a Time instant |

| Functions | |
| :--- | :--- |
| [`is_leap_year`](#is_leap_year) | report whether year is a leap year |
| [`days_in_month`](#days_in_month) | return the number of days in a given month |
| [`floor_div`](#floor_div), [`civil_to_days`](#civil_to_days) | |

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

## Datetime

```mach
pub rec Datetime {
    year:   i64;
    month:  i64;
    day:    i64;
    hour:   i64;
    minute: i64;
    second: i64;
    nsec:   i64;
    offset: i64;
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
| `second` | `i64` | second [0, 59] |
| `nsec` | `i64` | nanoseconds within second [0, 999999999] |
| `offset` | `i64` | UTC offset in seconds (0 = UTC, 3600 = +01:00, -18000 = -05:00) |

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

### civil_to_days

```mach
pub fun civil_to_days(y: i64, m: i64, d: i64) i64
```

