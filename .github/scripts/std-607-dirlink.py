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
windows = Path('src/system/os/windows/shared.mach').read_text(encoding="utf-8")
filesystem = Path('src/filesystem.mach').read_text(encoding="utf-8")
fixture = '''
fun audit607_dirlink(existing: bool) i32 {
    var target: str = "mach_607_dirlink_absent_target";
    var from: str = "mach_607_dirlink_absent_from";
    var to: str = "mach_607_dirlink_absent_to";
    if (existing) {
        target = "mach_607_dirlink_existing_target";
        from = "mach_607_dirlink_existing_from";
        to = "mach_607_dirlink_existing_to";
    }
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
        ('local-extended-directory-bit', windows.replace(replacement, condition), False),
        ('local-basic-directory-bit', basic.replace(replacement, condition), False),
        ('local-extended-real-directory', windows.replace(condition, replacement), False),
        ('local-basic-real-directory', basic.replace(condition, replacement), False),
        ('unc-selected-directory-bit', windows.replace(replacement, condition), True),
        ('unc-selected-real-directory', windows.replace(condition, replacement), True),
    ]:
        shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
        body = fixture
        if remote:
            body = body.replace('"mach_607_dirlink_', '"//localhost/MachStd607/mach_607_dirlink_')
        (snapshot / 'src/filesystem.mach').write_text(filesystem + body, newline='', encoding="utf-8")
        (snapshot / 'src/system/os/windows/shared.mach').write_text(modified, newline='', encoding="utf-8")
        census(name, 'windows')
        result = subprocess.run(['mach', 'test', 'test/native', '--target', 'windows-x86_64', '--include-deps', '--filter', 'std.filesystem.audit607_dirlink:'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = result.stdout.decode('utf-8', errors='replace')
        Path('std-607-evidence/' + name + '.log').write_text(log, encoding="utf-8")
        clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
        counts = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
        counts = list(map(int, counts[-1])) if counts else None
        exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
        record = dict(name=name, counts=counts, exits=exits, compiler_exit=result.returncode)
        print(json.dumps(record), flush=True)
        results.append(record)
        Path('std-607-evidence/dirlink-summary.json').write_text(json.dumps(results, indent=2), encoding="utf-8")
        if name.endswith('directory-bit'):
            assert counts == [1,1,2] and exits == ['17'] and result.returncode == 1, record
        else:
            assert counts == [2,0,2] and exits == [] and result.returncode == 0, record
finally:
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    subprocess.run(['git', 'diff', '--exit-code', 'e430a14', '--', 'src', 'mach.toml'], check=True)
