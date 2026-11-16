[std](../README.md) / [filesystem](README.md) / **removal**

# std.filesystem.removal

descriptor-relative recursive removal shared by namespace and transaction callers

the walk runs in std.runtime.native units, so an entry whose name, or any
name below it, has no UTF-8 spelling is removed like any other. a UTF-8
name is converted once and then walked the same way

Source: [`src/filesystem/removal.mach`](../../../src/filesystem/removal.mach)

Uses types from [`std.io.error`](../io/error.md).

| Type | | |
| :--- | :--- | :--- |
| [`Error`](#error) | `rec` |  |

| On `Error` | |
| :--- | :--- |
| [`message`](#message) | |
| [`from_native`](#from_native) | the error for a native code a primitive returned |
| [`contained`](#contained) | the error for a component or depth removal will not walk |
| [`with_cleanup`](#with_cleanup) | keep the primary failure when releasing a cursor or descriptor also fails |
| [`tree`](#tree) | count is usable only when the complete operation succeeds |
| [`tree_native`](#tree_native) | tree for an entry named in native units |
| [`private_tree`](#private_tree) | only for transaction-owned private trees under an exclusive cooperative root claim |
| [`private_tree_native`](#private_tree_native) | private_tree for an entry named in native units |

---

## Error

```mach
pub rec Error {
    kind: std.io.error.Kind;
    # the native code behind the failure, 0 when removal refused on its own
    code:        i64;
    containment: bool;
    # first independent cleanup failure
    cleanup_code: i64;
}
```

### message

```mach
pub fun message(e: Error) str
```

### from_native

```mach
pub fun from_native(code: i64) Error
```

the error for a native code a primitive returned

### contained

```mach
pub fun contained() Error
```

the error for a component or depth removal will not walk

### with_cleanup

```mach
pub fun with_cleanup(result: err[Error], code: i64) err[Error]
```

keep the primary failure when releasing a cursor or descriptor also fails

### tree

```mach
pub fun tree(dirfd: usize, name: str, removed: *usize, max_depth: usize) err[Error]
```

count is usable only when the complete operation succeeds

### tree_native

```mach
pub fun tree_native(dirfd: usize, name: *Unit, removed: *usize, max_depth: usize) err[Error]
```

tree for an entry named in native units

### private_tree

```mach
pub fun private_tree(dirfd: usize, name: str, removed: *usize, max_depth: usize) err[Error]
```

only for transaction-owned private trees under an exclusive cooperative root claim

### private_tree_native

```mach
pub fun private_tree_native(dirfd: usize, name: *Unit, removed: *usize, max_depth: usize) err[Error]
```

private_tree for an entry named in native units

