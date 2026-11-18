[std](../README.md) / [encoding](README.md) / **base64**

# std.encoding.base64

base64 encoding and decoding

Source: [`src/encoding/base64.mach`](../../../src/encoding/base64.mach)

| Functions | |
| :--- | :--- |
| [`encoded_len`](#encoded_len) | return the buffer size required to encode src_len bytes (including null terminator) |
| [`decoded_len`](#decoded_len) | return the maximum number of decoded bytes for a base64 string of src_len chars |
| [`encode`](#encode) | encode bytes as standard base64 with padding |
| [`encode_url`](#encode_url) | encode bytes as url-safe base64 without padding |
| [`decode`](#decode) | decode a base64 string to bytes |

---

## Functions

### encoded_len

```mach
pub fun encoded_len(src_len: usize) opt[usize]
```

return the buffer size required to encode src_len bytes (including null terminator)

| Parameter | |
| :--- | :--- |
| `src_len` | number of source bytes |
| **returns** | required destination buffer size, none when it does not fit usize |

### decoded_len

```mach
pub fun decoded_len(src_len: usize) usize
```

return the maximum number of decoded bytes for a base64 string of src_len chars

| Parameter | |
| :--- | :--- |
| `src_len` | length of the base64 string |
| **returns** | maximum decoded byte count |

### encode

```mach
pub fun encode(src: *u8, src_len: usize, dst: *u8, dst_len: usize) usize
```

encode bytes as standard base64 with padding

| Parameter | |
| :--- | :--- |
| `src` | pointer to source bytes |
| `src_len` | number of source bytes |
| `dst` | pointer to destination buffer |
| `dst_len` | size of destination buffer (must be >= encoded_len(src_len)) |
| **returns** | number of bytes written (not counting null terminator), 0 if dst too small |

### encode_url

```mach
pub fun encode_url(src: *u8, src_len: usize, dst: *u8, dst_len: usize) usize
```

encode bytes as url-safe base64 without padding

| Parameter | |
| :--- | :--- |
| `src` | pointer to source bytes |
| `src_len` | number of source bytes |
| `dst` | pointer to destination buffer |
| `dst_len` | size of destination buffer (must be >= encoded_len(src_len)) |
| **returns** | number of bytes written (not counting null terminator), 0 if dst too small |

### decode

```mach
pub fun decode(src: *u8, src_len: usize, dst: *u8, dst_len: usize) usize
```

decode a base64 string to bytes

handles both standard and url-safe alphabets, and padding characters.

| Parameter | |
| :--- | :--- |
| `src` | pointer to base64 string |
| `src_len` | length of the base64 string |
| `dst` | pointer to destination buffer |
| `dst_len` | size of destination buffer (must be >= decoded_len(src_len)) |
| **returns** | number of bytes written, 0 on invalid input or dst too small |

