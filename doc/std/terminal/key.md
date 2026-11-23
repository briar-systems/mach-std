[std](../README.md) / [terminal](README.md) / **key**

# std.terminal.key

decoded keyboard key shared by std.terminal and its per-os backends

a Key is one of three variants tagged by `kind`: nothing was waiting, an
ordinary byte, or a special (non-textual) key such as an arrow. the tag keeps
a raw byte from ever being confused with a sentinel, unlike a single shared
int space. lives in its own module so both the parent (std.terminal) and the
backends can reference it without a circular import.

Source: [`src/terminal/key.mach`](../../../src/terminal/key.mach)

| Type | | |
| :--- | :--- | :--- |
| [`KeyKind`](#keykind) | `def` | which variant a Key holds |
| [`Special`](#special) | `def` | a special (non-byte) key |
| [`Key`](#key) | `rec` | a single decoded key event |

| On `KeyKind` | |
| :--- | :--- |
| [`KIND_NONE`](#keykind), [`KIND_BYTE`](#keykind), [`KIND_SPECIAL`](#keykind) | |

| On `Special` | |
| :--- | :--- |
| [`KEY_UP`](#special), [`KEY_DOWN`](#special), [`KEY_LEFT`](#special), [`KEY_RIGHT`](#special) | |
| [`key_special`](#key_special) | a Key holding a special (non-byte) key |

| On `Key` | |
| :--- | :--- |
| [`key_none`](#key_none) | a Key meaning nothing was waiting |
| [`key_byte`](#key_byte) | a Key holding an ordinary byte |
| [`is_none`](#is_none) | whether no key was waiting |
| [`is_byte`](#is_byte) | whether the key is an ordinary byte |
| [`is_special`](#is_special) | whether the key is a special (non-byte) key |

---

## KeyKind

```mach
pub def KeyKind: u8
```

which variant a Key holds

| Name | Value | |
| :--- | :--- | :--- |
| `KIND_NONE` | `0` |  |
| `KIND_BYTE` | `1` |  |
| `KIND_SPECIAL` | `2` |  |

## Special

```mach
pub def Special: u8
```

a special (non-byte) key

| Name | Value | |
| :--- | :--- | :--- |
| `KEY_UP` | `0` |  |
| `KEY_DOWN` | `1` |  |
| `KEY_LEFT` | `2` |  |
| `KEY_RIGHT` | `3` |  |

### key_special

```mach
pub fun key_special(s: Special) Key
```

a Key holding a special (non-byte) key

## Key

```mach
pub rec Key {
    kind:    KeyKind;
    byte:    u8;
    special: Special;
}
```

a single decoded key event

| Field | Type | |
| :--- | :--- | :--- |
| `kind` | `KeyKind` | which field is meaningful |
| `byte` | `u8` | the byte value when kind == KIND_BYTE |
| `special` | `Special` | the special key when kind == KIND_SPECIAL |

### key_none

```mach
pub fun key_none() Key
```

a Key meaning nothing was waiting

### key_byte

```mach
pub fun key_byte(b: u8) Key
```

a Key holding an ordinary byte

### is_none

```mach
pub fun is_none(k: Key) bool
```

whether no key was waiting

### is_byte

```mach
pub fun is_byte(k: Key) bool
```

whether the key is an ordinary byte

### is_special

```mach
pub fun is_special(k: Key) bool
```

whether the key is a special (non-byte) key

