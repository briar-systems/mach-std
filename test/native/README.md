# Native suite profiles

`verify.sh` selects `debug` for ELF and Mach-O targets. These runs use optimization
level 0 and include debug symbols. Windows selects `windows-opt0`, which uses
optimization level 0 without symbols because the COFF backend has no registered
debug model. These Windows runs test runtime behavior and do not claim symbol
coverage.

The separate `release` ownership run uses optimization level 2 without debug
symbols on every target. Pass the desired profile explicitly when invoking the
native suite directly, for example:

```sh
mach test test/native --target windows-x86_64 --profile windows-opt0 --include-deps
```
