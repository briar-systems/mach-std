[std](../README.md) / [encoding](README.md) / **binary**

# std.encoding.binary

binary encoding with explicit byte order

encodes and decodes fixed-width scalars in a chosen endianness. an Encoder
builds a growable byte sequence, a Builder writes transactional fields into
fixed storage, and a Decoder reads a checked cursor over existing bytes. all
carry their Order so layouts never depend on the machine's native order.

only fixed-width unsigned scalars have an unambiguous byte layout, so the
scalar surface is the named-width write_u*/read_u*/patch_u* family; signed
and float values reinterpret through the matching width at the call site
(`v:~u32`). pointers, strings, and variable-length data need a format
decision (length prefixes, encodings) the caller must make with the
byte/str operations.

every producing operation reports an EncodeError and every consuming one a
DecodeError; both are closed tags, and a refused operation leaves its
encoder, builder or cursor exactly as it was.

Source: [`src/encoding/binary.mach`](../../../src/encoding/binary.mach)

Uses types from [`std.allocator`](../allocator.md).

| Type | | |
| :--- | :--- | :--- |
| [`Order`](#order) | `def` | byte order for multi-byte values |
| [`Checkpoint`](#checkpoint) | `def` | a logical position captured for explicit rollback |
| [`EncodeError`](#encodeerror) | `tag` | every way a write, patch, alignment or reservation can fail |
| [`DecodeError`](#decodeerror) | `tag` | every way a read, skip, alignment or checkpoint can fail |
| [`Encoder`](#encoder-1) | `rec` | growable byte sequence with a fixed byte order |
| [`Builder`](#builder-1) | `rec` | fixed-capacity byte builder with a transactional reservation lock |
| [`Reservation`](#reservation) | `rec` | unpublished child builder over a reserved parent tail |
| [`Decoder`](#decoder-1) | `rec` | cursor over existing bytes with a fixed byte order |
| [`Cursor`](#cursor-1) | `def` | checked borrowed cursor, retained as an alias of Decoder for compatibility |

| On `Order` | |
| :--- | :--- |
| [`LITTLE`](#order), [`BIG`](#order) | |
| [`put_uint`](#put_uint) | write the low sz bytes of v into dst in the given order |
| [`get_uint`](#get_uint) | read sz bytes from src in the given order into a u64 |
| [`encoder`](#encoder) | create an empty encoder |
| [`builder`](#builder) | wrap caller-owned storage as an empty fixed builder |
| [`decoder`](#decoder) | wrap existing bytes as a decoder positioned at offset 0 |
| [`cursor`](#cursor) | wrap existing bytes as a checked cursor positioned at offset 0 |

| On `Encoder` | |
| :--- | :--- |
| [`encoder_dnit`](#encoder_dnit) | release the encoder's buffer and reset it |
| [`reserve`](#reserve) | ensure capacity for `additional` more bytes |
| [`write_u8`](#write_u8) | append a u8 |
| [`write_u16`](#write_u16) | append a u16 in the encoder's byte order |
| [`write_u32`](#write_u32) | append a u32 in the encoder's byte order |
| [`write_u64`](#write_u64) | append a u64 in the encoder's byte order |
| [`write_bytes`](#write_bytes) | append raw bytes verbatim |
| [`write_str`](#write_str) | append a string and its null terminator |
| [`align`](#align) | pad with zero bytes up to an alignment boundary |
| [`patch_u8`](#patch_u8) | overwrite a u8 at an earlier offset without changing length |
| [`patch_u16`](#patch_u16) | overwrite a u16 at an earlier offset in the encoder's byte order |
| [`patch_u32`](#patch_u32) | overwrite a u32 at an earlier offset in the encoder's byte order |
| [`patch_u64`](#patch_u64) | overwrite a u64 at an earlier offset in the encoder's byte order |

| On `Builder` | |
| :--- | :--- |
| [`builder_remaining`](#builder_remaining) | bytes available after the builder's published prefix |
| [`builder_write_u8`](#builder_write_u8) | append a u8 atomically |
| [`builder_write_u16`](#builder_write_u16) | append a u16 in the builder's byte order atomically |
| [`builder_write_u32`](#builder_write_u32) | append a u32 in the builder's byte order atomically |
| [`builder_write_u64`](#builder_write_u64) | append a u64 in the builder's byte order atomically |
| [`builder_write_bytes`](#builder_write_bytes) | append raw bytes atomically |
| [`builder_write_str`](#builder_write_str) | append a string and null terminator atomically |
| [`builder_align`](#builder_align) | append zero padding to a power-of-two boundary atomically |
| [`builder_patch_u8`](#builder_patch_u8) | patch one published byte without changing length |
| [`builder_patch_u16`](#builder_patch_u16) | patch a published u16 without changing length |
| [`builder_patch_u32`](#builder_patch_u32) | patch a published u32 without changing length |
| [`builder_patch_u64`](#builder_patch_u64) | patch a published u64 without changing length |
| [`builder_checkpoint`](#builder_checkpoint) | capture the current fixed-builder length for explicit rollback |
| [`builder_rollback`](#builder_rollback) | restore a prior builder checkpoint without changing backing bytes |
| [`builder_reserve`](#builder_reserve) | lock capacity for a child field without publishing parent length |

| On `Reservation` | |
| :--- | :--- |
| [`builder_commit`](#builder_commit) | publish the completed prefix of a reservation as one logical field |
| [`reservation_rollback`](#reservation_rollback) | discard an unpublished reservation and unlock its parent |

| On `Decoder` | |
| :--- | :--- |
| [`read_u8`](#read_u8) | read a u8 and advance |
| [`read_u16`](#read_u16) | read a u16 in the decoder's byte order and advance |
| [`read_u32`](#read_u32) | read a u32 in the decoder's byte order and advance |
| [`read_u64`](#read_u64) | read a u64 in the decoder's byte order and advance |
| [`read_bytes`](#read_bytes) | return a pointer to the next `len` bytes and advance past them |
| [`read_str`](#read_str) | read a null-terminated string and advance past the terminator |
| [`skip`](#skip) | advance the cursor by n bytes |
| [`align_read`](#align_read) | advance the cursor to an alignment boundary |
| [`read_subview`](#read_subview) | return a bounded child cursor and advance only after validation |
| [`cursor_checkpoint`](#cursor_checkpoint) | capture a cursor position for speculative decoding |
| [`cursor_rollback`](#cursor_rollback) | restore an earlier cursor checkpoint |
| [`remaining`](#remaining) | bytes remaining between the cursor and the end |

---

## Order

```mach
pub def Order: u8
```

byte order for multi-byte values

| Name | Value | |
| :--- | :--- | :--- |
| `LITTLE` | `0` |  |
| `BIG` | `1` |  |

### put_uint

```mach
pub fun put_uint(dst: *u8, v: u64, sz: usize, order: Order)
```

write the low sz bytes of v into dst in the given order

| Parameter | |
| :--- | :--- |
| `dst` | destination for sz bytes |
| `v` | value whose low sz bytes are written |
| `sz` | number of bytes to write (1..8) |
| `order` | byte order |

### get_uint

```mach
pub fun get_uint(src: *u8, sz: usize, order: Order) u64
```

read sz bytes from src in the given order into a u64

| Parameter | |
| :--- | :--- |
| `src` | source of sz bytes |
| `sz` | number of bytes to read (1..8) |
| `order` | byte order |
| **returns** | the assembled value in the low sz bytes |

### encoder

```mach
pub fun encoder(a: *std.allocator.Allocator, order: Order) Encoder
```

create an empty encoder

| Parameter | |
| :--- | :--- |
| `a` | allocator for buffer memory |
| `order` | byte order for multi-byte writes |
| **returns** | a new empty Encoder |

### builder

```mach
pub fun builder(data: *u8, cap: usize, order: Order) Builder
```

wrap caller-owned storage as an empty fixed builder

### decoder

```mach
pub fun decoder(data: *u8, len: usize, order: Order) Decoder
```

wrap existing bytes as a decoder positioned at offset 0

| Parameter | |
| :--- | :--- |
| `data` | byte data |
| `len` | length in bytes |
| `order` | byte order for multi-byte reads |
| **returns** | a new Decoder |

### cursor

```mach
pub fun cursor(data: *u8, len: usize, order: Order) Cursor
```

wrap existing bytes as a checked cursor positioned at offset 0

## Checkpoint

```mach
pub def Checkpoint: usize
```

a logical position captured for explicit rollback

## EncodeError

```mach
pub tag EncodeError: u8 {
    alloc: std.allocator.Error;
    overflow;
    invalid;
    full:      usize;
    alignment: usize;
    reserved;
    bounds;
    inactive;
    stale;
    busy;
}
```

every way a write, patch, alignment or reservation can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `alloc` | `std.allocator.Error` | the encoder's growth was refused; the encoder is unchanged |
| `overflow` |  | a length or epoch would not fit usize |
| `invalid` |  | the encoder or builder is inconsistent (length past capacity, storage missing for a nonzero width, a nil source for nonzero bytes) |
| `full` | `usize` | the fixed builder lacks room; payload is the bytes available |
| `alignment` | `usize` | the boundary is not a power of two; payload is the boundary |
| `reserved` |  | the builder is locked by an active reservation |
| `bounds` |  | a patch or checkpoint lies outside the published bytes |
| `inactive` |  | the reservation was already resolved, or never made |
| `stale` |  | the reservation no longer matches its parent |
| `busy` |  | the reservation's child still holds a reservation of its own |

## DecodeError

```mach
pub tag DecodeError: u8 {
    short: usize;
    invalid;
    alignment: usize;
    bounds;
    unterminated;
}
```

every way a read, skip, alignment or checkpoint can fail

| Case | Payload | |
| :--- | :--- | :--- |
| `short` | `usize` | the request exceeds the bytes remaining; payload is the remaining count |
| `invalid` |  | the cursor is inconsistent (position past the end, storage missing for pending bytes) |
| `alignment` | `usize` | the boundary is not a power of two; payload is the boundary |
| `bounds` |  | a checkpoint lies outside the cursor's past |
| `unterminated` |  | no null terminator before the end |

## Encoder

```mach
pub rec Encoder {
    alloc: *std.allocator.Allocator;
    order: Order;
    data:  *u8;
    len:   usize;
    cap:   usize;
}
```

growable byte sequence with a fixed byte order

| Field | Type | |
| :--- | :--- | :--- |
| `alloc` | `*std.allocator.Allocator` | allocator for buffer memory |
| `order` | `Order` | byte order for multi-byte writes |
| `data` | `*u8` | backing byte array |
| `len` | `usize` | bytes written |
| `cap` | `usize` | allocated capacity |

### encoder_dnit

```mach
pub fun encoder_dnit(e: *Encoder) err[std.allocator.Error]
```

release the encoder's buffer and reset it

an encoder that owns no buffer is reset without asking the allocator. a
refused release leaves the encoder owning its buffer.

| Parameter | |
| :--- | :--- |
| `e` | encoder to deinitialize |
| **returns** | ok, or the allocator's refusal |

### reserve

```mach
pub fun reserve(e: *Encoder, additional: usize) res[usize, EncodeError]
```

ensure capacity for `additional` more bytes

| Parameter | |
| :--- | :--- |
| `e` | encoder to reserve in |
| `additional` | number of additional bytes needed |
| **returns** | new capacity, or the failure; a refused growth leaves the encoder as it was |

### write_u8

```mach
pub fun write_u8(e: *Encoder, v: u8) res[usize, EncodeError]
```

append a u8

| Parameter | |
| :--- | :--- |
| `e` | encoder to write into |
| `v` | value to append |
| **returns** | new length, or the failure |

### write_u16

```mach
pub fun write_u16(e: *Encoder, v: u16) res[usize, EncodeError]
```

append a u16 in the encoder's byte order

| Parameter | |
| :--- | :--- |
| `e` | encoder to write into |
| `v` | value to append |
| **returns** | new length, or the failure |

### write_u32

```mach
pub fun write_u32(e: *Encoder, v: u32) res[usize, EncodeError]
```

append a u32 in the encoder's byte order

| Parameter | |
| :--- | :--- |
| `e` | encoder to write into |
| `v` | value to append |
| **returns** | new length, or the failure |

### write_u64

```mach
pub fun write_u64(e: *Encoder, v: u64) res[usize, EncodeError]
```

append a u64 in the encoder's byte order

| Parameter | |
| :--- | :--- |
| `e` | encoder to write into |
| `v` | value to append |
| **returns** | new length, or the failure |

### write_bytes

```mach
pub fun write_bytes(e: *Encoder, p: *u8, len: usize) res[usize, EncodeError]
```

append raw bytes verbatim

| Parameter | |
| :--- | :--- |
| `e` | encoder to write into |
| `p` | source bytes |
| `len` | number of bytes |
| **returns** | new length, or the failure |

### write_str

```mach
pub fun write_str(e: *Encoder, s: str) res[usize, EncodeError]
```

append a string and its null terminator

| Parameter | |
| :--- | :--- |
| `e` | encoder to write into |
| `s` | string to append |
| **returns** | new length, or the failure |

### align

```mach
pub fun align(e: *Encoder, boundary: usize) res[usize, EncodeError]
```

pad with zero bytes up to an alignment boundary

| Parameter | |
| :--- | :--- |
| `e` | encoder to align |
| `boundary` | alignment boundary (a power of two) |
| **returns** | new length, or the failure |

### patch_u8

```mach
pub fun patch_u8(e: *Encoder, offset: usize, v: u8) res[usize, EncodeError]
```

overwrite a u8 at an earlier offset without changing length

### patch_u16

```mach
pub fun patch_u16(e: *Encoder, offset: usize, v: u16) res[usize, EncodeError]
```

overwrite a u16 at an earlier offset in the encoder's byte order

| Parameter | |
| :--- | :--- |
| `e` | encoder to patch |
| `offset` | byte offset to write at |
| `v` | value to write |
| **returns** | bytes written, or the failure |

### patch_u32

```mach
pub fun patch_u32(e: *Encoder, offset: usize, v: u32) res[usize, EncodeError]
```

overwrite a u32 at an earlier offset in the encoder's byte order

| Parameter | |
| :--- | :--- |
| `e` | encoder to patch |
| `offset` | byte offset to write at |
| `v` | value to write |
| **returns** | bytes written, or the failure |

### patch_u64

```mach
pub fun patch_u64(e: *Encoder, offset: usize, v: u64) res[usize, EncodeError]
```

overwrite a u64 at an earlier offset in the encoder's byte order

| Parameter | |
| :--- | :--- |
| `e` | encoder to patch |
| `offset` | byte offset to write at |
| `v` | value to write |
| **returns** | bytes written, or the failure |

## Builder

```mach
pub rec Builder {
    order:    Order;
    data:     *u8;
    len:      usize;
    cap:      usize;
    reserved: bool;
    epoch:    usize;
}
```

fixed-capacity byte builder with a transactional reservation lock

| Field | Type | |
| :--- | :--- | :--- |
| `order` | `Order` | byte order for multi-byte writes |
| `data` | `*u8` | caller-owned backing bytes |
| `len` | `usize` | logically published bytes |
| `cap` | `usize` | backing capacity |
| `reserved` | `bool` | whether a child reservation owns the unpublished tail |
| `epoch` | `usize` | monotonically increasing reservation identity |

### builder_remaining

```mach
pub fun builder_remaining(b: *Builder) usize
```

bytes available after the builder's published prefix

### builder_write_u8

```mach
pub fun builder_write_u8(b: *Builder, v: u8) res[usize, EncodeError]
```

append a u8 atomically

### builder_write_u16

```mach
pub fun builder_write_u16(b: *Builder, v: u16) res[usize, EncodeError]
```

append a u16 in the builder's byte order atomically

### builder_write_u32

```mach
pub fun builder_write_u32(b: *Builder, v: u32) res[usize, EncodeError]
```

append a u32 in the builder's byte order atomically

### builder_write_u64

```mach
pub fun builder_write_u64(b: *Builder, v: u64) res[usize, EncodeError]
```

append a u64 in the builder's byte order atomically

### builder_write_bytes

```mach
pub fun builder_write_bytes(b: *Builder, data: *u8, len: usize) res[usize, EncodeError]
```

append raw bytes atomically

### builder_write_str

```mach
pub fun builder_write_str(b: *Builder, s: str) res[usize, EncodeError]
```

append a string and null terminator atomically

### builder_align

```mach
pub fun builder_align(b: *Builder, boundary: usize) res[usize, EncodeError]
```

append zero padding to a power-of-two boundary atomically

### builder_patch_u8

```mach
pub fun builder_patch_u8(b: *Builder, offset: usize, v: u8) res[usize, EncodeError]
```

patch one published byte without changing length

### builder_patch_u16

```mach
pub fun builder_patch_u16(b: *Builder, offset: usize, v: u16) res[usize, EncodeError]
```

patch a published u16 without changing length

### builder_patch_u32

```mach
pub fun builder_patch_u32(b: *Builder, offset: usize, v: u32) res[usize, EncodeError]
```

patch a published u32 without changing length

### builder_patch_u64

```mach
pub fun builder_patch_u64(b: *Builder, offset: usize, v: u64) res[usize, EncodeError]
```

patch a published u64 without changing length

### builder_checkpoint

```mach
pub fun builder_checkpoint(b: *Builder) res[Checkpoint, EncodeError]
```

capture the current fixed-builder length for explicit rollback

### builder_rollback

```mach
pub fun builder_rollback(b: *Builder, mark: Checkpoint) res[usize, EncodeError]
```

restore a prior builder checkpoint without changing backing bytes

### builder_reserve

```mach
pub fun builder_reserve(b: *Builder, capacity: usize) res[Reservation, EncodeError]
```

lock capacity for a child field without publishing parent length

## Reservation

```mach
pub rec Reservation {
    parent: *Builder;
    body:   Builder;
    start:  usize;
    limit:  usize;
    epoch:  usize;
    active: bool;
}
```

unpublished child builder over a reserved parent tail

| Field | Type | |
| :--- | :--- | :--- |
| `parent` | `*Builder` | parent whose logical length remains unchanged until commit |
| `body` | `Builder` | fixed child builder bounded to the reservation |
| `start` | `usize` | parent's logical length when the reservation began |
| `limit` | `usize` | reserved byte capacity |
| `epoch` | `usize` | identity used to reject stale reservation handles |
| `active` | `bool` | whether the reservation can still commit or roll back  an active reservation and its parent must stay at stable addresses. resolve nested reservations before their parents and do not copy active handles. |

### builder_commit

```mach
pub fun builder_commit(r: *Reservation) res[usize, EncodeError]
```

publish the completed prefix of a reservation as one logical field

### reservation_rollback

```mach
pub fun reservation_rollback(r: *Reservation) res[usize, EncodeError]
```

discard an unpublished reservation and unlock its parent

## Decoder

```mach
pub rec Decoder {
    order: Order;
    data:  *u8;
    len:   usize;
    pos:   usize;
}
```

cursor over existing bytes with a fixed byte order

| Field | Type | |
| :--- | :--- | :--- |
| `order` | `Order` | byte order for multi-byte reads |
| `data` | `*u8` | byte data |
| `len` | `usize` | total length in bytes |
| `pos` | `usize` | current read position |

### read_u8

```mach
pub fun read_u8(d: *Decoder) res[u8, DecodeError]
```

read a u8 and advance

| Parameter | |
| :--- | :--- |
| `d` | decoder to read from |
| **returns** | the value, or the failure |

### read_u16

```mach
pub fun read_u16(d: *Decoder) res[u16, DecodeError]
```

read a u16 in the decoder's byte order and advance

| Parameter | |
| :--- | :--- |
| `d` | decoder to read from |
| **returns** | the value, or the failure |

### read_u32

```mach
pub fun read_u32(d: *Decoder) res[u32, DecodeError]
```

read a u32 in the decoder's byte order and advance

| Parameter | |
| :--- | :--- |
| `d` | decoder to read from |
| **returns** | the value, or the failure |

### read_u64

```mach
pub fun read_u64(d: *Decoder) res[u64, DecodeError]
```

read a u64 in the decoder's byte order and advance

| Parameter | |
| :--- | :--- |
| `d` | decoder to read from |
| **returns** | the value, or the failure |

### read_bytes

```mach
pub fun read_bytes(d: *Decoder, len: usize) res[*u8, DecodeError]
```

return a pointer to the next `len` bytes and advance past them

| Parameter | |
| :--- | :--- |
| `d` | decoder to read from |
| `len` | number of bytes to consume |
| **returns** | pointer into the decoder's data (nil for a zero-length request), or the failure |

### read_str

```mach
pub fun read_str(d: *Decoder) res[str, DecodeError]
```

read a null-terminated string and advance past the terminator

| Parameter | |
| :--- | :--- |
| `d` | decoder to read from |
| **returns** | pointer to the string within the data, or the failure |

### skip

```mach
pub fun skip(d: *Decoder, n: usize) res[usize, DecodeError]
```

advance the cursor by n bytes

| Parameter | |
| :--- | :--- |
| `d` | decoder to advance |
| `n` | number of bytes to skip |
| **returns** | new position, or the failure |

### align_read

```mach
pub fun align_read(d: *Decoder, boundary: usize) res[usize, DecodeError]
```

advance the cursor to an alignment boundary

| Parameter | |
| :--- | :--- |
| `d` | decoder to align |
| `boundary` | alignment boundary (a power of two) |
| **returns** | new position, or the failure |

### read_subview

```mach
pub fun read_subview(d: *Decoder, len: usize) res[Cursor, DecodeError]
```

return a bounded child cursor and advance only after validation

### cursor_checkpoint

```mach
pub fun cursor_checkpoint(d: *Decoder) res[Checkpoint, DecodeError]
```

capture a cursor position for speculative decoding

### cursor_rollback

```mach
pub fun cursor_rollback(d: *Decoder, mark: Checkpoint) res[usize, DecodeError]
```

restore an earlier cursor checkpoint

### remaining

```mach
pub fun remaining(d: *Decoder) usize
```

bytes remaining between the cursor and the end

| Parameter | |
| :--- | :--- |
| `d` | decoder to query |
| **returns** | unread byte count |

## Cursor

```mach
pub def Cursor: Decoder
```

checked borrowed cursor, retained as an alias of Decoder for compatibility

