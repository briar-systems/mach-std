[std](../README.md) / [system](README.md) / **file_identity**

# std.system.file_identity

observational identity within one host and its current mounted namespace

Source: [`src/system/file_identity.mach`](../../../src/system/file_identity.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Access`](#access) | `def` | maximum access authorized while retaining identity, never a required upgrade |
| [`Identity`](#identity) | `rec` | opaque to filesystem callers, native producers initialize every byte |

| On `Access` | |
| :--- | :--- |
| [`METADATA_ONLY`](#access), [`READ_AUTHORIZED`](#access) | |

| On `Identity` | |
| :--- | :--- |
| [`equal`](#equal) | compare two identities byte for byte |
| [`lasting`](#lasting) | whether an identity names its file for as long as the file exists |
| [`encode`](#encode) | failure leaves the output untouched |
| [`decode`](#decode) | only the complete current representation is accepted |
| [`native`](#native) | build an identity from a backend's volume and file numbers |

| Constants | |
| :--- | :--- |
| [`LINUX_LOCAL`](#constants), [`DARWIN_LOCAL`](#constants), [`WINDOWS_LOCAL`](#constants), [`WASI_LOCAL`](#constants) | |
| [`WINDOWS_ENTRY`](#constants) | a windows volume with no stable file id, such as fat or exfat: the volume serial and the 64-bit file index, which names the file's directory entry |
| [`TEXT_CAPACITY`](#constants) | |

---

## Access

```mach
pub def Access: u8
```

maximum access authorized while retaining identity, never a required upgrade

| Name | Value | |
| :--- | :--- | :--- |
| `METADATA_ONLY` | `0` |  |
| `READ_AUTHORIZED` | `1` |  |

## Identity

```mach
pub rec Identity {
    representation: [41]u8;
}
```

opaque to filesystem callers, native producers initialize every byte

byte 0 is the backend, bytes 1 to 16 are zero, bytes 17 to 24 hold the
volume and 25 to 32 the file number, little-endian. bytes 33 to 40 are zero
except for WINDOWS_LOCAL, whose file id is 128 bits

| Field | Type | |
| :--- | :--- | :--- |
| `representation` | `[41]u8` | the 41 identity bytes |

### equal

```mach
pub fun equal(a: Identity, b: Identity) bool
```

compare two identities byte for byte

| Parameter | |
| :--- | :--- |
| `a` | first identity |
| `b` | second identity |
| **returns** | true when both are well formed and identical |

### lasting

```mach
pub fun lasting(value: Identity) bool
```

whether an identity names its file for as long as the file exists

a WINDOWS_ENTRY identity names a directory entry: two entries that exist at
once differ, but a file's entry can move when the file is renamed or its
directory is reorganized, and a freed entry is reused by the next file made
there. it compares soundly only between observations taken while the file
stays open and unrenamed, never across a close or once stored for later

| Parameter | |
| :--- | :--- |
| `value` | a well-formed identity |
| **returns** | false for WINDOWS_ENTRY, true for every other backend |

### encode

```mach
pub fun encode(value: Identity, out: *u8, capacity: usize) bool
```

failure leaves the output untouched

writes the identity as 82 lowercase hex digits and a terminating nul

| Parameter | |
| :--- | :--- |
| `value` | identity to encode |
| `out` | destination buffer |
| `capacity` | bytes at out, at least TEXT_CAPACITY |
| **returns** | false for a nil out, a short buffer or a malformed identity |

### decode

```mach
pub fun decode(text: str, out: *Identity) bool
```

only the complete current representation is accepted

| Parameter | |
| :--- | :--- |
| `text` | 82 hex digits as encode writes them |
| `out` | receives the identity, untouched on failure |
| **returns** | false for nil operands, a wrong length, bad digits or a malformed identity |

### native

```mach
pub fun native(backend: u8, volume: u64, file: u64) Identity
```

build an identity from a backend's volume and file numbers

| Parameter | |
| :--- | :--- |
| `backend` | one of the *_LOCAL backend bytes |
| `volume` | volume or device number |
| `file` | file number within the volume |
| **returns** | the identity, every other byte zero |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `LINUX_LOCAL` | `u8` | `1` |  |
| `DARWIN_LOCAL` | `u8` | `2` |  |
| `WINDOWS_LOCAL` | `u8` | `3` |  |
| `WASI_LOCAL` | `u8` | `4` |  |
| `WINDOWS_ENTRY` | `u8` | `5` | a windows volume with no stable file id, such as fat or exfat: the volume serial and the 64-bit file index, which names the file's directory entry |
| `TEXT_CAPACITY` | `usize` | `83` |  |

