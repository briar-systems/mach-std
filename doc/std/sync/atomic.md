[std](../README.md) / [sync](README.md) / **atomic**

# std.sync.atomic

atomic operations for lock-free programming

all operations have sequential-consistency ordering, implemented with
real per-arch instruction sequences selected at comptime on
$mach.build.arch:
  - x86_64: aligned MOV loads and memory XCHG stores implement the
    load/store pair; LOCK XADD / XCHG / CMPXCHG carry an implicit full barrier
    for the read-modify-write ops; MFENCE is the standalone full barrier;
    PAUSE is the spin hint.
  - aarch64: LDAR / STLR give acquire/release; the LDAXR/STLXR loop with a
    trailing DMB ISH provides seq-cst read-modify-write; DMB ISH is the
    standalone full barrier; YIELD is the spin hint.
  - riscv64: the A extension provides seq-cst read-modify-write via the
    .aqrl-suffixed AMOs (amoadd/amoswap) and the lr.d/sc.d reservation loop;
    a plain aligned ld bracketed by full FENCEs is the seq-cst load; FENCE is
    the standalone full barrier; PAUSE, spelled as its base-I encoding
    `fence w, 0`, is the spin hint.
  - riscv32: the A extension's atomics are one word wide, so every 64-bit
    operation runs under one of a table of word spinlocks, picked by the
    target's address and taken and released with .aqrl AMOs, which order the
    plain accesses between them. FENCE is the standalone full barrier and
    `fence w, 0` (PAUSE) the spin hint.
  - wasm32: the baseline has no atomics and no second thread, so every
    operation is the plain access, and the barrier and the hint are nothing.

the word operations (load_word and the rest, on usize) are one native
instruction or reservation loop on every target, so they never take a lock.
state a signal handler touches must be word-sized and use them: a 64-bit
operation that takes a lock its own thread already holds would spin forever.

Source: [`src/sync/atomic.mach`](../../../src/sync/atomic.mach)

| Functions | |
| :--- | :--- |
| [`load`](#load) | atomic 64-bit load with sequential consistency |
| [`store`](#store) | atomic 64-bit store with sequential consistency |
| [`cas`](#cas) | atomic compare-and-swap if *ptr == *expected, stores desired and returns true |
| [`fetch_add`](#fetch_add) | atomic fetch-and-add |
| [`fetch_sub`](#fetch_sub) | atomic fetch-and-subtract |
| [`exchange`](#exchange) | atomic exchange |
| [`load_word`](#load_word) | atomic word load with sequential consistency |
| [`store_word`](#store_word) | atomic word store with sequential consistency |
| [`cas_word`](#cas_word) | atomic word compare-and-swap, as cas |
| [`fetch_add_word`](#fetch_add_word) | atomic word fetch-and-add, wrapping |
| [`fetch_sub_word`](#fetch_sub_word) | atomic word fetch-and-subtract, wrapping |
| [`exchange_word`](#exchange_word) | atomic word exchange |
| [`fence`](#fence) | full memory barrier |
| [`spin_hint`](#spin_hint) | cpu yield hint for spin loops |

| Constants | |
| :--- | :--- |
| [`LOCK_FREE_64`](#constants) | whether the 64-bit operations are lock-free |

---

## Functions

### load

```mach
#[inline("always")]
pub fun load(ptr: *i64) i64
```

atomic 64-bit load with sequential consistency

| Parameter | |
| :--- | :--- |
| `ptr` | address to load from |
| **returns** | loaded value |

### store

```mach
#[inline("always")]
pub fun store(ptr: *i64, v: i64)
```

atomic 64-bit store with sequential consistency

| Parameter | |
| :--- | :--- |
| `ptr` | address to store to |
| `v` | value to store |

### cas

```mach
#[inline("always")]
pub fun cas(ptr: *i64, expected: *i64, desired: i64) bool
```

atomic compare-and-swap
if *ptr == *expected, stores desired and returns true.
otherwise, writes actual value to *expected and returns false.

| Parameter | |
| :--- | :--- |
| `ptr` | address of the atomic variable |
| `expected` | pointer to expected value (updated on failure) |
| `desired` | value to store on success |
| **returns** | true if the swap succeeded |

### fetch_add

```mach
#[inline("always")]
pub fun fetch_add(ptr: *i64, v: i64) i64
```

atomic fetch-and-add. returns the old value

| Parameter | |
| :--- | :--- |
| `ptr` | address of the atomic variable |
| `v` | value to add |
| **returns** | previous value |

### fetch_sub

```mach
#[inline("always")]
pub fun fetch_sub(ptr: *i64, v: i64) i64
```

atomic fetch-and-subtract. returns the old value

| Parameter | |
| :--- | :--- |
| `ptr` | address of the atomic variable |
| `v` | value to subtract |
| **returns** | previous value |

### exchange

```mach
#[inline("always")]
pub fun exchange(ptr: *i64, v: i64) i64
```

atomic exchange. returns the old value

| Parameter | |
| :--- | :--- |
| `ptr` | address of the atomic variable |
| `v` | new value |
| **returns** | previous value |

### load_word

```mach
#[inline("always")]
pub fun load_word(ptr: *usize) usize
```

atomic word load with sequential consistency

| Parameter | |
| :--- | :--- |
| `ptr` | address to load from |
| **returns** | loaded value |

### store_word

```mach
#[inline("always")]
pub fun store_word(ptr: *usize, v: usize)
```

atomic word store with sequential consistency

| Parameter | |
| :--- | :--- |
| `ptr` | address to store to |
| `v` | value to store |

### cas_word

```mach
#[inline("always")]
pub fun cas_word(ptr: *usize, expected: *usize, desired: usize) bool
```

atomic word compare-and-swap, as cas

| Parameter | |
| :--- | :--- |
| `ptr` | address of the atomic word |
| `expected` | pointer to expected value (updated on failure) |
| `desired` | value to store on success |
| **returns** | true if the swap succeeded |

### fetch_add_word

```mach
#[inline("always")]
pub fun fetch_add_word(ptr: *usize, v: usize) usize
```

atomic word fetch-and-add, wrapping. returns the old value

| Parameter | |
| :--- | :--- |
| `ptr` | address of the atomic word |
| `v` | value to add |
| **returns** | previous value |

### fetch_sub_word

```mach
#[inline("always")]
pub fun fetch_sub_word(ptr: *usize, v: usize) usize
```

atomic word fetch-and-subtract, wrapping. returns the old value

| Parameter | |
| :--- | :--- |
| `ptr` | address of the atomic word |
| `v` | value to subtract |
| **returns** | previous value |

### exchange_word

```mach
#[inline("always")]
pub fun exchange_word(ptr: *usize, v: usize) usize
```

atomic word exchange. returns the old value

| Parameter | |
| :--- | :--- |
| `ptr` | address of the atomic word |
| `v` | new value |
| **returns** | previous value |

### fence

```mach
#[inline("always")]
pub fun fence()
```

full memory barrier

### spin_hint

```mach
#[inline("always")]
pub fun spin_hint()
```

cpu yield hint for spin loops

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `LOCK_FREE_64` | `bool` | `$mach.build.arch != $mach.arch.riscv32` | whether the 64-bit operations are lock-free |

