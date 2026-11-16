[std](../README.md) / [log](README.md) / **record**

# std.log.record

typed structured log records and deterministic logfmt encoding

Source: [`src/log/record.mach`](../../../src/log/record.mach)

Uses types from [`std.chrono.time`](../chrono/time.md), [`std.io.error`](../io/error.md).

| Type | | |
| :--- | :--- | :--- |
| [`Level`](#level) | `def` |  |
| [`Precision`](#precision) | `def` |  |
| [`ClockOwnership`](#clockownership) | `def` |  |
| [`NowFun`](#nowfun) | `def` | a clock source samples the current time or reports why it could not |
| [`ClockError`](#clockerror) | `tag` | every way a sample can fail |
| [`Sample`](#sample) | `def` | the outcome of one sample, normalized to the clock's precision |
| [`Clock`](#clock-1) | `rec` | the clock context is borrowed and must outlive every logger using it |
| [`FieldKind`](#fieldkind) | `def` |  |
| [`Bytes`](#bytes) | `rec` |  |
| [`Field`](#field) | `rec` | keys and borrowed string or byte values must outlive record encoding |
| [`Record`](#record) | `rec` | the timestamp is owned by value while message and fields are borrowed |
| [`OversizePolicy`](#oversizepolicy) | `def` |  |
| [`EncodeError`](#encodeerror) | `tag` | every way an encoding can fail; nothing is emitted on any of them |
| [`EncodeStatus`](#encodestatus) | `tag` | the outcome of one encoding |
| [`Encoded`](#encoded) | `rec` | len is the bytes emitted; required is the full record's size whenever the record was valid enough to measure, zero otherwise |

| On `Level` | |
| :--- | :--- |
| [`DEBUG`](#level), [`INFO`](#level), [`WARN`](#level), [`ERROR`](#level), [`OFF`](#level), [`level_name`](#level_name) | |

| On `Precision` | |
| :--- | :--- |
| [`PRECISION_SECONDS`](#precision), [`PRECISION_MILLIS`](#precision), [`PRECISION_MICROS`](#precision), [`PRECISION_NANOS`](#precision) | |
| [`system_clock`](#system_clock) | the system clock reads the OS layer's clock group |
| [`record_at`](#record_at) | |

| On `ClockOwnership` | |
| :--- | :--- |
| [`CLOCK_CONTEXT_NONE`](#clockownership), [`CLOCK_CONTEXT_BORROWED`](#clockownership) | |

| On `NowFun` | |
| :--- | :--- |
| [`clock`](#clock) | |

| On `Clock` | |
| :--- | :--- |
| [`clock_valid`](#clock_valid) | |
| [`clock_now`](#clock_now) | sample the clock; a failed clock is never zero time |

| On `FieldKind` | |
| :--- | :--- |
| [`FIELD_I64`](#fieldkind), [`FIELD_U64`](#fieldkind), [`FIELD_BOOL`](#fieldkind), [`FIELD_BYTES`](#fieldkind), [`FIELD_STRING`](#fieldkind), [`FIELD_ERROR`](#fieldkind) | |
| [`FIELD_TEXT`](#fieldkind) | length-delimited text, rendered and escaped like FIELD_STRING |

| On `Field` | |
| :--- | :--- |
| [`field_i64`](#field_i64), [`field_u64`](#field_u64), [`field_bool`](#field_bool), [`field_bytes`](#field_bytes), [`field_string`](#field_string) | |
| [`field_text`](#field_text) | borrowed text with an explicit length, for a view that carries no terminator |
| [`field_error`](#field_error) | |

| On `Record` | |
| :--- | :--- |
| [`encode`](#encode) | encode one record into caller-owned storage |

| On `OversizePolicy` | |
| :--- | :--- |
| [`OVERSIZE_REJECT`](#oversizepolicy), [`OVERSIZE_TRUNCATE`](#oversizepolicy) | |

| Constants | |
| :--- | :--- |
| [`MAX_RECORD_BYTES`](#constants), [`MIN_TRUNCATED_BYTES`](#constants) | |

---

## Level

```mach
pub def Level: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `DEBUG` | `0` |  |
| `INFO` | `1` |  |
| `WARN` | `2` |  |
| `ERROR` | `3` |  |
| `OFF` | `4` |  |

### level_name

```mach
pub fun level_name(level: Level) str
```

## Precision

```mach
pub def Precision: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `PRECISION_SECONDS` | `0` |  |
| `PRECISION_MILLIS` | `1` |  |
| `PRECISION_MICROS` | `2` |  |
| `PRECISION_NANOS` | `3` |  |

### system_clock

Only where `capability.HAS_CLOCK`.

```mach
pub fun system_clock(precision: Precision) Clock
```

the system clock reads the OS layer's clock group

### record_at

```mach
pub fun record_at(timestamp: Time, precision: Precision, level: Level, message: str, fields: *Field, field_count: usize) Record
```

## ClockOwnership

```mach
pub def ClockOwnership: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `CLOCK_CONTEXT_NONE` | `0` |  |
| `CLOCK_CONTEXT_BORROWED` | `1` |  |

## NowFun

```mach
pub def NowFun: fun(ptr) std.chrono.time.Clock
```

a clock source samples the current time or reports why it could not

### clock

```mach
pub fun clock(ctx: ptr, f_now: NowFun, precision: Precision) Clock
```

## ClockError

```mach
pub tag ClockError: u8 {
    invalid;
    read: std.io.error.Error;
}
```

every way a sample can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | the clock has no source, an unknown precision or an ownership that does not match its context |
| `read` | `std.io.error.Error` | the source refused; payload is its native failure |

## Sample

```mach
pub def Sample: res[Time, ClockError]
```

the outcome of one sample, normalized to the clock's precision

## Clock

```mach
pub rec Clock {
    ctx:       ptr;
    f_now:     NowFun;
    precision: Precision;
    ownership: ClockOwnership;
}
```

the clock context is borrowed and must outlive every logger using it

### clock_valid

```mach
pub fun clock_valid(c: *Clock) bool
```

### clock_now

```mach
pub fun clock_now(c: *Clock) Sample
```

sample the clock; a failed clock is never zero time

## FieldKind

```mach
pub def FieldKind: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `FIELD_I64` | `0` |  |
| `FIELD_U64` | `1` |  |
| `FIELD_BOOL` | `2` |  |
| `FIELD_BYTES` | `3` |  |
| `FIELD_STRING` | `4` |  |
| `FIELD_ERROR` | `5` |  |
| `FIELD_TEXT` | `6` | length-delimited text, rendered and escaped like FIELD_STRING |

## Bytes

```mach
pub rec Bytes {
    data: *u8;
    len:  usize;
}
```

## Field

```mach
pub rec Field {
    key:   str;
    kind:  FieldKind;
    value: uni {
        i64_value: i64;
        u64_value: u64;
        bool_value: bool;
        bytes_value: Bytes;
        string_value: str;
        error_value: std.io.error.Error;
        text_value: Bytes;
    };
}
```

keys and borrowed string or byte values must outlive record encoding

### field_i64

```mach
pub fun field_i64(key: str, value: i64) Field
```

### field_u64

```mach
pub fun field_u64(key: str, value: u64) Field
```

### field_bool

```mach
pub fun field_bool(key: str, value: bool) Field
```

### field_bytes

```mach
pub fun field_bytes(key: str, data: *u8, len: usize) Field
```

### field_string

```mach
pub fun field_string(key: str, value: str) Field
```

### field_text

```mach
pub fun field_text(key: str, data: *u8, len: usize) Field
```

borrowed text with an explicit length, for a view that carries no terminator

### field_error

```mach
pub fun field_error(key: str, value: std.io.error.Error) Field
```

## Record

```mach
pub rec Record {
    timestamp:   Time;
    precision:   Precision;
    level:       Level;
    message:     str;
    fields:      *Field;
    field_count: usize;
}
```

the timestamp is owned by value while message and fields are borrowed

### encode

```mach
pub fun encode(record: *Record, data: *u8, cap: usize, limit: usize, policy: OversizePolicy) Encoded
```

encode one record into caller-owned storage

reject emits no bytes. truncate retains whole leading tokens and appends
truncated=true, so the result remains a complete logfmt line.

## OversizePolicy

```mach
pub def OversizePolicy: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `OVERSIZE_REJECT` | `0` |  |
| `OVERSIZE_TRUNCATE` | `1` |  |

## EncodeError

```mach
pub tag EncodeError: u8 {
    invalid;
    buffer: usize;
    limit;
}
```

every way an encoding can fail; nothing is emitted on any of them

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | the record, policy, limit or buffer arguments are not encodable |
| `buffer` | `usize` | the caller's buffer cannot hold the encoding; payload is the bytes the full record needs |
| `limit` |  | the truncation limit is below MIN_TRUNCATED_BYTES |

## EncodeStatus

```mach
pub tag EncodeStatus: u8 {
    encoded;
    truncated;
    rejected;
    failed: EncodeError;
}
```

the outcome of one encoding

| Case | Payload | |
| :--- | :--- | :--- |
| `encoded` |  | the full record was emitted |
| `truncated` |  | whole leading tokens and a truncated=true marker were emitted |
| `rejected` |  | the record exceeds the limit under OVERSIZE_REJECT; nothing was emitted and Encoded.required carries its size |
| `failed` | `EncodeError` | the encoding could not proceed |

## Encoded

```mach
pub rec Encoded {
    status:   EncodeStatus;
    len:      usize;
    required: usize;
}
```

len is the bytes emitted; required is the full record's size whenever the
record was valid enough to measure, zero otherwise

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `MAX_RECORD_BYTES` | `usize` | `8192` |  |
| `MIN_TRUNCATED_BYTES` | `usize` | `15` |  |

