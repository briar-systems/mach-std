[std](../README.md) / [log](README.md) / **sink**

# std.log.sink

serialized record sinks with direct atomic publication

Source: [`src/log/sink.mach`](../../../src/log/sink.mach)

Uses types from [`std.filesystem`](../filesystem.md), [`std.io.writer`](../io/writer.md), [`std.log.record`](record.md), [`std.sync.channel`](../sync/channel.md), [`std.sync.condition`](../sync/condition.md), [`std.sync.mutex`](../sync/mutex.md), [`std.sync.thread`](../sync/thread.md).

| Type | | |
| :--- | :--- | :--- |
| [`SinkError`](#sinkerror) | `tag` | every way a sink, a logger or one publication can fail |
| [`Created`](#created) | `def` | a made sink, or why it could not be made |
| [`Operation`](#operation) | `def` | a state operation's outcome |
| [`Aborted`](#aborted) | `def` | an abort's outcome: the undelivered records transferred to the caller |
| [`WriteStatus`](#writestatus) | `tag` | the outcome of one publication; the cases that failed carry their cause |
| [`WriteReport`](#writereport) | `rec` | offered is the full logical size before truncation persisted is the byte count confirmed by the adapter |
| [`Delivery`](#delivery) | `def` |  |
| [`OverloadPolicy`](#overloadpolicy) | `def` |  |
| [`AdapterKind`](#adapterkind) | `def` |  |
| [`Contract`](#contract) | `rec` | target_atomic_limit is zero when the target offers no cross-process limit every direct adapter still serializes callbacks within this process |
| [`PublishFun`](#publishfun) | `def` |  |
| [`Sink`](#sink) | `rec` | sink ctx is borrowed and must outlive every publish publish callbacks must consume or copy the borrowed bytes before returning |
| [`Direct`](#direct) | `rec` | direct sinks must remain at a stable address and must not be copied in use reinitialization requires every current publication to stop first existing sinks retarget to the new adapter but retain their copied contract and must be discarded direct owns no resources and requires no destruction |
| [`QueuedRecord`](#queuedrecord) | `rec` |  |
| [`QueueStats`](#queuestats) | `rec` |  |
| [`Queued`](#queued) | `rec` | queued and its caller-owned records remain stable through join |

| On `SinkError` | |
| :--- | :--- |
| [`partial`](#partial), [`failed`](#failed), [`rejected`](#rejected) | |

| On `WriteStatus` | |
| :--- | :--- |
| [`report`](#report) | |

| On `WriteReport` | |
| :--- | :--- |
| [`persisted`](#persisted), [`dropped`](#dropped), [`enqueued`](#enqueued), [`suppressed`](#suppressed) | |
| [`cause`](#cause) | the cause carried by a report, or none for the cases that have no failure |
| [`report_write`](#report_write) | fold a writer outcome into a report: the persisted prefix is kept and the writer's failure is the cause; a short accept is the stalled prefix |

| On `Delivery` | |
| :--- | :--- |
| [`DELIVERY_DIRECT`](#delivery), [`DELIVERY_BOUNDED_QUEUED`](#delivery) | |

| On `OverloadPolicy` | |
| :--- | :--- |
| [`OVERLOAD_REJECT_NEW`](#overloadpolicy), [`OVERLOAD_DROP_NEW`](#overloadpolicy), [`OVERLOAD_BLOCK`](#overloadpolicy) | |
| [`queued_contract`](#queued_contract) | describe a bounded queued delivery contract |

| On `AdapterKind` | |
| :--- | :--- |
| [`ADAPTER_CONSOLE`](#adapterkind), [`ADAPTER_PIPE`](#adapterkind), [`ADAPTER_FILE`](#adapterkind), [`ADAPTER_CUSTOM`](#adapterkind) | |

| On `Contract` | |
| :--- | :--- |
| [`contract_valid`](#contract_valid) | |

| On `PublishFun` | |
| :--- | :--- |
| [`make`](#make) | construct a sink from an implementation and a validated contract |

| On `Sink` | |
| :--- | :--- |
| [`publish`](#publish) | |

| On `Direct` | |
| :--- | :--- |
| [`custom`](#custom) | ctx is borrowed and must outlive direct and every sink created from it the custom callback is serialized by direct before each invocation |
| [`from_writer`](#from_writer) | the writer value is copied while its ctx remains borrowed for every sink created from direct io writers report a failed call or a partial successful call |
| [`console`](#console) | consoles guarantee one in-process callback but no cross-process byte limit |
| [`file`](#file) | the caller owns the file handle and closes it only after sink use stops regular files guarantee one in-process callback but no cross-process limit |
| [`pipe`](#pipe) | linux pipe writes through 4096 bytes are cross-process atomic darwin exposes the posix minimum of 512 bytes through this contract windows anonymous byte pipes publish once but expose no portable byte limit the caller owns the pipe handle and closes it only after sink use stops |

| On `Queued` | |
| :--- | :--- |
| [`queued_with_config`](#queued_with_config) | initialize the queued sink in place: queued is address-bound and stays uninitialized after any refusal, with the channel released |
| [`queued`](#queued-1) | |
| [`queued_close_drain`](#queued_close_drain) | stop accepting records; the worker drains what was enqueued |
| [`queued_close_abort`](#queued_close_abort) | abort transfers every unpublished record to caller storage in fifo order |
| [`queued_join`](#queued_join) | wait for the worker after close; concurrent joins share one native join and a failed join is replayed to every later caller downstream callbacks must not join their own queue |
| [`queued_stats`](#queued_stats) | |
| [`queued_thread_error`](#queued_thread_error) | the native code of the worker's join failure, 0 when the join succeeded or has not run, ERROR_INVALID for a sink that was never made |
| [`queued_dnit`](#queued_dnit) | release the queue after a completed join; refused while joiners wait |

| Functions | |
| :--- | :--- |
| [`pipe_target_atomic_limit`](#pipe_target_atomic_limit) | |

---

## SinkError

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

| Case | Payload | |
| :--- | :--- | :--- |
| `invalid` |  | a nil, uninitialized or malformed argument, or a sink that was never made |
| `contract` |  | the delivery contract's parameters are inconsistent |
| `malformed` |  | an adapter's report broke the delivery contract |
| `clock` | `std.log.record.ClockError` | the logger's clock could not be sampled; nothing was published |
| `encode` | `std.log.record.EncodeError` | the record could not be encoded; nothing was published |
| `too_large` | `usize` | the record exceeds the contract's max_record; payload is its size and nothing was published |
| `write` | `WriteError` | the adapter's write failed; payload carries the persisted prefix and the cause |
| `queue_full` |  | the bounded queue had no capacity under OVERLOAD_REJECT_NEW |
| `queue_closed` |  | the queue no longer accepts records |
| `open` |  | the queue must be closed before it is joined |
| `unjoined` |  | the queue must be joined before it is destroyed |
| `busy` |  | joiners are still waiting on the queue |
| `queue` | `std.sync.channel.StateError` | the queue refused a state operation |
| `thread` | `std.sync.thread.ThreadError` | the worker could not be spawned or joined |

### partial

```mach
pub fun partial(offered: usize, persisted_bytes: usize, error: SinkError) WriteReport
```

### failed

```mach
pub fun failed(offered: usize, persisted_bytes: usize, error: SinkError) WriteReport
```

### rejected

```mach
pub fun rejected(offered: usize, error: SinkError) WriteReport
```

## Created

```mach
pub def Created: res[Sink, SinkError]
```

a made sink, or why it could not be made

## Operation

```mach
pub def Operation: err[SinkError]
```

a state operation's outcome

## Aborted

```mach
pub def Aborted: res[usize, SinkError]
```

an abort's outcome: the undelivered records transferred to the caller

## WriteStatus

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

| Case | Payload | |
| :--- | :--- | :--- |
| `persisted` |  | every offered byte was confirmed by the adapter |
| `partial` | `SinkError` | the adapter confirmed a prefix and then stalled or failed |
| `failed` | `SinkError` | the adapter failed; the confirmed prefix may be zero |
| `rejected` | `SinkError` | nothing was accepted (too large, queue full or closed, or an encoding refusal); the caller retains the record |
| `dropped` |  | the queue discarded the record under OVERLOAD_DROP_NEW |
| `enqueued` |  | the queue accepted the record for later publication |
| `suppressed` |  | the record was below the level and never encoded |

### report

```mach
pub fun report(status: WriteStatus, offered: usize, persisted: usize, truncated: bool) WriteReport
```

## WriteReport

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

### persisted

```mach
pub fun persisted(bytes: usize) WriteReport
```

### dropped

```mach
pub fun dropped(offered: usize) WriteReport
```

### enqueued

```mach
pub fun enqueued(offered: usize) WriteReport
```

### suppressed

```mach
pub fun suppressed() WriteReport
```

### cause

```mach
pub fun cause(r: WriteReport) opt[SinkError]
```

the cause carried by a report, or none for the cases that have no failure

### report_write

```mach
pub fun report_write(len: usize, outcome: res[usize, WriteError]) WriteReport
```

fold a writer outcome into a report: the persisted prefix is kept and the
writer's failure is the cause; a short accept is the stalled prefix

## Delivery

```mach
pub def Delivery: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `DELIVERY_DIRECT` | `0` |  |
| `DELIVERY_BOUNDED_QUEUED` | `1` |  |

## OverloadPolicy

```mach
pub def OverloadPolicy: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `OVERLOAD_REJECT_NEW` | `0` |  |
| `OVERLOAD_DROP_NEW` | `1` |  |
| `OVERLOAD_BLOCK` | `2` |  |

### queued_contract

```mach
pub fun queued_contract(max_record: usize, oversize: std.log.record.OversizePolicy, capacity: usize, overload: OverloadPolicy, adapter: AdapterKind, target_atomic_limit: usize) res[Contract, SinkError]
```

describe a bounded queued delivery contract

## AdapterKind

```mach
pub def AdapterKind: u8
```

| Name | Value | |
| :--- | :--- | :--- |
| `ADAPTER_CONSOLE` | `0` |  |
| `ADAPTER_PIPE` | `1` |  |
| `ADAPTER_FILE` | `2` |  |
| `ADAPTER_CUSTOM` | `3` |  |

## Contract

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

### contract_valid

```mach
pub fun contract_valid(contract: Contract) bool
```

## PublishFun

```mach
pub def PublishFun: fun(ptr, *u8, usize) WriteReport
```

### make

```mach
pub fun make(ctx: ptr, f_publish: PublishFun, contract: Contract) Created
```

construct a sink from an implementation and a validated contract

## Sink

```mach
pub rec Sink {
    ctx:       ptr;
    f_publish: PublishFun;
    contract:  Contract;
}
```

sink ctx is borrowed and must outlive every publish
publish callbacks must consume or copy the borrowed bytes before returning

### publish

```mach
pub fun publish(sink: *Sink, data: *u8, len: usize) WriteReport
```

## Direct

```mach
pub rec Direct {
    lock:        std.sync.mutex.Mutex;
    adapter_ctx: ptr;
    f_write:     PublishFun;
    writer:      std.io.writer.Writer;
    initialized: bool;
}
```

direct sinks must remain at a stable address and must not be copied in use
reinitialization requires every current publication to stop first
existing sinks retarget to the new adapter but retain their copied contract and must be discarded
direct owns no resources and requires no destruction

### custom

```mach
pub fun custom(direct: *Direct, ctx: ptr, f_write: PublishFun, max_record: usize, oversize: std.log.record.OversizePolicy, target_atomic_limit: usize) Created
```

ctx is borrowed and must outlive direct and every sink created from it
the custom callback is serialized by direct before each invocation

### from_writer

```mach
pub fun from_writer(direct: *Direct, output: std.io.writer.Writer, max_record: usize, oversize: std.log.record.OversizePolicy, target_atomic_limit: usize) Created
```

the writer value is copied while its ctx remains borrowed for every sink created from direct
io writers report a failed call or a partial successful call

### console

```mach
pub fun console(direct: *Direct, stderr: bool, max_record: usize, oversize: std.log.record.OversizePolicy) Created
```

consoles guarantee one in-process callback but no cross-process byte limit

### file

```mach
pub fun file(direct: *Direct, output: std.filesystem.File, max_record: usize, oversize: std.log.record.OversizePolicy) Created
```

the caller owns the file handle and closes it only after sink use stops
regular files guarantee one in-process callback but no cross-process limit

### pipe

```mach
pub fun pipe(direct: *Direct, output: std.filesystem.File, max_record: usize, oversize: std.log.record.OversizePolicy) Created
```

linux pipe writes through 4096 bytes are cross-process atomic
darwin exposes the posix minimum of 512 bytes through this contract
windows anonymous byte pipes publish once but expose no portable byte limit
the caller owns the pipe handle and closes it only after sink use stops

## QueuedRecord

```mach
pub rec QueuedRecord {
    data: [record.MAX_RECORD_BYTES]u8;
    len:  usize;
}
```

## QueueStats

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

## Queued

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

### queued_with_config

```mach
pub fun queued_with_config(queued: *Queued, storage: *QueuedRecord, capacity: usize, downstream: *Sink, max_record: usize, oversize: std.log.record.OversizePolicy, overload: OverloadPolicy, config: *std.sync.thread.Config) Created
```

initialize the queued sink in place: queued is address-bound and stays
uninitialized after any refusal, with the channel released

the downstream sink and every borrowed adapter context outlive queued join
downstream publication failure is recorded and does not stop queue service

### queued

```mach
pub fun queued(queued: *Queued, storage: *QueuedRecord, capacity: usize, downstream: *Sink, max_record: usize, oversize: std.log.record.OversizePolicy, overload: OverloadPolicy) Created
```

### queued_close_drain

```mach
pub fun queued_close_drain(queued: *Queued) Operation
```

stop accepting records; the worker drains what was enqueued. idempotent

### queued_close_abort

```mach
pub fun queued_close_abort(queued: *Queued, rejected_storage: *QueuedRecord, rejected_capacity: usize) Aborted
```

abort transfers every unpublished record to caller storage in fifo order

| Parameter | |
| :--- | :--- |
| **returns** | the records transferred, or invalid when the storage cannot hold them (the queue keeps them) |

### queued_join

```mach
pub fun queued_join(queued: *Queued) Operation
```

wait for the worker after close; concurrent joins share one native join and
a failed join is replayed to every later caller
downstream callbacks must not join their own queue

### queued_stats

```mach
pub fun queued_stats(queued: *Queued) QueueStats
```

### queued_thread_error

```mach
pub fun queued_thread_error(queued: *Queued) i64
```

the native code of the worker's join failure, 0 when the join succeeded or
has not run, ERROR_INVALID for a sink that was never made

### queued_dnit

```mach
pub fun queued_dnit(queued: *Queued) Operation
```

release the queue after a completed join; refused while joiners wait

## Functions

### pipe_target_atomic_limit

```mach
pub fun pipe_target_atomic_limit() usize
```

