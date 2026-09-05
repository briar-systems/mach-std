import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess

snapshot = Path('test/native/dep/std')
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
source = snapshot / 'src/filesystem.mach'
text = source.read_text(encoding='utf-8')
text = text.replace('    if (O.is_some[str](rename(from, to))) { ret 73; }',
    '    val raw: i64 = os.rename(os.AT_FDCWD, from, os.AT_FDCWD, to);\n    if (raw < 0) { ret (0 - raw)::i32; }')
text += '''
test "std.filesystem.audit607_unc: closed destination replacement" {
    val from: str = "//localhost/MachStd607/mach_607_unc_closed_from";
    val to: str = "//localhost/MachStd607/mach_607_unc_closed_to";
    if (O.is_some[str](write_bytes(from, "new", 3, 0o600))) { ret 61; }
    fin { remove_file(from); }
    if (O.is_some[str](write_bytes(to, "old", 3, 0o600))) { ret 62; }
    fin { remove_file(to); }
    val raw: i64 = os.rename(os.AT_FDCWD, from, os.AT_FDCWD, to);
    if (raw < 0) { ret (0 - raw)::i32; }
    val opened: R.Result[File, io_error.Error] = open(to);
    if (R.is_err[File, io_error.Error](opened)) { ret 63; }
    var file: File = R.unwrap_ok[File, io_error.Error](opened);
    fin { close(?file); }
    if (!rename_held_contents(file, "new")) { ret 64; }
    ret 0;
}
test "std.filesystem.audit607_unc: held destination replacement" {
    ret rename_held_pair("//localhost/MachStd607/mach_607_unc_held_from",
        "//localhost/MachStd607/mach_607_unc_held_to");
}
'''
source.write_text(text, encoding='utf-8', newline='')
census = runpy.run_path('.github/scripts/std-607-census.py')['census']
windows_path = snapshot / 'src/system/os/windows/shared.mach'
base_windows = windows_path.read_text(encoding='utf-8')
results = []
types = text[text.index('fun rename_type_conflicts('):text.index('test "std.filesystem.rename: type conflicts')]
types = types.replace('rename_type_conflicts', 'audit607_unc_types')
types = types.replace('"mach_std_rename_type_file"', '"//localhost/MachStd607/mach_std_rename_type_file"')
types = types.replace('"mach_std_rename_type_directory"', '"//localhost/MachStd607/mach_std_rename_type_directory"')
types = types.replace('os.AT_FDCWD, ".",', 'os.AT_FDCWD, "//localhost/MachStd607",')
types = types.replace('    if (os.rename(dirfd, file_path, dirfd, dir_path)', '''    var source_name: str = file_path;
    var target_name: str = dir_path;
    if (rooted) { source_name = path.filename(file_path); target_name = path.filename(dir_path); }
    if (os.rename(dirfd, source_name, dirfd, target_name)''')
types = types.replace('os.rename(dirfd, dir_path, dirfd, file_path)', 'os.rename(dirfd, target_name, dirfd, source_name)')
types += '''
test "std.filesystem.audit607_unc: public type conflicts" { ret audit607_unc_types(false); }
test "std.filesystem.audit607_unc: rooted type conflicts" { ret audit607_unc_types(true); }
'''
text += types
diagnostic = base_windows.replace('if (device_status < 0) { ret ntstatus_error(device_status); }', 'if (device_status < 0) { ret -101; }').replace('if (attribute_status < 0 && attribute_status != 0x80000005::u32::i32) { ret ntstatus_error(attribute_status); }', 'if (attribute_status < 0 && attribute_status != 0x80000005::u32::i32) { ret -103; }')
diagnostic = diagnostic.replace('GetFileInformationByHandleEx(source, FILE_REMOTE_PROTOCOL_INFO_CLASS, (?remote)::ptr, $size_of(FILE_REMOTE_PROTOCOL_INFO)::u32) == 0) {\n            ret last_error();', 'GetFileInformationByHandleEx(source, FILE_REMOTE_PROTOCOL_INFO_CLASS, (?remote)::ptr, $size_of(FILE_REMOTE_PROTOCOL_INFO)::u32) == 0) {\n            ret -102;')
owned = diagnostic.replace('var remote: FILE_REMOTE_PROTOCOL_INFO;', 'val remote: *FILE_REMOTE_PROTOCOL_INFO = allocate($size_of(FILE_REMOTE_PROTOCOL_INFO))::*FILE_REMOTE_PROTOCOL_INFO; if (remote == nil) { ret ENOMEM; } fin { deallocate(remote::ptr, $size_of(FILE_REMOTE_PROTOCOL_INFO)); }')
owned = owned.replace('(?remote)::ptr', 'remote::ptr')
for name, source_text, modified, expected, expected_exits in [
    ('query-failure-phase', text, diagnostic, None, None),
    ('owned-remote-record', text, owned, None, None),
]:
    source.write_text(source_text, encoding='utf-8', newline='')
    windows_path.write_text(modified, encoding='utf-8', newline='')
    census(name, 'windows')
    result = subprocess.run(['mach', 'test', 'test/native', '--target', 'windows-x86_64',
        '--include-deps', '--filter', 'std.filesystem.audit607_unc:'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = result.stdout.decode('utf-8', errors='replace')
    Path('std-607-evidence/' + name + '.log').write_text(log, encoding='utf-8')
    clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
    counts = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
    counts = list(map(int, counts[-1])) if counts else None
    exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
    record = dict(name=name, counts=counts, exits=exits, compiler_exit=result.returncode)
    print(json.dumps(record), flush=True)
    results.append(record)
    Path('std-607-evidence/unc-summary.json').write_text(json.dumps(results, indent=2))
    assert counts is not None and counts[2] == 4, record
shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
subprocess.run(['git', 'diff', '--exit-code', '7e02b68', '--', 'src', 'mach.toml'], check=True)
