import json
import pathlib
import re
import shutil
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[2]
source = root / 'src/filesystem/transaction.mach'
baseline = '7742cf4'
subprocess.run(['git', 'diff', '--exit-code', baseline, '--', 'src', 'mach.toml'], cwd=root, check=True)
pristine = source.read_bytes()
text = source.read_text(encoding='utf-8')
evidence = root / 'mutation-evidence'
evidence.mkdir(exist_ok=True)
fixture = root / 'test/native'
dependency = fixture / 'dep/std'
dependency.mkdir(parents=True, exist_ok=True)
results = []


def replace_once(body, before, after):
    if body.count(before) != 1:
        raise SystemExit('nonunique anchor: ' + before)
    return body.replace(before, after, 1)


oracle = '''
rec AuditMemoryInfo {
    base: ptr;
    allocation_base: ptr;
    allocation_protect: u32;
    partition: u16;
    region_size: usize;
    state: u32;
    protect: u32;
    kind: u32;
}
#[library("kernel32.dll")]
ext fun VirtualQuery(address: ptr, info: *AuditMemoryInfo, size: usize) usize;
var audit_components: [4]ptr;
var audit_component_count: usize = 0;
fun audit_component_record(address: ptr) {
    if (audit_component_count < 4) { audit_components[audit_component_count] = address; }
    audit_component_count = audit_component_count + 1;
}
fun audit_components_released(expected: usize) bool {
    if (audit_component_count != expected || expected > 4) { ret false; }
    var i: usize = 0;
    for (i < expected) {
        var info: AuditMemoryInfo;
        if (VirtualQuery(audit_components[i], ?info, $size_of(AuditMemoryInfo)) != 48) { ret false; }
        if (info.state != 0x10000) { ret false; }
        i = i + 1;
    }
    ret true;
}
'''
instrumented = replace_once(text,
    '    bytes[length] = 0;\n    ret R.ok[ComponentScratch, Error]',
    '    bytes[length] = 0;\n    audit_component_record(bytes::ptr);\n    ret R.ok[ComponentScratch, Error]')
instrumented += oracle
operations = [
    ('                val nested: R.Result[Root, Error] = root_open(base, rel);', 2, 40),
    ('                    val absent: R.Result[Root, Error] = root_open(base, rel);', 2, 41),
    ('                val nested: R.Result[usize, Error] = root_remove_tree(?root, rel);', 2, 42),
    ('                val removed: R.Result[usize, Error] = root_remove_tree(?root, leaf);', 1, 43),
]
for anchor, expected, code in operations:
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    instrumented = replace_once(instrumented, anchor,
        indent + 'audit_component_count = 0;\n' + anchor + '\n' + indent +
        f'if (!audit_components_released({expected})) {{ bad = {code}; }}')


def run(name, body, selected, expected, expected_exits):
    source.write_text(body, encoding='utf-8', newline='')
    shutil.copy2(root / 'mach.toml', dependency / 'mach.toml')
    shutil.copytree(root / 'src', dependency / 'src', dirs_exist_ok=True)
    command = [sys.argv[1], 'test', str(fixture), '--target', 'windows-x86_64', '--include-deps', '--filter', selected]
    process = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    log = process.stdout.decode('utf-8', errors='replace')
    (evidence / (name + '.log')).write_text(log, encoding='utf-8')
    counts = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', log)
    counts = list(map(int, counts[-1])) if counts else None
    exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', log, re.MULTILINE)
    valid = counts == expected and sorted(exits) == sorted(expected_exits)
    valid = valid and ((process.returncode == 0) == (expected[1] == 0))
    result = dict(name=name, counts=counts, exits=exits, compiler_exit=process.returncode, verified=valid)
    results.append(result)
    print(json.dumps(result), flush=True)
    (evidence / 'summary.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    return valid


both = 'full Unicode components'
opening = 'root_open: full Unicode components'
removal = 'root_remove_tree: full Unicode components'
release = '    os.deallocate(component.name::ptr, component.size);'
variants = [
    ('omit-native-release', replace_once(instrumented, release, ''), both, [1, 2, 3], ['40', '42']),
    ('omit-open-release', replace_once(instrumented,
        '        free_component(?component);\n        os.close(fd);',
        '        os.close(fd);'), opening, [0, 1, 1], ['40']),
    ('omit-failed-open-release', replace_once(instrumented,
        '        free_component(?component);\n        os.close(fd);',
        '        if (R.is_ok[i32, Error](next)) { free_component(?component); }\n        os.close(fd);'), opening, [0, 1, 1], ['41']),
    ('omit-intermediate-remove-release', replace_once(instrumented,
        '        free_component(?component);\n        if (held) { os.close(fd); }',
        '        if (held) { os.close(fd); }'), removal, [0, 1, 1], ['42']),
    ('omit-final-remove-release', replace_once(instrumented,
        '            free_component(?component);\n            if (held) { os.close(fd); }',
        '            if (held) { os.close(fd); }'), removal, [0, 1, 1], ['42']),
]
try:
    if not run('baseline-uninstrumented', text, both, [3, 0, 3], []):
        raise SystemExit('production baseline failed')
    if not run('uninstrumented-release-leak', replace_once(text, release, ''), both, [3, 0, 3], []):
        raise SystemExit('unexpected uninstrumented behavior')
    if not run('baseline-allocation-oracle', instrumented, both, [3, 0, 3], []):
        raise SystemExit('allocation oracle baseline failed')
    for args in variants:
        run(*args)
finally:
    source.write_bytes(pristine)
    subprocess.run(['git', 'diff', '--exit-code', '--', str(source.relative_to(root))], cwd=root, check=True)
if not all(result['verified'] for result in results):
    raise SystemExit('one or more ownership mutations lacks the exact runtime result')
