# Darwin entropy boundary probe

`verify.py` checks `os.random_fill` and its `getentropy` binding against the host
SDK. Run it on a native darwin host whose architecture matches the target, once per
profile, or run every darwin fixture with `test/lib/darwin-fixtures.py`:

```sh
python3 test/entropy-darwin/verify.py <mach> darwin-aarch64 debug
python3 test/entropy-darwin/verify.py <mach> darwin-aarch64 release
```

- `native.c` statically checks the SDK's `getentropy` signature and the LP64 widths.
- `entropy smoke` fills spans of 0, 1, 255, 256, 257, 512 and 1025 bytes between
  guard bytes through `std.crypto.rand`, which crosses `getentropy`'s 256-byte limit
  in the wrapper's chunk loop, and requires both guards intact. It does not judge the
  randomness.
- `entropy errors` makes an oversized and an invalid request through the binding
  and the wrapper. Its line must equal `native.c errors`: the errnos the SDK
  reports, and an oversized failure leaves its buffer untouched.
