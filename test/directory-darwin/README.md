# Darwin directory cursor probe

`verify.py` checks the darwin directory cursor (`fdopendir`, `readdir`,
`closedir`) against the host SDK. Run it on a native darwin host whose architecture matches the target, once per
profile, or run every darwin fixture with `test/lib/darwin-fixtures.py`:

```sh
python3 test/directory-darwin/verify.py <mach> darwin-aarch64 debug
python3 test/directory-darwin/verify.py <mach> darwin-aarch64 release
```

- `native.c` statically checks the SDK's cursor signatures, the `struct dirent`
  offsets and widths and the descriptor flags, and prints the host's layout and the
  `ENOTDIR` a regular file gets.
- `directory layout` requires `DirectoryRecord` to have the SDK's offsets.
- `directory errors` opens a cursor on a regular file: `ENOTDIR`, no cleanup error,
  the caller's descriptor still owned and the descriptor count unchanged.
- `directory borrowed` lists a directory renamed after the cursor opened, sees its
  one entry once, reads end of directory twice, and closes with the descriptor count
  back where it started.

The probes work in the fixture's `out` directory.
