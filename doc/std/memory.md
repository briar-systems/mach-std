[std](README.md) / **memory**

# std.memory

low-level memory operations for raw and typed buffers

Source: [`src/memory.mach`](../../src/memory.mach)

| Functions | |
| :--- | :--- |
| [`range_valid`](#range_valid) | validate a public byte range without forming an exclusive end |
| [`range_scaled`](#range_scaled) | calculate a byte count without multiplication overflow |
| [`ranges_overlap`](#ranges_overlap) | conservatively reject malformed ranges and compare inclusive ends |
| [`raw_fill`](#raw_fill) | fill a block of raw memory with a byte value |
| [`raw_copy`](#raw_copy) | copy a block of raw memory from source to destination |
| [`raw_move`](#raw_move) | copy a block of raw memory, correctly handling overlapping regions |
| [`raw_zero`](#raw_zero) | zero out a block of raw memory |
| [`fill`](#fill) | fill a block of memory with a value for type T |
| [`copy`](#copy) | copy a block of memory from a source to a destination |
| [`move`](#move) | copy a typed block of memory, correctly handling overlapping regions |
| [`zero`](#zero) | zero out a block of memory for a number of elements of type T |
| [`raw_equal`](#raw_equal) | compare two blocks of raw memory byte-wise |
| [`equal`](#equal) | compare n typed elements at a and b for byte-wise equality |

---

## Functions

### range_valid

```mach
pub fun range_valid(data: *u8, len: usize) bool
```

validate a public byte range without forming an exclusive end

### range_scaled

```mach
pub fun range_scaled(count: usize, item_size: usize, output: *usize) bool
```

calculate a byte count without multiplication overflow

### ranges_overlap

```mach
pub fun ranges_overlap(first: *u8, first_len: usize, second: *u8,
    second_len: usize) bool
```

conservatively reject malformed ranges and compare inclusive ends

### raw_fill

```mach
pub fun raw_fill(p: ptr, value: u8, size: usize)
```

fill a block of raw memory with a byte value

byte-fills a head prologue to word alignment, stores the value splatted
across whole machine words through the aligned body, then byte-fills the
tail. word size is derived from usize, so the path adapts to 32/64-bit.

| Parameter | |
| :--- | :--- |
| `p` | pointer to the start of the memory block |
| `value` | byte value to fill with |
| `size` | number of bytes to fill |

### raw_copy

```mach
pub fun raw_copy(dst: ptr, src: ptr, size: usize)
```

copy a block of raw memory from source to destination

the regions must not overlap; raw_move is the overlap-safe copy. see the
kernels above for how the bytes are moved.

| Parameter | |
| :--- | :--- |
| `dst` | pointer to the destination memory block |
| `src` | pointer to the source memory block |
| `size` | number of bytes to copy |

### raw_move

```mach
pub fun raw_move(dst: ptr, src: ptr, size: usize)
```

copy a block of raw memory, correctly handling overlapping regions

copies backward when dst lies inside the source range, forward otherwise, so
every source byte is read before it is overwritten. for non-overlapping
regions, raw_copy is preferred.

| Parameter | |
| :--- | :--- |
| `dst` | pointer to the destination memory block |
| `src` | pointer to the source memory block |
| `size` | number of bytes to copy |

### raw_zero

```mach
pub fun raw_zero(p: ptr, size: usize)
```

zero out a block of raw memory

| Parameter | |
| :--- | :--- |
| `p` | pointer to the start of the memory block |
| `size` | number of bytes to zero out |

### fill

```mach
pub fun fill[T](p: *T, value: T, count: usize)
```

fill a block of memory with a value for type T

| Parameter | |
| :--- | :--- |
| `p` | pointer to the start of the memory block |
| `value` | value to fill with |
| `count` | number of elements to fill |

### copy

```mach
pub fun copy[T](dst: *T, src: *T, count: usize)
```

copy a block of memory from a source to a destination

a T with no secret byte takes raw_copy, a wholly secret T the constant-time
kernel through *^u8, and a mixed T an element loop. no arm declassifies.

| Parameter | |
| :--- | :--- |
| `dst` | pointer to the destination memory block |
| `src` | pointer to the source memory block |
| `count` | number of elements to copy |

### move

```mach
pub fun move[T](dst: *T, src: *T, count: usize)
```

copy a typed block of memory, correctly handling overlapping regions

dispatches like copy[T], with the overlap-safe kernel on each arm. for
non-overlapping regions, copy[T] is preferred.

| Parameter | |
| :--- | :--- |
| `dst` | pointer to the destination memory block |
| `src` | pointer to the source memory block |
| `count` | number of elements to copy |

### zero

```mach
pub fun zero[T](p: *T, count: usize)
```

zero out a block of memory for a number of elements of type T

a type holding any secret byte goes through `$zeroize`, which no pass removes,
and the rest through raw_zero.

| Parameter | |
| :--- | :--- |
| `p` | pointer to the start of the memory block |
| `count` | number of elements to zero out |

### raw_equal

```mach
pub fun raw_equal(a: ptr, b: ptr, n: usize) bool
```

compare two blocks of raw memory byte-wise

when a and b are co-aligned modulo the word size, a byte head reaches
alignment, whole words are compared through the body, then a byte tail;
mismatched alignment falls back to a plain byte loop. word size is derived
from usize (32/64-bit adaptive).

nil contract: n==0 is vacuously true regardless of pointer values.
equal pointers (including nil==nil) are trivially true without dereference.
if exactly one pointer is nil and n>0, the result is false.

| Parameter | |
| :--- | :--- |
| `a` | pointer to the first memory block |
| `b` | pointer to the second memory block |
| `n` | number of bytes to compare |
| **returns** | true if the first n bytes of a and b are identical |

### equal

```mach
pub fun equal[T](a: *T, b: *T, n: usize) bool
```

compare n typed elements at a and b for byte-wise equality

delegates to raw_equal; see raw_equal for nil handling.
returns false if the byte count would overflow usize.

| Parameter | |
| :--- | :--- |
| `a` | pointer to the first element |
| `b` | pointer to the second element |
| `n` | number of elements to compare |
| **returns** | true if the first n elements of a and b are byte-identical |

