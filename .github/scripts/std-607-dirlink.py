import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess

census = runpy.run_path('.github/scripts/std-607-census.py')['census']
snapshot = Path('test/native/dep/std')
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
windows = Path('src/system/os/windows/shared.mach').read_text()
filesystem = Path('src/filesystem.mach').read_text()
fixture = '''
fun audit607_dirlink(existing: bool) i32 {
    val target: str = "mach_607_dirlink_target";
    val from: str = "mach_607_dirlink_from";
    val to: str = "mach_607_dirlink_to";
    if (O.is_some[str](create_dir(target, 0o700))) { ret 97; }
    fin { remove_dir(target); }
    if (O.is_some[str](symlink(target, from))) { ret 98; }
    fin { remove_dir(from); remove_file(from); remove_dir(to); remove_file(to); }
    val before: R.Result[Metadata, str] = metadata_link(from);
    if (R.is_err[Metadata, str](before)) { ret 96; }
    if (R.unwrap_ok[Metadata, str](before).kind != KIND_SYMLINK) { ret 95; }
    if (existing && O.is_some[str](write_bytes(to, "old", 3, 0o600))) { ret 94; }
    val raw: i64 = os.rename(os.AT_FDCWD, from, os.AT_FDCWD, to);
    if (raw < 0) { ret (0 - raw)::i32; }
    val moved: R.Result[Metadata, str] = metadata_link(to);
    if (R.is_err[Metadata, str](moved)) { ret 93; }
    if (R.unwrap_ok[Metadata, str](moved).kind != KIND_SYMLINK) { ret 92; }
    if (!is_dir(target) || exists(from)) { ret 91; }
    ret 0;
}
test "std.filesystem.audit607_dirlink: absent destination" { ret audit607_dirlink(false); }
test "std.filesystem.audit607_dirlink: regular file destination" { ret audit607_dirlink(true); }
'''
basic = windows.replace('fun native_rename_class(source: isize) i64 {', 'fun native_rename_class(source: isize) i64 {\n    ret FILE_RENAME_INFORMATION_CLASS::i64;')
condition = '(source_info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0'
replacement = '(source_info.dwFileAttributes & (FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_REPARSE_POINT)) == FILE_ATTRIBUTE_DIRECTORY'
results = []
try:
    for name, modified, remote in [
        ('local-extended-directory-bit', windows, False),
        ('local-basic-directory-bit', basic, False),
        ('local-extended-real-directory', windows.replace(condition, replacement), False),
        ('local-basic-real-directory', basic.replace(condition, replacement), False),
        ('unc-selected-directory-bit', windows, True),
        ('unc-selected-real-directory', windows.replace(condition, replacement), True),
    ]:
        shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
        body = fixture
        if remote:
            body = body.replace('"mach_607_dirlink_', '"//localhost/MachStd607/mach_607_dirlink_')
        (snapshot / 'src/filesystem.mach').write_text(filesystem + body, newline='')
        (snapshot / 'src/system/os/windows/shared.mach').write_text(modified, newline='')
        census(name, 'windows')
        result = subprocess.run(['mach', 'test', 'test/native', '--target', 'windows-x86_64', '--include-deps', '--filter', 'std.filesystem.audit607_dirlink:'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = result.stdout.decode('utf-8', errors='replace')
        Path('std-607-evidence/' + name + '.log').write_text(log)
        clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
        counts = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
        counts = list(map(int, counts[-1])) if counts else None
        exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
        record = dict(name=name, counts=counts, exits=exits, compiler_exit=result.returncode)
        print(json.dumps(record), flush=True)
        results.append(record)
        Path('std-607-evidence/dirlink-summary.json').write_text(json.dumps(results, indent=2))
        assert counts is not None and counts[2] == 2 and result.returncode in (0,1), record
finally:
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    subprocess.run(['git', 'diff', '--exit-code', 'c7e59c4', '--', 'src', 'mach.toml'], check=True)
