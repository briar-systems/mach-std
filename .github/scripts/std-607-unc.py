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
text = text.replace('    val raw: i64 = os.rename(os.AT_FDCWD, from, os.AT_FDCWD, to);', '''    val parent: i64 = os.open(os.AT_FDCWD, "//localhost/MachStd607", os.O_RDONLY | os.O_DIRECTORY, 0);
    if (parent < 0) { ret (0 - parent)::i32; }
    val raw: i64 = os.rename(os.AT_FDCWD, from, parent::i32, path.filename(to));
    os.close(parent::i32);''')
source.write_text(text, encoding='utf-8', newline='')
census = runpy.run_path('.github/scripts/std-607-census.py')['census']
windows_path = snapshot / 'src/system/os/windows/shared.mach'
base_windows = windows_path.read_text(encoding='utf-8')
results = []
for name, info_class, flags, basename in [
    ('extended-posix-parent', 65, 3, False),
    ('extended-replace-parent', 65, 1, False),
    ('legacy-replace-parent', 10, 1, False),
]:
    modified = base_windows.replace('val FILE_RENAME_INFORMATION_EX_CLASS:   u32 = 65;',
        'val FILE_RENAME_INFORMATION_EX_CLASS:   u32 = ' + str(info_class) + ';')
    modified = modified.replace('info.flags = FILE_RENAME_REPLACE_IF_EXISTS | FILE_RENAME_POSIX_SEMANTICS;',
        'info.flags = ' + str(flags) + ';')
    if basename:
        modified = modified.replace('or { result = native_rename_handle(source, 0, native.buffer, native.length::usize / 2); }',
            'or { var start: usize = 0; var i: usize = 0; val length: usize = native.length::usize / 2; for (i < length) { if (native.buffer[i] == 92) { start = i + 1; } i = i + 1; } result = native_rename_handle(source, 0, ?native.buffer[start], length - start); }')
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
    assert counts is not None and counts[2] == 2 and result.returncode in (0, 1), record
shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
subprocess.run(['git', 'diff', '--exit-code', 'e0eee1164491c003f774dc8318f23fd72eefb130', '--', 'src', 'mach.toml'], check=True)
