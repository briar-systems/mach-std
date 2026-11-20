[std](../../README.md) / [filesystem](../README.md) / [transaction](README.md) / **ownership**

# std.filesystem.transaction.ownership

stable owners for cooperative root claims and filesystem-enforced leaf reservations

Source: [`src/filesystem/transaction/ownership.mach`](../../../../src/filesystem/transaction/ownership.mach)

Uses types from [`std.filesystem.removal`](../removal.md), [`std.sync.mutex`](../../sync/mutex.md), [`std.system.os`](../../system/os.md).

| Type | | |
| :--- | :--- | :--- |
| [`Root`](#root) | `rec` | initialized owners stay at their original address until destruction |
| [`Lock`](#lock) | `rec` | the exclusive claim on a root, held through a locked sentinel file |
| [`Borrow`](#borrow) | `rec` | name, in native units, is borrowed from the destination claim and remains valid through release, or is converted, the conversion owned by the borrow |

| On `Root` | |
| :--- | :--- |
| [`control_fd`](#control_fd) | the directory this module's control files live in |
| [`root_homed`](#root_homed) | whether a valid root has a control directory separate from itself |
| [`root_valid`](#root_valid) | whether a root is initialized at its own address and still holds its directory |
| [`root_init`](#root_init) | takes descriptor ownership only on success |
| [`root_init_with_home`](#root_init_with_home) | `home_fd` is the control directory, owned by the root only when `owned`; a borrowed home stays the caller's to keep alive through the root's use |
| [`root_set_home`](#root_set_home) | give an unclaimed root a borrowed home, releasing one it owned |
| [`root_dnit`](#root_dnit) | close a root's directory and the home it owns |

| On `Lock` | |
| :--- | :--- |
| [`lock_valid`](#lock_valid) | whether a lock is acquired at its own address and not being released |
| [`acquire`](#acquire) | claim a root exclusively by creating and locking its sentinel file |
| [`release_lock`](#release_lock) | close a lock's sentinel and claims directory and unclaim its root |
| [`begin_recovery`](#begin_recovery) | the caller keeps the exclusive root claim throughout its recovery effects |
| [`end_recovery`](#end_recovery) | leave recovery, closing admission unless the caller admits new borrows |
| [`initialize_claims`](#initialize_claims) | fresh creation inherits the root namespace instead of trusting stale directory flags |

| On `Borrow` | |
| :--- | :--- |
| [`borrow_valid`](#borrow_valid) | whether a borrow is registered at its own address and not yet released |
| [`borrow_worker`](#borrow_worker) | admission happens before a worker is launched |
| [`borrow_leaf`](#borrow_leaf) | the name is converted once, and the borrow owns the conversion |
| [`borrow_leaf_native`](#borrow_leaf_native) | borrow_leaf for a name in native units, borrowed through release |
| [`release_borrow`](#release_borrow) | even failed claim cleanup consumes the borrow and leaves recoverable residue |

| Constants | |
| :--- | :--- |
| [`LOCK_LEAF`](#constants), [`CLAIMS_LEAF`](#constants) | |

---

## Root

```mach
pub rec Root {
    dirfd: usize;
    # the control directory holding the lock sentinel, claims and backups:
    # os.INVALID_HANDLE when the root directory is its own home, closed at destruction
    # only when derivation opened it
    home_fd:    usize;
    home_owned: bool;
    address:    usize;
    gate:       std.sync.mutex.Mutex;
    claimed:    bool;
}
```

initialized owners stay at their original address until destruction

### control_fd

```mach
pub fun control_fd(root: *Root) usize
```

the directory this module's control files live in

### root_homed

```mach
pub fun root_homed(root: *Root) bool
```

whether a valid root has a control directory separate from itself

| Parameter | |
| :--- | :--- |
| `root` | the root |
| **returns** | true when the root is valid and has a home descriptor |

### root_valid

```mach
pub fun root_valid(root: *Root) bool
```

whether a root is initialized at its own address and still holds its directory

| Parameter | |
| :--- | :--- |
| `root` | the root, which may be nil |
| **returns** | true for a live root |

### root_init

```mach
pub fun root_init(out: *Root, fd: usize) err[std.filesystem.removal.Error]
```

takes descriptor ownership only on success

### root_init_with_home

```mach
pub fun root_init_with_home(out: *Root, fd: usize, home_fd: usize, owned: bool) err[std.filesystem.removal.Error]
```

`home_fd` is the control directory, owned by the root only when `owned`;
a borrowed home stays the caller's to keep alive through the root's use

### root_set_home

```mach
pub fun root_set_home(root: *Root, home_fd: usize) err[std.filesystem.removal.Error]
```

give an unclaimed root a borrowed home, releasing one it owned

### root_dnit

```mach
pub fun root_dnit(root: *Root) err[std.filesystem.removal.Error]
```

close a root's directory and the home it owns

a zeroed root is already destroyed. a claimed root or a copy away from its
original address is refused

| Parameter | |
| :--- | :--- |
| `root` | the root to destroy |
| **returns** | ok, INVALID for a nil, copied or claimed root, or the first close failure |

## Lock

```mach
pub rec Lock {
    fd:          usize;
    claims_fd:   usize;
    address:     usize;
    root:        *Root;
    gate:        std.sync.mutex.Mutex;
    borrowers:   usize;
    initialized: bool;
    recovering:  bool;
    closing:     bool;
}
```

the exclusive claim on a root, held through a locked sentinel file

an acquired lock stays at its original address until it is released

| Field | Type | |
| :--- | :--- | :--- |
| `fd` | `usize` | the locked sentinel descriptor, os.INVALID_HANDLE once released |
| `claims_fd` | `usize` | the open claims directory, os.INVALID_HANDLE until initialized |
| `address` | `usize` | the lock's own address, set when acquired |
| `root` | `*Root` | the claimed root |
| `gate` | `std.sync.mutex.Mutex` | guards the counters and state flags |
| `borrowers` | `usize` | live borrows admitted under this lock |
| `initialized` | `bool` | true once the claims directory is ready and admission is open |
| `recovering` | `bool` | true between begin_recovery and end_recovery |
| `closing` | `bool` | true while release_lock is closing descriptors |

### lock_valid

```mach
pub fun lock_valid(held: *Lock) bool
```

whether a lock is acquired at its own address and not being released

| Parameter | |
| :--- | :--- |
| `held` | the lock, which may be nil |
| **returns** | true for a held lock |

### acquire

```mach
pub fun acquire(out: *Lock, root: *Root) err[std.filesystem.removal.Error]
```

claim a root exclusively by creating and locking its sentinel file

the lock is not open for borrows until recovery initializes the claims
directory

| Parameter | |
| :--- | :--- |
| `out` | the lock to fill, zeroed or released at the same address |
| `root` | the root to claim |
| **returns** | ok, INVALID for a bad lock or root or a sentinel that is not a regular file, WOULD_BLOCK when this root is already claimed, UNSUPPORTED when the control directory cannot hold claims, or the native failure, including a lock another process holds |

### release_lock

```mach
pub fun release_lock(held: *Lock) err[std.filesystem.removal.Error]
```

close a lock's sentinel and claims directory and unclaim its root

| Parameter | |
| :--- | :--- |
| `held` | the lock, already released or zeroed for a no-op |
| **returns** | ok, INVALID for a nil or copied lock or one with live borrows or in recovery, or the first close failure |

### begin_recovery

```mach
pub fun begin_recovery(held: *Lock) err[std.filesystem.removal.Error]
```

the caller keeps the exclusive root claim throughout its recovery effects

### end_recovery

```mach
pub fun end_recovery(held: *Lock, admit: bool) err[std.filesystem.removal.Error]
```

leave recovery, closing admission unless the caller admits new borrows

| Parameter | |
| :--- | :--- |
| `held` | the lock in recovery |
| `admit` | false marks the claims uninitialized so borrows stay refused |
| **returns** | ok, or INVALID when the lock is not valid or not in recovery |

### initialize_claims

```mach
pub fun initialize_claims(held: *Lock) err[std.filesystem.removal.Error]
```

fresh creation inherits the root namespace instead of trusting stale directory flags

## Borrow

```mach
pub rec Borrow {
    address:   usize;
    owner:     *Lock;
    name:      *Unit;
    claim_fd:  usize;
    active:    bool;
    converted: std.system.os.NativePath;
}
```

name, in native units, is borrowed from the destination claim and remains
valid through release, or is converted, the conversion owned by the borrow

### borrow_valid

```mach
pub fun borrow_valid(borrow: *Borrow) bool
```

whether a borrow is registered at its own address and not yet released

| Parameter | |
| :--- | :--- |
| `borrow` | the borrow, which may be nil |
| **returns** | true for an active borrow |

### borrow_worker

```mach
pub fun borrow_worker(out: *Borrow, held: *Lock) err[std.filesystem.removal.Error]
```

admission happens before a worker is launched

### borrow_leaf

```mach
pub fun borrow_leaf(out: *Borrow, held: *Lock, name: str) err[std.filesystem.removal.Error]
```

the name is converted once, and the borrow owns the conversion

### borrow_leaf_native

```mach
pub fun borrow_leaf_native(out: *Borrow, held: *Lock, name: *Unit) err[std.filesystem.removal.Error]
```

borrow_leaf for a name in native units, borrowed through release

### release_borrow

```mach
pub fun release_borrow(borrow: *Borrow) err[std.filesystem.removal.Error]
```

even failed claim cleanup consumes the borrow and leaves recoverable residue

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `LOCK_LEAF` | `str` | `".mach-txn-lock"` |  |
| `CLAIMS_LEAF` | `str` | `".machtxn.claims"` |  |

