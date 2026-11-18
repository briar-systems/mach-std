# Darwin active CPU query probe

`verify.py` checks `os.cpu_count` and its `sysctlbyname` binding against the host
SDK. Run it on a native darwin host whose architecture matches the target, once per
profile, or run every darwin fixture with `test/lib/darwin-fixtures.py`:

```sh
python3 test/cpu-darwin/verify.py <mach> darwin-aarch64 debug
python3 test/cpu-darwin/verify.py <mach> darwin-aarch64 release
```

- `native.c` statically checks the SDK's `sysctlbyname` signature and the LP64
  widths, and prints the host's `hw.activecpu` and `hw.ncpu` around a third read.
- `cpu observe` reads `hw.activecpu` directly around the wrapper and `hw.ncpu`,
  and requires every answer to be a positive count.
- `cpu errors` queries a name that does not exist through the direct binding and
  must print exactly what `native.c errors` prints: the failing result, the errno
  and the untouched output.

The wrapper's minimum-one policy is the production contract. It does not promise
affinity limits, topology or a value stable over time.
