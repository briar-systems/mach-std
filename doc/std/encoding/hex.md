[std](../README.md) / [encoding](README.md) / **hex**

# std.encoding.hex

hexadecimal encoding and decoding

Source: [`src/encoding/hex.mach`](../../../src/encoding/hex.mach)

| Functions | |
| :--- | :--- |
| [`encoded_len`](#encoded_len) | return the buffer size required to encode src_len bytes (including null terminator) |
| [`decoded_len`](#decoded_len) | return the maximum number of decoded bytes for a hex string of src_len chars |
| [`encode`](#encode) | encode bytes as lowercase hexadecimal |
| [`encode_upper`](#encode_upper) | encode bytes as uppercase hexadecimal |
| [`decode`](#decode) | decode a hexadecimal string to bytes |

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

return the maximum number of decoded bytes for a hex string of src_len chars

| Parameter | |
| :--- | :--- |
| `src_len` | length of the hex string |
| **returns** | maximum decoded byte count |

### encode

```mach
pub fun encode(src: *u8, src_len: usize, dst: *u8, dst_len: usize) usize
```

encode bytes as lowercase hexadecimal

| Parameter | |
| :--- | :--- |
| `src` | pointer to source bytes |
| `src_len` | number of source bytes |
| `dst` | pointer to destination buffer |
| `dst_len` | size of destination buffer (must be >= encoded_len(src_len)) |
| **returns** | number of bytes written (not counting null terminator), 0 if dst too small |

### encode_upper

```mach
pub fun encode_upper(src: *u8, src_len: usize, dst: *u8, dst_len: usize) usize
```

encode bytes as uppercase hexadecimal

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

decode a hexadecimal string to bytes

accepts both uppercase and lowercase hex characters.
returns 0 if the input has odd length or contains invalid characters.

| Parameter | |
| :--- | :--- |
| `src` | pointer to hex string |
| `src_len` | length of the hex string |
| `dst` | pointer to destination buffer |
| `dst_len` | size of destination buffer (must be >= decoded_len(src_len)) |
| **returns** | number of bytes written, 0 on invalid input or dst too small |

