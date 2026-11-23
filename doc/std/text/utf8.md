[std](../README.md) / [text](README.md) / **utf8**

# std.text.utf8

UTF-8 encoding, decoding, and validation

Source: [`src/text/utf8.mach`](../../../src/text/utf8.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Codepoint`](#codepoint) | `def` |  |

| On `Codepoint` | |
| :--- | :--- |
| [`REPLACEMENT`](#codepoint), [`MAX_CODEPOINT`](#codepoint) | |
| [`codepoint_len`](#codepoint_len) | return how many bytes are needed to encode a codepoint |
| [`encode`](#encode) | encode a codepoint into a byte buffer |
| [`decode`](#decode) | decode one codepoint from a byte buffer |

| Functions | |
| :--- | :--- |
| [`byte_len`](#byte_len) | return the sequence length from a UTF-8 leading byte |
| [`is_continuation`](#is_continuation) | true if the byte is a UTF-8 continuation byte (0x80-0xBF) |
| [`validate`](#validate) | check if a byte buffer contains valid UTF-8 |
| [`count`](#count) | count the number of codepoints in a UTF-8 byte buffer |

---

## Codepoint

```mach
pub def Codepoint: u32
```

| Name | Value | |
| :--- | :--- | :--- |
| `REPLACEMENT` | `0xFFFD` |  |
| `MAX_CODEPOINT` | `0x10FFFF` |  |

### codepoint_len

```mach
pub fun codepoint_len(cp: Codepoint) usize
```

return how many bytes are needed to encode a codepoint

| Parameter | |
| :--- | :--- |
| `cp` | the codepoint to measure |
| **returns** | 1-4 for valid codepoints, 0 if > U+10FFFF |

### encode

```mach
pub fun encode(cp: Codepoint, buf: *u8, len: usize) usize
```

encode a codepoint into a byte buffer

| Parameter | |
| :--- | :--- |
| `cp` | codepoint to encode |
| `buf` | destination buffer |
| `len` | size of buf in bytes |
| **returns** | bytes written (0 if buf too small or invalid codepoint) |

### decode

```mach
pub fun decode(buf: *u8, len: usize, cp: *Codepoint) usize
```

decode one codepoint from a byte buffer

| Parameter | |
| :--- | :--- |
| `buf` | source buffer |
| `len` | number of bytes available |
| `cp` | pointer to write the decoded codepoint |
| **returns** | bytes consumed (0 if invalid or empty; sets *cp to REPLACEMENT on error) |

## Functions

### byte_len

```mach
pub fun byte_len(first_byte: u8) usize
```

return the sequence length from a UTF-8 leading byte

| Parameter | |
| :--- | :--- |
| `first_byte` | the first byte of a UTF-8 sequence |
| **returns** | 1-4 from the leading bit pattern, 0 for a continuation byte or a byte from 0xF8 up (0xC0, 0xC1 and 0xF5-0xF7 still report 2 or 4, and decode rejects what they start) |

### is_continuation

```mach
pub fun is_continuation(b: u8) bool
```

true if the byte is a UTF-8 continuation byte (0x80-0xBF)

| Parameter | |
| :--- | :--- |
| `b` | byte to test |
| **returns** | true if continuation byte |

### validate

```mach
pub fun validate(buf: *u8, len: usize) bool
```

check if a byte buffer contains valid UTF-8

| Parameter | |
| :--- | :--- |
| `buf` | source buffer |
| `len` | number of bytes |
| **returns** | true if the entire buffer is valid UTF-8 |

### count

```mach
pub fun count(buf: *u8, len: usize) usize
```

count the number of codepoints in a UTF-8 byte buffer

| Parameter | |
| :--- | :--- |
| `buf` | source buffer |
| `len` | number of bytes |
| **returns** | number of codepoints (counts sequence starts, not bytes) |

