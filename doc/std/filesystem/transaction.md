[std](../README.md) / [filesystem](README.md) / **transaction**

# std.filesystem.transaction

cooperative filesystem publication with explicit session ownership

roots, locks, claims, workers and transactions remain at their initialized
addresses. a copied owner cannot consume the original owner's resources.
a caller supplies its authoritative coordinator scope, holds all root locks
through recovery and worker completion, and reserves every planned destination
before worker admission. independent claims can publish concurrently beneath
one held root lock. a claim permits one active transaction or mutation at a time.
commit, abort and failed preparation release that active use, while the session
retains the reservation until its workers have joined.

recovery requires the coordinator and root lock with no claims or workers.
it resolves only the requested backup and sweeps recognized staging, preserving
other destinations' backups and malformed content. successful recovery creates
a fresh claims directory that inherits the root's native name equivalence.
failed recovery leaves admission closed. the persistent lock sentinel is never
unlinked by unlock. journal and claim ownership covers process interruption,
not arbitrary noncooperative mutation, host restart or power-loss recovery.

`.machtxn.<16 hex digits>` names private staging independently of destination
length. owned replacement keeps the previous directory at `.machtxn.backup/leaf`.
`.machtxn.claims/leaf` reserves the exact native destination name exclusively.
the journal prefix and `.mach-txn-lock` are reserved case-insensitively on every
platform. callers never place unrelated content in these namespaces.

a root opened with a control home keeps its lock sentinel, claims directory
and backup container under the home instead of beside the destination, so a
publication into a source tree leaves nothing there but the destination.
staging stays in the destination directory for the one-step rename. a child
derived from a homed root is homed at `home/leaf`, created on demand, so
two destinations never share a claims directory. the home must be on the
destination's filesystem, and the reserved names apply in both places.

descriptor-relative nofollow walks preserve containment when ancestor names
change. filesystem-qualified locks and claims enforce cooperative ownership.
presence and type queries are observations only. same-object preparation alone
retains the prior object and compares its complete local-domain identity at
commit. it detects replacement, not in-place writes or all content changes.
metadata-only retention is the default. explicit read authorization permits
event-only darwin references where existing permissions allow the open.
unsupported retention returns UNSUPPORTED without changing permissions.

preparation selects both precondition and durability. DUR_NONE requests no
barriers. DUR_FILE flushes file content through the original writable handles
and flushes subtree directories after their children and final modes. DUR_FULL
additionally flushes the publication parent after rename. required preparation
barriers fail before publication, while a required parent-flush failure occurs
after publication and does not undo it. permissive requests report aggregate
shortfall without allowing an outer flush to hide a missing child barrier.
windows directory persistence requires supported local ntfs and writable access.
journal recovery does not infer a power-durable multi-root transaction from these
per-publication barriers. callers serialize their own multi-root journal under
the supplied coordinator and recover it before planning or recording baselines.

ordinary commit uses one native rename. owned directory replacement uses two
renames and may temporarily leave the destination absent. it never runs recovery
while claims are live. every valid prepared transaction is consumed by commit,
including an invalid owned-replacement request. failed validation leaves it owned.

Source: [`src/filesystem/transaction.mach`](../../../src/filesystem/transaction.mach)

Uses types from [`std.allocator`](../allocator.md), [`std.crypto.hash.hasher`](../crypto/hash/hasher.md), [`std.filesystem.transaction.ownership`](transaction/ownership.md), [`std.io.writer`](../io/writer.md), [`std.sync.mutex`](../sync/mutex.md), [`std.system.file_identity`](../system/file_identity.md), [`std.system.os`](../system/os.md).

| Type | | |
| :--- | :--- | :--- |
| [`ErrorKind`](#errorkind) | `def` | what went wrong |
| [`Op`](#op) | `def` | which step failed, so a caller can say where without this module having to build a sentence |
| [`Error`](#error-1) | `rec` |  |
| [`EntryProbe`](#entryprobe) | `rec` | what a name under a root currently refers to |
| [`Claim`](#claim) | `rec` | planned reservations remain owned by the session until its workers have joined |
| [`Worker`](#worker) | `rec` |  |
| [`Durability`](#durability) | `def` | how much of a publication must reach stable storage before commit reports success |
| [`DurabilityRequest`](#durabilityrequest) | `rec` |  |
| [`Precondition`](#precondition) | `def` | what the destination must look like at commit for the publication to be allowed to land |
| [`PrepareOptions`](#prepareoptions) | `rec` | selected before any destination observation or staging work |
| [`EntryKind`](#entrykind) | `def` | what a transaction publishes |
| [`Transaction`](#transaction) | `rec` | leaf is the destination claim's native name |
| [`Outcome`](#outcome) | `rec` | what a commit actually achieved |
| [`BackupOutcome`](#backupoutcome) | `rec` | exact effects of a caller-journaled file publication, including failure |
| [`Entry`](#entry) | `rec` | one item in a subtree about to be published |
| [`Inventory`](#inventory) | `rec` | the complete contents of a subtree to publish |
| [`Descent`](#descent) | `rec` | a root at the deepest existing ancestor of a path, and what was missing |
| [`NativeDescent`](#nativedescent) | `rec` | a descent whose names are in native units |

| On `ErrorKind` | |
| :--- | :--- |
| [`CONTAINMENT`](#errorkind) | a name was not a single path component, or a walk left the root |
| [`PRECONDITION`](#errorkind) | the destination did not satisfy the precondition asked for at commit |
| [`DURABILITY`](#errorkind) | a required durability level could not be achieved |
| [`LOCK_HELD`](#errorkind) | another process holds the root lock |
| [`CONFLICT`](#errorkind) | the destination changed underneath in a way the operation cannot absorb |
| [`REJECTED`](#errorkind) | a validator rejected the staged content |
| [`INVALID`](#errorkind) | the caller misused the interface: a spent transaction, a nil argument |
| [`MEMORY`](#errorkind) | an allocation failed |
| [`IO`](#errorkind) | the operating system refused, and `code` carries the errno |
| [`ENTROPY`](#errorkind) | entropy for a staging name was unavailable |
| [`UNSUPPORTED`](#errorkind) | the backend cannot provide the requested contract |
| [`error`](#error) | |

| On `Op` | |
| :--- | :--- |
| [`OP_ROOT_OPEN`](#op), [`OP_LOCK`](#op), [`OP_PREPARE`](#op), [`OP_VALIDATE`](#op), [`OP_COMMIT`](#op), [`OP_ABORT`](#op), [`OP_RECOVER`](#op), [`OP_REMOVE`](#op), [`io_error`](#io_error) | |

| On `Error` | |
| :--- | :--- |
| [`error_message`](#error_message) | a stable description of the failure kind |
| [`error_op_name`](#error_op_name) | a stable name for the step that failed |
| [`root_open`](#root_open) | open a publication root |
| [`root_open_native`](#root_open_native) | root_open for a base and rel in native units, the walk done in them |
| [`root_open_with_home`](#root_open_with_home) | open a publication root whose control files live under `home` |
| [`root_open_with_home_native`](#root_open_with_home_native) | root_open_with_home for a base and rel in native units |
| [`root_adopt_home`](#root_adopt_home) | home an open root that is not locked: the same borrowed-home contract as `root_open_with_home`, for a root reached by descent rather than by path |
| [`root_open_child`](#root_open_child) | derive an independently owned root from a held directory capability the caller keeps parent alive and reserves leaf across derivation and use no ancestor pathname is reconstructed and a symlink leaf is refused a child of a homed root is homed at `home/leaf`, created when absent |
| [`root_open_child_native`](#root_open_child_native) | root_open_child for a leaf in native units |
| [`root_dnit`](#root_dnit) | release a publication root |
| [`root_identity`](#root_identity) | the identity of the root directory itself |
| [`entry_identity`](#entry_identity) | identity is separate from presence and type, and may be unsupported |
| [`entry_identity_native`](#entry_identity_native) | entry_identity for a leaf in native units |
| [`entry_read_all`](#entry_read_all) | read a whole small file under a root into a caller-provided buffer |
| [`entry_read_all_native`](#entry_read_all_native) | entry_read_all for a leaf in native units |
| [`lock`](#lock) | an exclusive claim on a publication root |
| [`unlock`](#unlock) | live borrowers and active recovery refuse release without closing anything |
| [`recover`](#recover) | requires the supplied coordinator lock and no live claims or workers admission remains closed when any recovery or claims initialization step fails |
| [`recover_native`](#recover_native) | recover for a leaf in native units, nil or empty to resolve no backup |

| On `EntryProbe` | |
| :--- | :--- |
| [`entry_probe`](#entry_probe) | describe a name under a root |
| [`entry_probe_native`](#entry_probe_native) | entry_probe for a leaf in native units |

| On `Claim` | |
| :--- | :--- |
| [`entry_rename`](#entry_rename) | both distinct reservations are borrowed before native effects begin |
| [`entry_rename_alias`](#entry_rename_alias) | a native same-entry rename may preserve the existing on-disk spelling |
| [`entry_rename_alias_native`](#entry_rename_alias_native) | entry_rename_alias for a spelling in native units |
| [`entry_unlink`](#entry_unlink) | ordinary unlink policy is retained, including readonly-file refusal |
| [`entry_rmdir_if_empty`](#entry_rmdir_if_empty) | absent and nonempty directories remain successful cleanup no-ops |
| [`root_remove_tree`](#root_remove_tree) | remove a tree under a root, by a path relative to it |
| [`entry_make_dir`](#entry_make_dir) | create a directory under a root |
| [`claim`](#claim-1) | reserves one complete destination spelling before workers or staging are admitted |
| [`claim_native`](#claim_native) | claim for a leaf in native units, reserved by those units in the claims directory |
| [`claim_leaf`](#claim_leaf) | borrowed until successful alias rename or release, stable during active use |
| [`claim_leaf_native`](#claim_leaf_native) | claim_leaf in native units, never nil for a live claim |
| [`claim_dnit`](#claim_dnit) | release refuses copied owners and active borrowers without changing their claim |

| On `Worker` | |
| :--- | :--- |
| [`borrow_worker`](#borrow_worker), [`release_worker`](#release_worker) | |

| On `Durability` | |
| :--- | :--- |
| [`DUR_NONE`](#durability) | order nothing; the destination appears when the operating system gets to it |
| [`DUR_FILE`](#durability) | flush the content, so a destination that survives a crash is complete |
| [`DUR_FULL`](#durability) | also flush the directory, so the destination's existence survives a crash |

| On `DurabilityRequest` | |
| :--- | :--- |
| [`durability_none`](#durability_none), [`durability_file`](#durability_file), [`durability_full`](#durability_full) | |

| On `Precondition` | |
| :--- | :--- |
| [`PRE_REPLACE`](#precondition) | replace without retaining or comparing an existing destination |
| [`PRE_SAME_OBJECT`](#precondition) | retain the prior object, or require continued absence when initially absent |
| [`PRE_ABSENT`](#precondition) | the destination must not exist |

| On `EntryKind` | |
| :--- | :--- |
| [`ENTRY_FILE`](#entrykind) | a single regular file, written through a writer |
| [`ENTRY_DIR`](#entrykind) | a single empty directory |
| [`ENTRY_SUBTREE`](#entrykind) | a directory and everything beneath it, built privately and moved in whole |

| On `Transaction` | |
| :--- | :--- |
| [`transaction_len`](#transaction_len), [`transaction_kind`](#transaction_kind) | |
| [`transaction_prior_identity`](#transaction_prior_identity) | the identity the destination had when prepare ran |
| [`transaction_staged_identity`](#transaction_staged_identity) | the identity of the staged entry, before it is committed |
| [`transaction_staged_child_identity`](#transaction_staged_child_identity) | observe one prepared subtree child through its original held staging directory the observation does not transfer a reference or admit a mutation |
| [`transaction_staged_child_identity_native`](#transaction_staged_child_identity_native) | transaction_staged_child_identity for a leaf in native units |
| [`prepare`](#prepare) | prepare a file publication from a writer |
| [`prepare_bytes`](#prepare_bytes) | prepare a file publication from bytes already in memory |
| [`validate`](#validate) | check the staged content before committing it |
| [`commit_with_backup`](#commit_with_backup) | consume a prepared file while retaining its original for a caller-owned journal requires same-object preparation, including initial absence, and a distinct absent backup claim under the same lock |
| [`commit`](#commit) | consumes the prepared transaction using its preparation-time policy a failure after rename reports an error without claiming publication rolled back |
| [`abort`](#abort) | discard the staged content without publishing it |
| [`prepare_subtree`](#prepare_subtree) | prepare a subtree publication |
| [`prepare_dir`](#prepare_dir) | prepare an empty directory publication |
| [`commit_replacing_owned`](#commit_replacing_owned) | consumes even invalid replacement requests and never recovers a live session the destination may be temporarily absent between the backup and publication renames |
| [`commit_replacing_owned_native`](#commit_replacing_owned_native) | commit_replacing_owned with an owns callback that takes each path relative to the target in native units, joined with `/`, so a tree holding a name with no UTF-8 spelling can be replaced |

| On `Entry` | |
| :--- | :--- |
| [`entry_file`](#entry_file), [`entry_dir`](#entry_dir) | |
| [`entry_file_native`](#entry_file_native) | entry_file for a canonical path in native units, borrowed until the inventory is released |
| [`entry_dir_native`](#entry_dir_native) | entry_dir for a canonical path in native units, borrowed until the inventory is released |

| On `Inventory` | |
| :--- | :--- |
| [`inventory_init`](#inventory_init), [`inventory_dnit`](#inventory_dnit) | |
| [`inventory_push`](#inventory_push) | add an item, refusing a path that is not canonical or that repeats one already added |

| On `Descent` | |
| :--- | :--- |
| [`descend`](#descend) | find where an existing tree stops along `rel` |
| [`descent_dnit`](#descent_dnit) | release a descent and everything it allocated |

| On `NativeDescent` | |
| :--- | :--- |
| [`descend_native`](#descend_native) | descend for a base and rel in native units, the walk done in them |
| [`native_descent_dnit`](#native_descent_dnit) | release a native descent and everything it allocated |

| Functions | |
| :--- | :--- |
| [`identity_equal`](#identity_equal), [`identity_encode`](#identity_encode), [`identity_decode`](#identity_decode) | |
| [`root_fd`](#root_fd) | the descriptor behind a root, for callers that must reach the operating system directly |
| [`root_home_fd`](#root_home_fd) | the directory holding the root's lock sentinel, claims and backups: the root itself unless it was opened with a home |
| [`coordinator_entry`](#coordinator_entry) | |

| Constants | |
| :--- | :--- |
| [`IDENTITY_TEXT_CAPACITY`](#constants) | complete observations have backend-qualified scope and do not retain an object |
| [`LOCK_LEAF`](#constants) | the sentinel file a root lock is taken on |
| [`STAGING_TAG`](#constants) | the prefix on every entry this module creates while a transaction is in flight |

| Forwards | |
| :--- | :--- |
| [`Identity`](#identity), [`METADATA_ONLY`](#metadata_only), [`READ_AUTHORIZED`](#read_authorized), [`Root`](#root), [`Lock`](#lock-1) | |

---

## ErrorKind

```mach
pub def ErrorKind: u8
```

what went wrong. the set is closed: every failure this module reports is one
of these, and no variant carries a message the caller has to parse.

| Name | Value | |
| :--- | :--- | :--- |
| `CONTAINMENT` | `1` | a name was not a single path component, or a walk left the root |
| `PRECONDITION` | `2` | the destination did not satisfy the precondition asked for at commit |
| `DURABILITY` | `3` | a required durability level could not be achieved |
| `LOCK_HELD` | `4` | another process holds the root lock |
| `CONFLICT` | `5` | the destination changed underneath in a way the operation cannot absorb |
| `REJECTED` | `6` | a validator rejected the staged content |
| `INVALID` | `7` | the caller misused the interface: a spent transaction, a nil argument |
| `MEMORY` | `8` | an allocation failed |
| `IO` | `9` | the operating system refused, and `code` carries the errno |
| `ENTROPY` | `10` | entropy for a staging name was unavailable |
| `UNSUPPORTED` | `11` | the backend cannot provide the requested contract |

### error

```mach
pub fun error(kind: ErrorKind, op: Op) Error
```

## Op

```mach
pub def Op: u8
```

which step failed, so a caller can say where without this module having to
build a sentence.

| Name | Value | |
| :--- | :--- | :--- |
| `OP_ROOT_OPEN` | `0` |  |
| `OP_LOCK` | `1` |  |
| `OP_PREPARE` | `2` |  |
| `OP_VALIDATE` | `3` |  |
| `OP_COMMIT` | `4` |  |
| `OP_ABORT` | `5` |  |
| `OP_RECOVER` | `6` |  |
| `OP_REMOVE` | `7` |  |

### io_error

```mach
pub fun io_error(op: Op, code: i64) Error
```

## Error

```mach
pub rec Error {
    kind: ErrorKind;
    op:   Op;
    # underlying producer errno when available, including native unsupported errors
    code: i64;
    # first independent cleanup failure
    cleanup_code: i64;
}
```

### error_message

```mach
pub fun error_message(e: Error) str
```

a stable description of the failure kind

the returned string is a literal, so this never allocates and never returns
an empty string. the offending path is deliberately absent: the caller passed
it in and can name it far better than this module can.

| Parameter | |
| :--- | :--- |
| `e` | the error to describe |
| **returns** | a non-empty description of `e.kind` |

### error_op_name

```mach
pub fun error_op_name(e: Error) str
```

a stable name for the step that failed

| Parameter | |
| :--- | :--- |
| `e` | the error to describe |
| **returns** | a non-empty name for `e.op` |

### root_open

```mach
pub fun root_open(out: *Root, base: Path, rel: Path) err[Error]
```

open a publication root

walks `rel` beneath `base` one component at a time. each component must
already exist and be a real directory, checked without following symlinks, so
a symlinked ancestor is refused rather than traversed. passing an empty `rel`
or `.` opens `base` itself.

| Parameter | |
| :--- | :--- |
| `base` | absolute or process-relative path of the anchor directory |
| `rel` | canonical relative path beneath `base`, or empty for `base` itself |
| **returns** | none when initialized in caller-provided final storage failure retains the primary cause and first cleanup error, with no new root descriptors passed to close are consumed even when close reports an error |

### root_open_native

```mach
pub fun root_open_native(out: *Root, base: *Unit, rel: *Unit) err[Error]
```

root_open for a base and rel in native units, the walk done in them

### root_open_with_home

```mach
pub fun root_open_with_home(out: *Root, base: Path, rel: Path, home: *Root) err[Error]
```

open a publication root whose control files live under `home`

the lock sentinel, claims directory and backup container are placed in the
home directory rather than beside the destination. the home is borrowed:
the caller keeps it alive through the root's use. a home on another
filesystem cannot receive an owned-replacement backup by rename.

| Parameter | |
| :--- | :--- |
| `home` | an open root over the control directory |

### root_open_with_home_native

```mach
pub fun root_open_with_home_native(out: *Root, base: *Unit, rel: *Unit, home: *Root) err[Error]
```

root_open_with_home for a base and rel in native units

### root_adopt_home

```mach
pub fun root_adopt_home(r: *Root, home: *Root) err[Error]
```

home an open root that is not locked: the same borrowed-home contract as
`root_open_with_home`, for a root reached by descent rather than by path

### root_open_child

```mach
pub fun root_open_child(out: *Root, parent: *Root, leaf: str) err[Error]
```

derive an independently owned root from a held directory capability
the caller keeps parent alive and reserves leaf across derivation and use
no ancestor pathname is reconstructed and a symlink leaf is refused
a child of a homed root is homed at `home/leaf`, created when absent

### root_open_child_native

```mach
pub fun root_open_child_native(out: *Root, parent: *Root, leaf: *Unit) err[Error]
```

root_open_child for a leaf in native units

### root_dnit

```mach
pub fun root_dnit(r: *Root) err[Error]
```

release a publication root

idempotent: a second call is a no-op, so a caller may release on every exit
path without tracking whether it already did.

### root_identity

```mach
pub fun root_identity(r: *Root) res[Identity, Error]
```

the identity of the root directory itself

### entry_identity

```mach
pub fun entry_identity(r: *Root, leaf: str) res[opt[Identity], Error]
```

identity is separate from presence and type, and may be unsupported

### entry_identity_native

```mach
pub fun entry_identity_native(r: *Root, leaf: *Unit) res[opt[Identity], Error]
```

entry_identity for a leaf in native units

### entry_read_all

```mach
pub fun entry_read_all(r: *Root, leaf: str, out: *u8,
    out_cap: usize) res[opt[usize], Error]
```

read a whole small file under a root into a caller-provided buffer

for the fixed-size records a caller keeps beside its own data, where the
expected size is known and anything larger is corruption rather than a file
to grow a buffer for.

| Parameter | |
| :--- | :--- |
| `out` | destination buffer |
| `out_cap` | its capacity; a file larger than this is refused, not truncated |
| **returns** | the byte count, or none when the file does not exist |

### entry_read_all_native

```mach
pub fun entry_read_all_native(r: *Root, leaf: *Unit, out: *u8,
    out_cap: usize) res[opt[usize], Error]
```

entry_read_all for a leaf in native units

### lock

```mach
pub fun lock(out: *Lock, r: *Root) err[Error]
```

an exclusive claim on a publication root

while held, no other process can take the same claim. the operating system
releases it when this process exits, whether it exits cleanly, is killed, or
crashes, so a claim can never outlive its holder and be mistaken for a live
writer.
acquire without waiting, keeping the root alive until unlock

### unlock

```mach
pub fun unlock(held: *Lock) err[Error]
```

live borrowers and active recovery refuse release without closing anything

### recover

```mach
pub fun recover(alloc: *std.allocator.Allocator, held: *Lock, leaf: str) res[usize, Error]
```

requires the supplied coordinator lock and no live claims or workers
admission remains closed when any recovery or claims initialization step fails

### recover_native

```mach
pub fun recover_native(alloc: *std.allocator.Allocator, held: *Lock, leaf: *Unit) res[usize, Error]
```

recover for a leaf in native units, nil or empty to resolve no backup

## EntryProbe

```mach
pub rec EntryProbe {
    present:      bool;
    is_regular:   bool;
    is_directory: bool;
}
```

what a name under a root currently refers to

probing through the root's descriptor rather than through a path is what
makes the answer trustworthy: it describes an entry in the directory the
capability was granted over, and cannot be redirected by an ancestor that
changed since.

### entry_probe

```mach
pub fun entry_probe(r: *Root, leaf: str) res[EntryProbe, Error]
```

describe a name under a root

a name that does not exist is not an error: the probe comes back absent. the
lookup does not follow symlinks, so a symlink is reported as neither a
regular file nor a directory.

| Parameter | |
| :--- | :--- |
| `r` | the root to look in |
| `leaf` | the name to describe, a single path component |
| **returns** | what is there, or why it could not be determined |

### entry_probe_native

```mach
pub fun entry_probe_native(r: *Root, leaf: *Unit) res[EntryProbe, Error]
```

entry_probe for a leaf in native units

## Claim

```mach
pub rec Claim {
    address:     usize;
    owner:       *Lock;
    leaf:        str;
    name:        *Unit;
    alloc:       *std.allocator.Allocator;
    reservation: std.filesystem.transaction.ownership.Borrow;
    gate:        std.sync.mutex.Mutex;
    active:      bool;
    closing:     bool;
}
```

planned reservations remain owned by the session until its workers have joined

| Field | Type | |
| :--- | :--- | :--- |
| `leaf` | `str` | the reserved name spelled in UTF-8, nil when it has no UTF-8 spelling |
| `name` | `*Unit` | the reserved name in native units |

### entry_rename

```mach
pub fun entry_rename(from: *Claim, to: *Claim) err[Error]
```

both distinct reservations are borrowed before native effects begin

### entry_rename_alias

```mach
pub fun entry_rename_alias(destination: *Claim, spelling: str) err[Error]
```

a native same-entry rename may preserve the existing on-disk spelling

### entry_rename_alias_native

```mach
pub fun entry_rename_alias_native(destination: *Claim, spelling: *Unit) err[Error]
```

entry_rename_alias for a spelling in native units

### entry_unlink

```mach
pub fun entry_unlink(destination: *Claim) err[Error]
```

ordinary unlink policy is retained, including readonly-file refusal

### entry_rmdir_if_empty

```mach
pub fun entry_rmdir_if_empty(destination: *Claim) err[Error]
```

absent and nonempty directories remain successful cleanup no-ops

### root_remove_tree

```mach
pub fun root_remove_tree(destination: *Claim, rel: Path) res[usize, Error]
```

remove a tree under a root, by a path relative to it

this is the removal a caller reaches for instead of validating a path with a
string prefix check. containment is by construction rather than by comparison:
`rel` is walked one component at a time against the root's own descriptor, so
there is no absolute path to compare and no prefix to get wrong.

every way out of the root is refused rather than silently ignored, and each
comes back as CONTAINMENT:

  - an absolute path, a `..` component, a `.` component, or an empty one,
    none of which are canonical
  - a symlink at any component of `rel`, its last included. one named by the
    caller is refused rather than unlinked: removing the link itself would be
    safe enough, but refusing means the capability never has to reason about
    where a link points, and a caller that meant the link can unlink it by
    name. a symlink FOUND INSIDE the tree during the descent is a different
    thing and is unlinked, which removes the link and never its target
  - a directory swapped for a symlink between the check and the descent,
    refused by the native nofollow directory open
  - a tree deeper than MAX_REMOVE_DEPTH, since depth is input too

what it removed is reported only on success. a failure part-way returns the
error and no count, because a partial count invites a caller to treat a
failed removal as a smaller successful one. the entries removed before the
failure stay removed: this reports what happened, it does not roll back.

| Parameter | |
| :--- | :--- |
| `destination` | reserved top-level leaf |
| `rel` | canonical path beneath that leaf, empty to remove the leaf itself |
| **returns** | how many entries were removed, or why the removal was refused |

### entry_make_dir

```mach
pub fun entry_make_dir(destination: *Claim, mode: i32) res[bool, Error]
```

create a directory under a root

| Parameter | |
| :--- | :--- |
| **returns** | true when this call created it, false when it already existed |

### claim

```mach
pub fun claim(out: *Claim, alloc: *std.allocator.Allocator, held: *Lock, leaf: str) err[Error]
```

reserves one complete destination spelling before workers or staging are admitted

### claim_native

```mach
pub fun claim_native(out: *Claim, alloc: *std.allocator.Allocator, held: *Lock, leaf: *Unit) err[Error]
```

claim for a leaf in native units, reserved by those units in the claims
directory

### claim_leaf

```mach
pub fun claim_leaf(destination: *Claim) str
```

borrowed until successful alias rename or release, stable during active use.
nil when the reserved name has no UTF-8 spelling

### claim_leaf_native

```mach
pub fun claim_leaf_native(destination: *Claim) *Unit
```

claim_leaf in native units, never nil for a live claim

### claim_dnit

```mach
pub fun claim_dnit(destination: *Claim) err[Error]
```

release refuses copied owners and active borrowers without changing their claim

## Worker

```mach
pub rec Worker {
    admission: std.filesystem.transaction.ownership.Borrow;
}
```

### borrow_worker

```mach
pub fun borrow_worker(out: *Worker, held: *Lock) err[Error]
```

### release_worker

```mach
pub fun release_worker(worker: *Worker) err[Error]
```

## Durability

```mach
pub def Durability: u8
```

how much of a publication must reach stable storage before commit reports
success

| Name | Value | |
| :--- | :--- | :--- |
| `DUR_NONE` | `0` | order nothing; the destination appears when the operating system gets to it |
| `DUR_FILE` | `1` | flush the content, so a destination that survives a crash is complete |
| `DUR_FULL` | `2` | also flush the directory, so the destination's existence survives a crash |

## DurabilityRequest

```mach
pub rec DurabilityRequest {
    level: Durability;
    # when true a failed barrier fails its preparation or commit step
    required: bool;
}
```

### durability_none

```mach
pub fun durability_none() DurabilityRequest
```

### durability_file

```mach
pub fun durability_file(required: bool) DurabilityRequest
```

### durability_full

```mach
pub fun durability_full(required: bool) DurabilityRequest
```

## Precondition

```mach
pub def Precondition: u8
```

what the destination must look like at commit for the publication to be
allowed to land

| Name | Value | |
| :--- | :--- | :--- |
| `PRE_REPLACE` | `0` | replace without retaining or comparing an existing destination |
| `PRE_SAME_OBJECT` | `1` | retain the prior object, or require continued absence when initially absent |
| `PRE_ABSENT` | `2` | the destination must not exist |

## PrepareOptions

```mach
pub rec PrepareOptions {
    precondition: Precondition;
    # omitted fields retain the zero-valued metadata-only access contract
    prior_access: std.system.file_identity.Access;
    # file-only final permission mode, independent of the process umask
    # false keeps ordinary creation permissions, unsupported backends refuse true
    exact_mode: bool;
    durability: DurabilityRequest;
}
```

selected before any destination observation or staging work

## EntryKind

```mach
pub def EntryKind: u8
```

what a transaction publishes

| Name | Value | |
| :--- | :--- | :--- |
| `ENTRY_FILE` | `0` | a single regular file, written through a writer |
| `ENTRY_DIR` | `1` | a single empty directory |
| `ENTRY_SUBTREE` | `2` | a directory and everything beneath it, built privately and moved in whole |

## Transaction

```mach
pub rec Transaction {
    address:         usize;
    state:           u8;
    destination:     *Claim;
    dirfd:           usize;
    homefd:          usize;
    leaf:            *Unit;
    staging_name:    str;
    staging:         std.system.os.NativePath;
    staging_fd:      usize;
    prior_fd:        usize;
    kind:            EntryKind;
    had_prior:       bool;
    prior:           Identity;
    len:             usize;
    alloc:           *std.allocator.Allocator;
    options:         PrepareOptions;
    content_flushed: bool;
}
```

leaf is the destination claim's native name. staging_name is the staging
entry's name, and staging the same name in native units

### transaction_len

```mach
pub fun transaction_len(t: *Transaction) usize
```

### transaction_kind

```mach
pub fun transaction_kind(t: *Transaction) EntryKind
```

### transaction_prior_identity

```mach
pub fun transaction_prior_identity(t: *Transaction, out: *Identity) bool
```

the identity the destination had when prepare ran

| Parameter | |
| :--- | :--- |
| **returns** | false when the destination did not exist, leaving `out` untouched |

### transaction_staged_identity

```mach
pub fun transaction_staged_identity(t: *Transaction) res[Identity, Error]
```

the identity of the staged entry, before it is committed

a caller that records what it is about to publish needs this: after the
commit the staged name is gone, and the identity is the only thing that ties
the destination back to the transaction that produced it.

### transaction_staged_child_identity

```mach
pub fun transaction_staged_child_identity(t: *Transaction, leaf: str) res[Identity, Error]
```

observe one prepared subtree child through its original held staging directory
the observation does not transfer a reference or admit a mutation

### transaction_staged_child_identity_native

```mach
pub fun transaction_staged_child_identity_native(t: *Transaction, leaf: *Unit) res[Identity, Error]
```

transaction_staged_child_identity for a leaf in native units

### prepare

```mach
pub fun prepare[W](out: *Transaction, alloc: *std.allocator.Allocator, destination: *Claim,
    write_ctx: *W, write_cb: fun(*W, *std.io.writer.Writer) err[WriteError],
    mode: i32, digest: *std.crypto.hash.hasher.Hasher, options: PrepareOptions) err[Error]
```

prepare a file publication from a writer

the writer is the general form: `write_cb` is handed a `Writer` and may
produce the content however it likes, streaming it without ever holding it
all in memory. the bytes land in private staging beside the destination, on
the same filesystem, so the eventual commit is a rename and not a copy.

nothing about the destination changes here. on any failure the staging entry
is removed and the destination is left exactly as it was.

| Parameter | |
| :--- | :--- |
| `alloc` | allocator for the transaction's own strings |
| `destination` | the session-owned reservation borrowed until commit or abort |
| `write_ctx` | context handed back to `write_cb` |
| `write_cb` | produces the content through the writer; its error, the writer's own tag, rejects the prepare |
| `mode` | creation permission bits, or final file bits when exact_mode is true exact modes are applied after writing and before the requested durability barrier |
| `digest` | fed every byte written, nil for none |
| **returns** | none when out owns a prepared transaction |

### prepare_bytes

```mach
pub fun prepare_bytes(out: *Transaction, alloc: *std.allocator.Allocator, destination: *Claim,
    data: *u8, len: usize, mode: i32, digest: *std.crypto.hash.hasher.Hasher,
    options: PrepareOptions) err[Error]
```

prepare a file publication from bytes already in memory

the trivial writer: everything `prepare` says applies, with the content
supplied as a buffer instead of a callback.

### validate

```mach
pub fun validate[V](t: *Transaction, ctx: *V,
    validator: fun(*V, *u8, usize) bool) err[Error]
```

check the staged content before committing it

a step on the prepared value rather than an argument to prepare, so a caller
can decide what to check after seeing what was produced, and so a rejection
is reported separately from a write failure. the whole staged content is read
back from the staging descriptor and handed to `validator`; a validator that
returns false leaves the staging entry in place, so the caller still owns
the transaction and must abort it.

| Parameter | |
| :--- | :--- |
| `t` | the prepared transaction, which must be a file |
| `ctx` | context handed back to `validator` |
| `validator` | false rejects the content |
| **returns** | ok when the content passed |

### commit_with_backup

```mach
pub fun commit_with_backup(t: *Transaction, backup: *Claim) BackupOutcome
```

consume a prepared file while retaining its original for a caller-owned journal
requires same-object preparation, including initial absence, and a distinct
absent backup claim under the same lock. both reservations remain caller-owned.
each successful rename is reported even if the next step or cleanup fails.
no rollback or backup retirement is implicit. a published result may still carry
a durability or cleanup error. failure and cleanup_failure are independent.
staging_residue transfers only the name allocation when private removal fails.
the caller frees that string with t.alloc and retains its journal for recovery.
an invalid or copied transaction is not consumed. every valid prepared owner is.

### commit

```mach
pub fun commit(t: *Transaction) res[Outcome, Error]
```

consumes the prepared transaction using its preparation-time policy
a failure after rename reports an error without claiming publication rolled back

### abort

```mach
pub fun abort(t: *Transaction) err[Error]
```

discard the staged content without publishing it

the destination is never touched. the transaction is spent afterwards.

| Parameter | |
| :--- | :--- |
| **returns** | none on success; an error means residue may remain, which a later `recover` will remove |

### prepare_subtree

```mach
pub fun prepare_subtree(out: *Transaction, alloc: *std.allocator.Allocator, destination: *Claim,
    inv: *Inventory, mode: i32, options: PrepareOptions) err[Error]
```

prepare a subtree publication

builds the whole subtree privately beside its destination, so the commit is
one rename of the subtree root and the destination never exists in a partial
state. every descendant is created through held directory descriptors.

| Parameter | |
| :--- | :--- |
| `alloc` | allocator for the transaction's own strings |
| `destination` | the session-owned reservation borrowed until commit or abort |
| `inv` | everything the subtree contains |
| `mode` | permission bits for the subtree root directory |
| **returns** | none when out owns a prepared transaction |

### prepare_dir

```mach
pub fun prepare_dir(out: *Transaction, alloc: *std.allocator.Allocator, destination: *Claim,
    mode: i32, options: PrepareOptions) err[Error]
```

prepare an empty directory publication

the degenerate subtree: one directory and nothing in it.

### commit_replacing_owned

```mach
pub fun commit_replacing_owned[T](t: *Transaction, ctx: *T,
    owns: fun(*T, str, bool) bool) res[Outcome, Error]
```

consumes even invalid replacement requests and never recovers a live session
the destination may be temporarily absent between the backup and publication renames

| Parameter | |
| :--- | :--- |
| `ctx` | the caller's context, handed to owns |
| `owns` | whether the caller owns an entry, given its path relative to the target in UTF-8 with `/` separators and whether it is a directory |
| **returns** | the outcome, or io EINVAL with OP_RECOVER for an entry with no UTF-8 spelling, which only windows can hold |

### commit_replacing_owned_native

```mach
pub fun commit_replacing_owned_native[T](t: *Transaction, ctx: *T,
    owns: fun(*T, *Unit, bool) bool) res[Outcome, Error]
```

commit_replacing_owned with an owns callback that takes each path relative to
the target in native units, joined with `/`, so a tree holding a name with no
UTF-8 spelling can be replaced

## Outcome

```mach
pub rec Outcome {
    committed: bool;
    # the durability that was reached, which may be less than was requested
    achieved: Durability;
    # true when less was reached than was requested and the request allowed it
    shortfall: bool;
}
```

what a commit actually achieved

## BackupOutcome

```mach
pub rec BackupOutcome {
    consumed:        bool;
    prior_moved:     bool;
    published:       bool;
    achieved:        Durability;
    shortfall:       bool;
    failure:         err[Error];
    cleanup_failure: err[Error];
    # owned by the caller with the transaction allocator, nil after successful cleanup
    staging_residue: str;
}
```

exact effects of a caller-journaled file publication, including failure

## Entry

```mach
pub rec Entry {
    rel:    str;
    kind:   EntryKind;
    data:   *u8;
    len:    usize;
    mode:   i32;
    native: std.system.os.NativePath;
}
```

one item in a subtree about to be published

| Field | Type | |
| :--- | :--- | :--- |
| `rel` | `str` | canonical path relative to the subtree root, in UTF-8, or nil for an entry named in native units |
| `native` | `std.system.os.NativePath` | the same path in native units. entry_file_native and entry_dir_native borrow it, inventory_push converts rel into it once, and inventory_dnit releases it |

### entry_file

```mach
pub fun entry_file(rel: str, data: *u8, len: usize, mode: i32) Entry
```

### entry_dir

```mach
pub fun entry_dir(rel: str, mode: i32) Entry
```

### entry_file_native

```mach
pub fun entry_file_native(rel: *Unit, data: *u8, len: usize, mode: i32) Entry
```

entry_file for a canonical path in native units, borrowed until the
inventory is released

### entry_dir_native

```mach
pub fun entry_dir_native(rel: *Unit, mode: i32) Entry
```

entry_dir for a canonical path in native units, borrowed until the
inventory is released

## Inventory

```mach
pub rec Inventory {
    entries: Vector[Entry];
}
```

the complete contents of a subtree to publish

collected up front so the whole shape is known before anything is written,
which is what lets a subtree be built privately and moved into place in one
step rather than appearing a file at a time.

### inventory_init

```mach
pub fun inventory_init(alloc: *std.allocator.Allocator) Inventory
```

### inventory_dnit

```mach
pub fun inventory_dnit(inv: *Inventory) err[std.allocator.Error]
```

### inventory_push

```mach
pub fun inventory_push(inv: *Inventory, e: Entry) err[Error]
```

add an item, refusing a path that is not canonical or that repeats one
already added. a UTF-8 path is converted here, once, so every path in the
inventory is held and compared in native units

## Descent

```mach
pub rec Descent {
    # a capability over the deepest directory that already exists
    root: Root;
    # the first component under `root` that does not exist, a single component
    first_missing: str;
    # the rest of the requested path below `first_missing`, possibly empty
    remainder: str;
}
```

a root at the deepest existing ancestor of a path, and what was missing

publishing `a/b/c` when `a` does not exist yet must create `a`, `a/b` and
`a/b/c` together: a reader must never see a half-built `a`. `descend` finds
where the existing tree stops, so the caller can stage the entire missing
chain privately and publish it with one rename of `first_missing`.

### descend

```mach
pub fun descend(out: *Descent, alloc: *std.allocator.Allocator, base: Path, rel: Path) res[bool, Error]
```

find where an existing tree stops along `rel`

every component up to the first missing one must be a real directory,
checked without following symlinks, exactly as `root_open` does.

| Parameter | |
| :--- | :--- |
| `alloc` | allocator for the returned strings |
| `base` | absolute path of the anchor directory |
| `rel` | canonical relative path beneath `base` |
| **returns** | true when out owns the first missing location, false when all of rel exists failure retains the primary cause and first cleanup error, with no new descent |

### descent_dnit

```mach
pub fun descent_dnit(alloc: *std.allocator.Allocator, d: *Descent) err[Error]
```

release a descent and everything it allocated

## NativeDescent

```mach
pub rec NativeDescent {
    root:          Root;
    first_missing: *Unit;
    remainder:     *Unit;
}
```

a descent whose names are in native units

| Field | Type | |
| :--- | :--- | :--- |
| `first_missing` | `*Unit` | the first missing component under root, one component |
| `remainder` | `*Unit` | the rest of the requested path below it, or nil |

### descend_native

```mach
pub fun descend_native(out: *NativeDescent, alloc: *std.allocator.Allocator, base: *Unit, rel: *Unit) res[bool, Error]
```

descend for a base and rel in native units, the walk done in them

### native_descent_dnit

```mach
pub fun native_descent_dnit(alloc: *std.allocator.Allocator, d: *NativeDescent) err[Error]
```

release a native descent and everything it allocated

## Functions

### identity_equal

```mach
pub fun identity_equal(a: Identity, b: Identity) bool
```

### identity_encode

```mach
pub fun identity_encode(value: Identity, out: *u8, capacity: usize) bool
```

### identity_decode

```mach
pub fun identity_decode(text: str, out: *Identity) bool
```

### root_fd

```mach
pub fun root_fd(r: *Root) usize
```

the descriptor behind a root, for callers that must reach the operating
system directly. the root retains ownership; do not close it.

### root_home_fd

```mach
pub fun root_home_fd(r: *Root) usize
```

the directory holding the root's lock sentinel, claims and backups: the
root itself unless it was opened with a home. the root retains ownership.

### coordinator_entry

```mach
pub fun coordinator_entry(name: str) bool
```

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `IDENTITY_TEXT_CAPACITY` | `usize` | `identities.TEXT_CAPACITY` | complete observations have backend-qualified scope and do not retain an object |
| `LOCK_LEAF` | `str` | `".mach-txn-lock"` | the sentinel file a root lock is taken on |
| `STAGING_TAG` | `str` | `".machtxn."` | the prefix on every entry this module creates while a transaction is in flight |

## Forwards

### Identity

Forwards [`std.system.file_identity.Identity`](../system/file_identity.md#identity).

```mach
pub rec Identity {
    representation: [41]u8;
}
```

opaque to filesystem callers, native producers initialize every byte

### METADATA_ONLY

Forwards [`std.system.file_identity.METADATA_ONLY`](../system/file_identity.md#access).

```mach
pub val METADATA_ONLY:   Access = 0
```

### READ_AUTHORIZED

Forwards [`std.system.file_identity.READ_AUTHORIZED`](../system/file_identity.md#access).

```mach
pub val READ_AUTHORIZED: Access = 1
```

### Root

Forwards [`std.filesystem.transaction.ownership.Root`](transaction/ownership.md#root), only where `capability.HAS_FILES && capability.HAS_PAGES && capability.HAS_THREADS`.

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

### Lock

Forwards [`std.filesystem.transaction.ownership.Lock`](transaction/ownership.md#lock), only where `capability.HAS_FILES && capability.HAS_PAGES && capability.HAS_THREADS`.

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

