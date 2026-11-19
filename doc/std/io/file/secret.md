[std](../../README.md) / [io](../README.md) / [file](README.md) / **secret**

# std.io.file.secret

positioned file transfers into and out of secret-welded storage

the file is the destination or source and welded storage the bytes, as in
std.io.file's read_at and write_at, so the kernel reads or writes the welded
bytes through one native call and nothing else and a secret never passes
through public memory. the storage is the caller's, from std.memory.secret,
held directly or lent to a borrow. an interrupted call is retried within a
budget, and this layer leaves the storage untouched before, during and after
the call.

the direct transfers need the files capability. the borrow forms resolve a
std.memory.secret borrow, so they exist only where the pages capability does.

Source: [`src/io/file/secret.mach`](../../../../src/io/file/secret.mach)

Uses types from [`std.io.error`](../error.md), [`std.io.handle`](../handle.md), [`std.memory.secret`](../../memory/secret.md).

| Functions | |
| :--- | :--- |
| [`read_at`](#read_at) | read from a file straight into welded storage the caller owns: the kernel writes the storage through this call and nothing else |
| [`write_at`](#write_at) | write welded storage the caller owns straight to a file: the kernel reads the storage through this call and nothing else |
| [`borrow_read_at`](#borrow_read_at) | read from a file into a span of a borrow: the kernel writes the welded storage through this call and nothing else |
| [`borrow_write_at`](#borrow_write_at) | write a span of a borrow to a file: the kernel reads the welded storage through this call and nothing else |

---

## Functions

### read_at

```mach
pub fun read_at(file: std.io.handle.FileHandle, data: *^u8, len: usize, file_offset: u64) res[usize, std.io.error.Error]
```

read from a file straight into welded storage the caller owns: the kernel
writes the storage through this call and nothing else

| Parameter | |
| :--- | :--- |
| `file` | open file |
| `data` | destination secret storage |
| `len` | maximum bytes to read |
| `file_offset` | file position to read from |
| **returns** | bytes delivered (zero at end of file), or the error with the span unspecified. INVALID for an invalid file, a nil data or an offset past the largest file position |

### write_at

```mach
pub fun write_at(file: std.io.handle.FileHandle, data: *^u8, len: usize, file_offset: u64) res[usize, std.io.error.Error]
```

write welded storage the caller owns straight to a file: the kernel reads the
storage through this call and nothing else

| Parameter | |
| :--- | :--- |
| `file` | open file |
| `data` | source secret storage |
| `len` | maximum bytes to write |
| `file_offset` | file position to write at |
| **returns** | bytes persisted, or the error with nothing about the storage changed. INVALID as read_at |

### borrow_read_at

Only where `capability.HAS_PAGES`.

```mach
pub fun borrow_read_at(file: std.io.handle.FileHandle, borrow: std.memory.secret.Borrow, offset: usize, len: usize, file_offset: u64) res[usize, std.io.error.Error]
```

read from a file into a span of a borrow: the kernel writes the welded
storage through this call and nothing else

| Parameter | |
| :--- | :--- |
| **returns** | bytes delivered (zero at end of file), or the error with the span unspecified. CLOSED for a borrow that is not live, INVALID for a span outside it, and otherwise as read_at |

### borrow_write_at

Only where `capability.HAS_PAGES`.

```mach
pub fun borrow_write_at(file: std.io.handle.FileHandle, borrow: std.memory.secret.Borrow, offset: usize, len: usize, file_offset: u64) res[usize, std.io.error.Error]
```

write a span of a borrow to a file: the kernel reads the welded storage
through this call and nothing else

| Parameter | |
| :--- | :--- |
| **returns** | bytes persisted, or the error with nothing about the span changed. CLOSED and INVALID as borrow_read_at |

