[std](README.md) / **log**

# std.log

atomic structured logging with explicit record and sink contracts

Source: [`src/log.mach`](../../src/log.mach)

Uses types from [`std.chrono.time`](chrono/time.md), [`std.io.writer`](io/writer.md), [`std.log.record`](log/record.md), [`std.log.sink`](log/sink.md).

| Type | | |
| :--- | :--- | :--- |
| [`Logger`](#logger) | `rec` | the sink and borrowed clock context must outlive the logger |
| [`Made`](#made) | `def` | a made logger, or why it could not be made |

| On `Logger` | |
| :--- | :--- |
| [`logger_set_level`](#logger_set_level) | change the logger's minimum level, ignored for a nil logger or a level past OFF |
| [`emit`](#emit) | encode and publish one record; the report's offered count is the full record's size and truncated tells whether the sink saw a shortened line |
| [`write_at`](#write_at) | publish one record stamped with a caller-supplied time, sampling no clock |
| [`write`](#write) | stamp and publish; a clock that cannot be sampled fails the write and publishes nothing, since a record is never given a time it did not have |

| On `Made` | |
| :--- | :--- |
| [`logger`](#logger-1) | make a logger that writes records at min_level and above to output |

| Functions | |
| :--- | :--- |
| [`set_level`](#set_level) | messages below this level are suppressed before timestamp sampling |
| [`set_writer`](#set_writer) | the writer ctx is borrowed and must outlive every subsequent global log call the pair changes under out_lock, so a concurrent log call sees the old pair or the new one |
| [`debug_report`](#debug_report) | write a message at DEBUG through the global writer and report the outcome |
| [`info_report`](#info_report) | write a message at INFO through the global writer and report the outcome |
| [`warn_report`](#warn_report) | write a message at WARN through the global writer and report the outcome |
| [`error_report`](#error_report) | write a message at ERROR through the global writer and report the outcome |
| [`debug`](#debug) | write a message at DEBUG through the global writer, discarding the report |
| [`info`](#info) | write a message at INFO through the global writer, discarding the report |
| [`warn`](#warn) | write a message at WARN through the global writer, discarding the report |
| [`error`](#error) | write a message at ERROR through the global writer, discarding the report |

| Forwards | |
| :--- | :--- |
| [`MAX_RECORD_BYTES`](#max_record_bytes), [`MIN_TRUNCATED_BYTES`](#min_truncated_bytes), [`Level`](#level), [`DEBUG`](#debug-1), [`INFO`](#info-1), [`WARN`](#warn-1), [`ERROR`](#error-1), [`OFF`](#off), [`Precision`](#precision), [`PRECISION_SECONDS`](#precision_seconds), [`PRECISION_MILLIS`](#precision_millis), [`PRECISION_MICROS`](#precision_micros), [`PRECISION_NANOS`](#precision_nanos), [`ClockOwnership`](#clockownership), [`CLOCK_CONTEXT_NONE`](#clock_context_none), [`CLOCK_CONTEXT_BORROWED`](#clock_context_borrowed), [`NowFun`](#nowfun), [`ClockError`](#clockerror), [`Sample`](#sample), [`Clock`](#clock), [`FieldKind`](#fieldkind), [`FIELD_I64`](#field_i64), [`FIELD_U64`](#field_u64), [`FIELD_BOOL`](#field_bool), [`FIELD_BYTES`](#field_bytes), [`FIELD_STRING`](#field_string), [`FIELD_ERROR`](#field_error), [`Bytes`](#bytes), [`Field`](#field), [`Record`](#record), [`OversizePolicy`](#oversizepolicy), [`OVERSIZE_REJECT`](#oversize_reject), [`OVERSIZE_TRUNCATE`](#oversize_truncate), [`EncodeError`](#encodeerror), [`EncodeStatus`](#encodestatus), [`Encoded`](#encoded), [`system_clock`](#system_clock), [`clock`](#clock-1), [`clock_valid`](#clock_valid), [`clock_now`](#clock_now), [`record_at`](#record_at), [`field_i64`](#field_i64-1), [`field_u64`](#field_u64-1), [`field_bool`](#field_bool-1), [`field_bytes`](#field_bytes-1), [`field_string`](#field_string-1), [`field_error`](#field_error-1), [`level_name`](#level_name), [`encode_record`](#encode_record), [`SinkError`](#sinkerror), [`Created`](#created), [`Operation`](#operation), [`Aborted`](#aborted), [`WriteStatus`](#writestatus), [`WriteReport`](#writereport), [`Delivery`](#delivery), [`DELIVERY_DIRECT`](#delivery_direct), [`DELIVERY_BOUNDED_QUEUED`](#delivery_bounded_queued), [`OverloadPolicy`](#overloadpolicy), [`OVERLOAD_REJECT_NEW`](#overload_reject_new), [`OVERLOAD_DROP_NEW`](#overload_drop_new), [`OVERLOAD_BLOCK`](#overload_block), [`AdapterKind`](#adapterkind), [`ADAPTER_CONSOLE`](#adapter_console), [`ADAPTER_PIPE`](#adapter_pipe), [`ADAPTER_FILE`](#adapter_file), [`ADAPTER_CUSTOM`](#adapter_custom), [`Contract`](#contract), [`PublishFun`](#publishfun), [`Sink`](#sink), [`Direct`](#direct), [`QueuedRecord`](#queuedrecord), [`QueueStats`](#queuestats), [`Queued`](#queued), [`report`](#report), [`persisted`](#persisted), [`partial`](#partial), [`failed`](#failed), [`rejected`](#rejected), [`dropped`](#dropped), [`enqueued`](#enqueued), [`suppressed`](#suppressed), [`cause`](#cause), [`report_write`](#report_write), [`contract_valid`](#contract_valid), [`queued_contract`](#queued_contract), [`sink_make`](#sink_make), [`sink_publish`](#sink_publish), [`direct_custom`](#direct_custom), [`direct_writer`](#direct_writer), [`direct_console`](#direct_console), [`direct_file`](#direct_file), [`direct_pipe`](#direct_pipe), [`pipe_target_atomic_limit`](#pipe_target_atomic_limit), [`queued_sink`](#queued_sink), [`queued_sink_with_config`](#queued_sink_with_config), [`queued_close_drain`](#queued_close_drain), [`queued_close_abort`](#queued_close_abort), [`queued_join`](#queued_join), [`queued_stats`](#queued_stats), [`queued_thread_error`](#queued_thread_error), [`queued_dnit`](#queued_dnit) | |

---

## Logger

```mach
pub rec Logger {
    output:    *std.log.sink.Sink;
    clock:     std.log.record.Clock;
    min_level: i64;
}
```

the sink and borrowed clock context must outlive the logger

### logger_set_level

```mach
pub fun logger_set_level(log: *Logger, level: std.log.record.Level)
```

change the logger's minimum level, ignored for a nil logger or a level past OFF

| Parameter | |
| :--- | :--- |
| `log` | the logger to change |
| `level` | records below this level are suppressed from now on |

### emit

```mach
pub fun emit(log: *Logger, entry: *std.log.record.Record) std.log.sink.WriteReport
```

encode and publish one record; the report's offered count is the full
record's size and truncated tells whether the sink saw a shortened line

### write_at

```mach
pub fun write_at(log: *Logger, timestamp: std.chrono.time.Time, level: std.log.record.Level, message: str, fields: *std.log.record.Field, field_count: usize) std.log.sink.WriteReport
```

publish one record stamped with a caller-supplied time, sampling no clock

| Parameter | |
| :--- | :--- |
| `log` | the logger to write through |
| `timestamp` | the time recorded in the line, at the logger clock's precision |
| `level` | the record's level |
| `message` | the record's message |
| `fields` | the record's fields, borrowed for the call |
| `field_count` | how many fields are at fields |
| **returns** | the write report emit gives, failed with invalid for a nil logger |

### write

```mach
pub fun write(log: *Logger, level: std.log.record.Level, message: str, fields: *std.log.record.Field, field_count: usize) std.log.sink.WriteReport
```

stamp and publish; a clock that cannot be sampled fails the write and
publishes nothing, since a record is never given a time it did not have

## Made

```mach
pub def Made: res[Logger, std.log.sink.SinkError]
```

a made logger, or why it could not be made

### logger

```mach
pub fun logger(output: *std.log.sink.Sink, clock: std.log.record.Clock, min_level: std.log.record.Level) Made
```

make a logger that writes records at min_level and above to output

| Parameter | |
| :--- | :--- |
| `output` | the sink, which must outlive the logger |
| `clock` | the clock records are stamped with, borrowed for the logger's life |
| `min_level` | the least level written |
| **returns** | the logger; invalid for a nil sink, an invalid clock or a level past OFF, contract for a sink whose contract is inconsistent |

## Functions

### set_level

```mach
pub fun set_level(level: std.log.record.Level)
```

messages below this level are suppressed before timestamp sampling

### set_writer

```mach
pub fun set_writer(output: *std.io.writer.Writer)
```

the writer ctx is borrowed and must outlive every subsequent global log call
the pair changes under out_lock, so a concurrent log call sees the old pair or the new one

### debug_report

```mach
pub fun debug_report(message: str) std.log.sink.WriteReport
```

write a message at DEBUG through the global writer and report the outcome

| Parameter | |
| :--- | :--- |
| `message` | the message to log |
| **returns** | the write report, suppressed below the global level, failed when the clock cannot be sampled or the record cannot be encoded, rejected with too_large past MAX_RECORD_BYTES, otherwise the outcome of one write to the global writer or standard error |

### info_report

```mach
pub fun info_report(message: str) std.log.sink.WriteReport
```

write a message at INFO through the global writer and report the outcome

| Parameter | |
| :--- | :--- |
| `message` | the message to log |
| **returns** | the write report, suppressed below the global level, failed when the clock cannot be sampled or the record cannot be encoded, rejected with too_large past MAX_RECORD_BYTES, otherwise the outcome of one write to the global writer or standard error |

### warn_report

```mach
pub fun warn_report(message: str) std.log.sink.WriteReport
```

write a message at WARN through the global writer and report the outcome

| Parameter | |
| :--- | :--- |
| `message` | the message to log |
| **returns** | the write report, suppressed below the global level, failed when the clock cannot be sampled or the record cannot be encoded, rejected with too_large past MAX_RECORD_BYTES, otherwise the outcome of one write to the global writer or standard error |

### error_report

```mach
pub fun error_report(message: str) std.log.sink.WriteReport
```

write a message at ERROR through the global writer and report the outcome

| Parameter | |
| :--- | :--- |
| `message` | the message to log |
| **returns** | the write report, suppressed below the global level, failed when the clock cannot be sampled or the record cannot be encoded, rejected with too_large past MAX_RECORD_BYTES, otherwise the outcome of one write to the global writer or standard error |

### debug

```mach
pub fun debug(message: str)
```

write a message at DEBUG through the global writer, discarding the report

| Parameter | |
| :--- | :--- |
| `message` | the message to log |

### info

```mach
pub fun info(message: str)
```

write a message at INFO through the global writer, discarding the report

| Parameter | |
| :--- | :--- |
| `message` | the message to log |

### warn

```mach
pub fun warn(message: str)
```

write a message at WARN through the global writer, discarding the report

| Parameter | |
| :--- | :--- |
| `message` | the message to log |

### error

```mach
pub fun error(message: str)
```

write a message at ERROR through the global writer, discarding the report

| Parameter | |
| :--- | :--- |
| `message` | the message to log |

## Forwards

### MAX_RECORD_BYTES

Forwards [`std.log.record.MAX_RECORD_BYTES`](log/record.md#constants).

```mach
pub val MAX_RECORD_BYTES:    usize = 8192
```

### MIN_TRUNCATED_BYTES

Forwards [`std.log.record.MIN_TRUNCATED_BYTES`](log/record.md#constants).

```mach
pub val MIN_TRUNCATED_BYTES: usize = 15
```

### Level

Forwards [`std.log.record.Level`](log/record.md#level).

```mach
pub def Level: u8
```

### DEBUG

Forwards [`std.log.record.DEBUG`](log/record.md#level).

```mach
pub val DEBUG: Level = 0
```

### INFO

Forwards [`std.log.record.INFO`](log/record.md#level).

```mach
pub val INFO:  Level = 1
```

### WARN

Forwards [`std.log.record.WARN`](log/record.md#level).

```mach
pub val WARN:  Level = 2
```

### ERROR

Forwards [`std.log.record.ERROR`](log/record.md#level).

```mach
pub val ERROR: Level = 3
```

### OFF

Forwards [`std.log.record.OFF`](log/record.md#level).

```mach
pub val OFF:   Level = 4
```

### Precision

Forwards [`std.log.record.Precision`](log/record.md#precision).

```mach
pub def Precision: u8
```

### PRECISION_SECONDS

Forwards [`std.log.record.PRECISION_SECONDS`](log/record.md#precision).

```mach
pub val PRECISION_SECONDS: Precision = 0
```

### PRECISION_MILLIS

Forwards [`std.log.record.PRECISION_MILLIS`](log/record.md#precision).

```mach
pub val PRECISION_MILLIS:  Precision = 1
```

### PRECISION_MICROS

Forwards [`std.log.record.PRECISION_MICROS`](log/record.md#precision).

```mach
pub val PRECISION_MICROS:  Precision = 2
```

### PRECISION_NANOS

Forwards [`std.log.record.PRECISION_NANOS`](log/record.md#precision).

```mach
pub val PRECISION_NANOS:   Precision = 3
```

### ClockOwnership

Forwards [`std.log.record.ClockOwnership`](log/record.md#clockownership).

```mach
pub def ClockOwnership: u8
```

### CLOCK_CONTEXT_NONE

Forwards [`std.log.record.CLOCK_CONTEXT_NONE`](log/record.md#clockownership).

```mach
pub val CLOCK_CONTEXT_NONE:     ClockOwnership = 0
```

### CLOCK_CONTEXT_BORROWED

Forwards [`std.log.record.CLOCK_CONTEXT_BORROWED`](log/record.md#clockownership).

```mach
pub val CLOCK_CONTEXT_BORROWED: ClockOwnership = 1
```

### NowFun

Forwards [`std.log.record.NowFun`](log/record.md#nowfun).

```mach
pub def NowFun: fun(ptr) std.chrono.time.Clock
```

a clock source samples the current time or reports why it could not

### ClockError

Forwards [`std.log.record.ClockError`](log/record.md#clockerror).

```mach
pub tag ClockError: u8 {
    invalid;
    read: std.io.error.Error;
}
```

every way a sample can fail

### Sample

Forwards [`std.log.record.Sample`](log/record.md#sample).

```mach
pub def Sample: res[Time, ClockError]
```

the outcome of one sample, normalized to the clock's precision

### Clock

Forwards [`std.log.record.Clock`](log/record.md#clock-1).

```mach
pub rec Clock {
    ctx:       ptr;
    fn_now:    NowFun;
    precision: Precision;
    ownership: ClockOwnership;
}
```

the clock context is borrowed and must outlive every logger using it

### FieldKind

Forwards [`std.log.record.FieldKind`](log/record.md#fieldkind).

```mach
pub def FieldKind: u8
```

### FIELD_I64

Forwards [`std.log.record.FIELD_I64`](log/record.md#fieldkind).

```mach
pub val FIELD_I64:    FieldKind = 0
```

### FIELD_U64

Forwards [`std.log.record.FIELD_U64`](log/record.md#fieldkind).

```mach
pub val FIELD_U64:    FieldKind = 1
```

### FIELD_BOOL

Forwards [`std.log.record.FIELD_BOOL`](log/record.md#fieldkind).

```mach
pub val FIELD_BOOL:   FieldKind = 2
```

### FIELD_BYTES

Forwards [`std.log.record.FIELD_BYTES`](log/record.md#fieldkind).

```mach
pub val FIELD_BYTES:  FieldKind = 3
```

### FIELD_STRING

Forwards [`std.log.record.FIELD_STRING`](log/record.md#fieldkind).

```mach
pub val FIELD_STRING: FieldKind = 4
```

### FIELD_ERROR

Forwards [`std.log.record.FIELD_ERROR`](log/record.md#fieldkind).

```mach
pub val FIELD_ERROR:  FieldKind = 5
```

### Bytes

Forwards [`std.log.record.Bytes`](log/record.md#bytes).

```mach
pub rec Bytes {
    data: *u8;
    len:  usize;
}
```

a borrowed run of bytes

### Field

Forwards [`std.log.record.Field`](log/record.md#field).

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

### Record

Forwards [`std.log.record.Record`](log/record.md#record).

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

### OversizePolicy

Forwards [`std.log.record.OversizePolicy`](log/record.md#oversizepolicy).

```mach
pub def OversizePolicy: u8
```

### OVERSIZE_REJECT

Forwards [`std.log.record.OVERSIZE_REJECT`](log/record.md#oversizepolicy).

```mach
pub val OVERSIZE_REJECT:   OversizePolicy = 0
```

### OVERSIZE_TRUNCATE

Forwards [`std.log.record.OVERSIZE_TRUNCATE`](log/record.md#oversizepolicy).

```mach
pub val OVERSIZE_TRUNCATE: OversizePolicy = 1
```

### EncodeError

Forwards [`std.log.record.EncodeError`](log/record.md#encodeerror).

```mach
pub tag EncodeError: u8 {
    invalid;
    buffer: usize;
    limit;
}
```

every way an encoding can fail; nothing is emitted on any of them

### EncodeStatus

Forwards [`std.log.record.EncodeStatus`](log/record.md#encodestatus).

```mach
pub tag EncodeStatus: u8 {
    encoded;
    truncated;
    rejected;
    failed: EncodeError;
}
```

the outcome of one encoding

### Encoded

Forwards [`std.log.record.Encoded`](log/record.md#encoded).

```mach
pub rec Encoded {
    status:   EncodeStatus;
    len:      usize;
    required: usize;
}
```

len is the bytes emitted; required is the full record's size whenever the
record was valid enough to measure, zero otherwise

### system_clock

Forwards [`std.log.record.system_clock`](log/record.md#system_clock).

Only where `capability.HAS_CLOCK`.

```mach
pub fun system_clock(precision: Precision) Clock
```

a clock reading the system time, with no context

### clock

Forwards [`std.log.record.clock`](log/record.md#clock).

```mach
pub fun clock(ctx: ptr, fn_now: NowFun, precision: Precision) Clock
```

a clock over a caller's source, borrowing its context

### clock_valid

Forwards [`std.log.record.clock_valid`](log/record.md#clock_valid).

```mach
pub fun clock_valid(c: *Clock) bool
```

tell whether a clock can be sampled

### clock_now

Forwards [`std.log.record.clock_now`](log/record.md#clock_now).

```mach
pub fun clock_now(c: *Clock) Sample
```

sample the clock; a failed clock is never zero time

### record_at

Forwards [`std.log.record.record_at`](log/record.md#record_at).

```mach
pub fun record_at(timestamp: Time, precision: Precision, level: Level, message: str, fields: *Field, field_count: usize) Record
```

build a record stamped with a given time, truncated to the precision

### field_i64

Forwards [`std.log.record.field_i64`](log/record.md#field_i64).

```mach
pub fun field_i64(key: str, value: i64) Field
```

a field carrying a signed integer

### field_u64

Forwards [`std.log.record.field_u64`](log/record.md#field_u64).

```mach
pub fun field_u64(key: str, value: u64) Field
```

a field carrying an unsigned integer

### field_bool

Forwards [`std.log.record.field_bool`](log/record.md#field_bool).

```mach
pub fun field_bool(key: str, value: bool) Field
```

a field carrying a boolean

### field_bytes

Forwards [`std.log.record.field_bytes`](log/record.md#field_bytes).

```mach
pub fun field_bytes(key: str, data: *u8, len: usize) Field
```

a field carrying raw bytes, rendered as hex

### field_string

Forwards [`std.log.record.field_string`](log/record.md#field_string).

```mach
pub fun field_string(key: str, value: str) Field
```

a field carrying a terminated string, rendered quoted

### field_error

Forwards [`std.log.record.field_error`](log/record.md#field_error).

```mach
pub fun field_error(key: str, value: std.io.error.Error) Field
```

a field carrying an io error

### level_name

Forwards [`std.log.record.level_name`](log/record.md#level_name).

```mach
pub fun level_name(level: Level) str
```

the name a level renders as in a record

### encode_record

Forwards [`std.log.record.encode`](log/record.md#encode).

```mach
pub fun encode(record: *Record, data: *u8, cap: usize, limit: usize, policy: OversizePolicy) Encoded
```

encode one record into caller-owned storage

reject emits no bytes. truncate retains whole leading tokens and appends
truncated=true, so the result remains a complete logfmt line.

### SinkError

Forwards [`std.log.sink.SinkError`](log/sink.md#sinkerror), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub tag SinkError: u8 {
    invalid;
    contract;
    malformed;
    clock:     std.log.record.ClockError;
    encode:    std.log.record.EncodeError;
    too_large: usize;
    write:     WriteError;
    queue_full;
    queue_closed;
    open;
    unjoined;
    busy;
    queue:  std.sync.channel.StateError;
    thread: std.sync.thread.ThreadError;
}
```

every way a sink, a logger or one publication can fail

### Created

Forwards [`std.log.sink.Created`](log/sink.md#created), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub def Created: res[Sink, SinkError]
```

a made sink, or why it could not be made

### Operation

Forwards [`std.log.sink.Operation`](log/sink.md#operation), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub def Operation: err[SinkError]
```

a state operation's outcome

### Aborted

Forwards [`std.log.sink.Aborted`](log/sink.md#aborted), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub def Aborted: res[usize, SinkError]
```

an abort's outcome: the undelivered records transferred to the caller

### WriteStatus

Forwards [`std.log.sink.WriteStatus`](log/sink.md#writestatus), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub tag WriteStatus: u8 {
    persisted;
    partial:  SinkError;
    failed:   SinkError;
    rejected: SinkError;
    dropped;
    enqueued;
    suppressed;
}
```

the outcome of one publication; the cases that failed carry their cause

### WriteReport

Forwards [`std.log.sink.WriteReport`](log/sink.md#writereport), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub rec WriteReport {
    status:    WriteStatus;
    offered:   usize;
    persisted: usize;
    truncated: bool;
}
```

offered is the full logical size before truncation
persisted is the byte count confirmed by the adapter

### Delivery

Forwards [`std.log.sink.Delivery`](log/sink.md#delivery), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub def Delivery: u8
```

### DELIVERY_DIRECT

Forwards [`std.log.sink.DELIVERY_DIRECT`](log/sink.md#delivery), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val DELIVERY_DIRECT:         Delivery = 0
```

### DELIVERY_BOUNDED_QUEUED

Forwards [`std.log.sink.DELIVERY_BOUNDED_QUEUED`](log/sink.md#delivery), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val DELIVERY_BOUNDED_QUEUED: Delivery = 1
```

### OverloadPolicy

Forwards [`std.log.sink.OverloadPolicy`](log/sink.md#overloadpolicy), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub def OverloadPolicy: u8
```

### OVERLOAD_REJECT_NEW

Forwards [`std.log.sink.OVERLOAD_REJECT_NEW`](log/sink.md#overloadpolicy), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val OVERLOAD_REJECT_NEW: OverloadPolicy = 0
```

### OVERLOAD_DROP_NEW

Forwards [`std.log.sink.OVERLOAD_DROP_NEW`](log/sink.md#overloadpolicy), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val OVERLOAD_DROP_NEW:   OverloadPolicy = 1
```

### OVERLOAD_BLOCK

Forwards [`std.log.sink.OVERLOAD_BLOCK`](log/sink.md#overloadpolicy), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val OVERLOAD_BLOCK:      OverloadPolicy = 2
```

### AdapterKind

Forwards [`std.log.sink.AdapterKind`](log/sink.md#adapterkind), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub def AdapterKind: u8
```

### ADAPTER_CONSOLE

Forwards [`std.log.sink.ADAPTER_CONSOLE`](log/sink.md#adapterkind), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val ADAPTER_CONSOLE: AdapterKind = 0
```

### ADAPTER_PIPE

Forwards [`std.log.sink.ADAPTER_PIPE`](log/sink.md#adapterkind), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val ADAPTER_PIPE:    AdapterKind = 1
```

### ADAPTER_FILE

Forwards [`std.log.sink.ADAPTER_FILE`](log/sink.md#adapterkind), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val ADAPTER_FILE:    AdapterKind = 2
```

### ADAPTER_CUSTOM

Forwards [`std.log.sink.ADAPTER_CUSTOM`](log/sink.md#adapterkind), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub val ADAPTER_CUSTOM:  AdapterKind = 3
```

### Contract

Forwards [`std.log.sink.Contract`](log/sink.md#contract), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub rec Contract {
    delivery:            Delivery;
    max_record:          usize;
    oversize:            std.log.record.OversizePolicy;
    adapter:             AdapterKind;
    target_atomic_limit: usize;
    queue_capacity:      usize;
    overload:            OverloadPolicy;
}
```

target_atomic_limit is zero when the target offers no cross-process limit
every direct adapter still serializes callbacks within this process

### PublishFun

Forwards [`std.log.sink.PublishFun`](log/sink.md#publishfun), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub def PublishFun: fun(ptr, *u8, usize) WriteReport
```

### Sink

Forwards [`std.log.sink.Sink`](log/sink.md#sink), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub rec Sink {
    ctx:        ptr;
    fn_publish: PublishFun;
    contract:   Contract;
}
```

sink ctx is borrowed and must outlive every publish
publish callbacks must consume or copy the borrowed bytes before returning

### Direct

Forwards [`std.log.sink.Direct`](log/sink.md#direct), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub rec Direct {
    lock:        std.sync.mutex.Mutex;
    adapter_ctx: ptr;
    fn_write:    PublishFun;
    writer:      std.io.writer.Writer;
    initialized: bool;
}
```

direct sinks must remain at a stable address and must not be copied in use
reinitialization requires every current publication to stop first
existing sinks retarget to the new adapter but retain their copied contract and must be discarded
direct owns no resources and requires no destruction

### QueuedRecord

Forwards [`std.log.sink.QueuedRecord`](log/sink.md#queuedrecord), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub rec QueuedRecord {
    data: [record.MAX_RECORD_BYTES]u8;
    len:  usize;
}
```

one encoded record held in a queued sink's storage

### QueueStats

Forwards [`std.log.sink.QueueStats`](log/sink.md#queuestats), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub rec QueueStats {
    enqueued:  usize;
    persisted: usize;
    partial:   usize;
    failed:    usize;
    rejected:  usize;
    dropped:   usize;
    aborted:   usize;
    last:      WriteReport;
}
```

a snapshot of a queued sink's counters

### Queued

Forwards [`std.log.sink.Queued`](log/sink.md#queued), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub rec Queued {
    queue:       std.sync.channel.Channel[QueuedRecord];
    downstream:  *Sink;
    worker:      std.sync.thread.Thread;
    overload:    OverloadPolicy;
    enqueued:    i64;
    persisted:   i64;
    partial:     i64;
    failed:      i64;
    rejected:    i64;
    dropped:     i64;
    aborted:     i64;
    last:        WriteReport;
    lock:        std.sync.mutex.Mutex;
    state_lock:  std.sync.mutex.Mutex;
    joined:      std.sync.condition.Condition;
    initialized: bool;
    join_state:  i64;
    join_error:  std.sync.thread.ThreadError;
}
```

queued and its caller-owned records remain stable through join

### report

Forwards [`std.log.sink.report`](log/sink.md#report), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun report(status: WriteStatus, offered: usize, persisted: usize, truncated: bool) WriteReport
```

assemble a write report

### persisted

Forwards [`std.log.sink.persisted`](log/sink.md#persisted), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun persisted(bytes: usize) WriteReport
```

a report for a publication the adapter fully confirmed

### partial

Forwards [`std.log.sink.partial`](log/sink.md#partial), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun partial(offered: usize, persisted_bytes: usize, error: SinkError) WriteReport
```

a report for a publication the adapter confirmed only in part

### failed

Forwards [`std.log.sink.failed`](log/sink.md#failed), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun failed(offered: usize, persisted_bytes: usize, error: SinkError) WriteReport
```

a report for a publication that failed

### rejected

Forwards [`std.log.sink.rejected`](log/sink.md#rejected), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun rejected(offered: usize, error: SinkError) WriteReport
```

a report for a publication nothing accepted, leaving the record with the caller

### dropped

Forwards [`std.log.sink.dropped`](log/sink.md#dropped), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun dropped(offered: usize) WriteReport
```

a report for a record a queue discarded under OVERLOAD_DROP_NEW

### enqueued

Forwards [`std.log.sink.enqueued`](log/sink.md#enqueued), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun enqueued(offered: usize) WriteReport
```

a report for a record a queue accepted for later publication

### suppressed

Forwards [`std.log.sink.suppressed`](log/sink.md#suppressed), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun suppressed() WriteReport
```

a report for a record below the level that was never encoded

### cause

Forwards [`std.log.sink.cause`](log/sink.md#cause), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun cause(r: WriteReport) opt[SinkError]
```

the cause carried by a report, or none for the cases that have no failure

### report_write

Forwards [`std.log.sink.report_write`](log/sink.md#report_write), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun report_write(len: usize, outcome: res[usize, WriteError]) WriteReport
```

fold a writer outcome into a report: the persisted prefix is kept and the
writer's failure is the cause; a short accept is the stalled prefix

### contract_valid

Forwards [`std.log.sink.contract_valid`](log/sink.md#contract_valid), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun contract_valid(contract: Contract) bool
```

tell whether a delivery contract is consistent

### queued_contract

Forwards [`std.log.sink.queued_contract`](log/sink.md#queued_contract), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued_contract(max_record: usize, oversize: std.log.record.OversizePolicy, capacity: usize, overload: OverloadPolicy, adapter: AdapterKind, target_atomic_limit: usize) res[Contract, SinkError]
```

describe a bounded queued delivery contract

### sink_make

Forwards [`std.log.sink.make`](log/sink.md#make), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun make(ctx: ptr, fn_publish: PublishFun, contract: Contract) Created
```

construct a sink from an implementation and a validated contract

### sink_publish

Forwards [`std.log.sink.publish`](log/sink.md#publish), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun publish(sink: *Sink, data: *u8, len: usize) WriteReport
```

publish one encoded record through a sink and check the adapter kept its contract

### direct_custom

Forwards [`std.log.sink.custom`](log/sink.md#custom), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun custom(direct: *Direct, ctx: ptr, fn_write: PublishFun, max_record: usize, oversize: std.log.record.OversizePolicy, target_atomic_limit: usize) Created
```

ctx is borrowed and must outlive direct and every sink created from it
the custom callback is serialized by direct before each invocation

### direct_writer

Forwards [`std.log.sink.from_writer`](log/sink.md#from_writer), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun from_writer(direct: *Direct, output: std.io.writer.Writer, max_record: usize, oversize: std.log.record.OversizePolicy, target_atomic_limit: usize) Created
```

the writer value is copied while its ctx remains borrowed for every sink created from direct
io writers report a failed call or a partial successful call

### direct_console

Forwards [`std.log.sink.console`](log/sink.md#console), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun console(direct: *Direct, stderr: bool, max_record: usize, oversize: std.log.record.OversizePolicy) Created
```

consoles guarantee one in-process callback but no cross-process byte limit

### direct_file

Forwards [`std.log.sink.file`](log/sink.md#file), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun file(direct: *Direct, output: std.filesystem.File, max_record: usize, oversize: std.log.record.OversizePolicy) Created
```

the caller owns the file handle and closes it only after sink use stops
regular files guarantee one in-process callback but no cross-process limit

### direct_pipe

Forwards [`std.log.sink.pipe`](log/sink.md#pipe), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun pipe(direct: *Direct, output: std.filesystem.File, max_record: usize, oversize: std.log.record.OversizePolicy) Created
```

linux pipe writes through 4096 bytes are cross-process atomic
darwin exposes the posix minimum of 512 bytes through this contract
windows anonymous byte pipes publish once but expose no portable byte limit
the caller owns the pipe handle and closes it only after sink use stops

### pipe_target_atomic_limit

Forwards [`std.log.sink.pipe_target_atomic_limit`](log/sink.md#pipe_target_atomic_limit), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun pipe_target_atomic_limit() usize
```

the byte count a pipe write is atomic across processes on the build target

### queued_sink

Forwards [`std.log.sink.queued`](log/sink.md#queued-1), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued(queued: *Queued, storage: *QueuedRecord, capacity: usize, downstream: *Sink, max_record: usize, oversize: std.log.record.OversizePolicy, overload: OverloadPolicy) Created
```

initialize a queued sink in place with the default worker thread configuration

### queued_sink_with_config

Forwards [`std.log.sink.queued_with_config`](log/sink.md#queued_with_config), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued_with_config(queued: *Queued, storage: *QueuedRecord, capacity: usize, downstream: *Sink, max_record: usize, oversize: std.log.record.OversizePolicy, overload: OverloadPolicy, config: *std.sync.thread.Config) Created
```

initialize the queued sink in place: queued is address-bound and stays
uninitialized after any refusal, with the channel released

the downstream sink and every borrowed adapter context outlive queued join
downstream publication failure is recorded and does not stop queue service

### queued_close_drain

Forwards [`std.log.sink.queued_close_drain`](log/sink.md#queued_close_drain), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued_close_drain(queued: *Queued) Operation
```

stop accepting records; the worker drains what was enqueued. idempotent

### queued_close_abort

Forwards [`std.log.sink.queued_close_abort`](log/sink.md#queued_close_abort), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued_close_abort(queued: *Queued, rejected_storage: *QueuedRecord, rejected_capacity: usize) Aborted
```

abort transfers every unpublished record to caller storage in fifo order

### queued_join

Forwards [`std.log.sink.queued_join`](log/sink.md#queued_join), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued_join(queued: *Queued) Operation
```

wait for the worker after close; concurrent joins share one native join and
a failed join is replayed to every later caller
downstream callbacks must not join their own queue

### queued_stats

Forwards [`std.log.sink.queued_stats`](log/sink.md#queued_stats), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued_stats(queued: *Queued) QueueStats
```

snapshot a queued sink's counters

### queued_thread_error

Forwards [`std.log.sink.queued_thread_error`](log/sink.md#queued_thread_error), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued_thread_error(queued: *Queued) i64
```

the native code of the worker's join failure, 0 when the join succeeded or
has not run, ERROR_INVALID for a sink that was never made

### queued_dnit

Forwards [`std.log.sink.queued_dnit`](log/sink.md#queued_dnit), only where `capability.HAS_CLOCK && capability.HAS_FILES && capability.HAS_THREADS`.

```mach
pub fun queued_dnit(queued: *Queued) Operation
```

release the queue after a completed join; refused while joiners wait

