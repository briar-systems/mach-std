[std](../../README.md) / [math](../README.md) / **bignum**

# std.math.bignum

fixed-capacity big integer

a std.math.bignum.nat.Nat over LIMBS inline limbs (4096 bits), for a caller
whose values have a known small bound. the float conversions do not use it:
they size their own Nat storage from the format row (see std.math.ieee).

The directory's root module is [`std.math.bignum`](../bignum.md).

| Module | |
| :--- | :--- |
| [`nat`](nat.md) | unsigned big integer over caller storage |

