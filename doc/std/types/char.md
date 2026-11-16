[std](../README.md) / [types](README.md) / **char**

# std.types.char

Source: [`src/types/char.mach`](../../../src/types/char.mach)

| Type | | |
| :--- | :--- | :--- |
| [`char`](#char) | `def` | a single byte representing a character |

| On `char` | |
| :--- | :--- |
| [`char_is_space`](#char_is_space) | check if a character is ASCII whitespace |
| [`char_is_digit`](#char_is_digit) | check if a character is an ASCII digit |
| [`char_is_alpha`](#char_is_alpha) | check if a character is an ASCII letter |
| [`char_is_alnum`](#char_is_alnum) | check if a character is alphanumeric |
| [`char_is_lower`](#char_is_lower) | check if a character is a lowercase ASCII letter |
| [`char_is_upper`](#char_is_upper) | check if a character is an uppercase ASCII letter |
| [`char_to_lower`](#char_to_lower) | convert an ASCII letter to lowercase |
| [`char_to_upper`](#char_to_upper) | convert an ASCII letter to uppercase |
| [`char_is_hex_digit`](#char_is_hex_digit) | check if a character is a hexadecimal digit |
| [`char_is_punct`](#char_is_punct) | check if a character is ASCII punctuation |
| [`char_is_print`](#char_is_print) | check if a character is printable ASCII |
| [`char_is_ctrl`](#char_is_ctrl) | check if a character is an ASCII control character |
| [`char_digit_val`](#char_digit_val) | get the numeric value of a digit or letter character |

---

## char

```mach
pub def char: u8
```

a single byte representing a character

### char_is_space

```mach
pub fun char_is_space(c: char) bool
```

check if a character is ASCII whitespace

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if whitespace (space, tab, newline, vertical tab, form feed, carriage return) |

### char_is_digit

```mach
pub fun char_is_digit(c: char) bool
```

check if a character is an ASCII digit

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if 0-9 |

### char_is_alpha

```mach
pub fun char_is_alpha(c: char) bool
```

check if a character is an ASCII letter

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if a-z or A-Z |

### char_is_alnum

```mach
pub fun char_is_alnum(c: char) bool
```

check if a character is alphanumeric

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if letter or digit |

### char_is_lower

```mach
pub fun char_is_lower(c: char) bool
```

check if a character is a lowercase ASCII letter

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if a-z |

### char_is_upper

```mach
pub fun char_is_upper(c: char) bool
```

check if a character is an uppercase ASCII letter

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if A-Z |

### char_to_lower

```mach
pub fun char_to_lower(c: char) char
```

convert an ASCII letter to lowercase

| Parameter | |
| :--- | :--- |
| `c` | character to convert |
| **returns** | lowercase equivalent, or c unchanged if not uppercase |

### char_to_upper

```mach
pub fun char_to_upper(c: char) char
```

convert an ASCII letter to uppercase

| Parameter | |
| :--- | :--- |
| `c` | character to convert |
| **returns** | uppercase equivalent, or c unchanged if not lowercase |

### char_is_hex_digit

```mach
pub fun char_is_hex_digit(c: char) bool
```

check if a character is a hexadecimal digit

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if 0-9, a-f, or A-F |

### char_is_punct

```mach
pub fun char_is_punct(c: char) bool
```

check if a character is ASCII punctuation

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if punctuation |

### char_is_print

```mach
pub fun char_is_print(c: char) bool
```

check if a character is printable ASCII

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if printable (space through tilde) |

### char_is_ctrl

```mach
pub fun char_is_ctrl(c: char) bool
```

check if a character is an ASCII control character

| Parameter | |
| :--- | :--- |
| `c` | character to test |
| **returns** | true if control character |

### char_digit_val

```mach
pub fun char_digit_val(c: char) i32
```

get the numeric value of a digit or letter character

| Parameter | |
| :--- | :--- |
| `c` | character to evaluate |
| **returns** | 0-9 for digits, 10-35 for letters, or -1 if invalid |

