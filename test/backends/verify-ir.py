# secret IR contract: the native secret primitives exist, std.memory.secret
# wipes before it calls the native release, no integer pointer alias is
# materialized, and no test-only inspection enters production IR.
# every wipe goes through std.crypto.ct.zeroize. the kernel is a call while its
# #[oblivious] marker stands, and it may inline. a wipe is therefore either a
# call to the kernel or its asm body, the kernel's own asm node as ct.ir emits
# it, and the ordering is asserted on whichever form the caller holds. release
# may inline wipe_typed into release_typed, so the typed wipe is also that
# function's call.
from pathlib import Path
import re
import sys


class IR:
    def __init__(self, text):
        if not text.startswith('ir-debug stage='):
            raise ValueError('expected the current emitted IR format')
        self.text = text
        self.types = dict(re.findall(r'^    (!\d+) = (i8|i64|void|ptr)$', text, re.M))

    def raw_function(self, name):
        match = re.search(r'^  fn @"' + re.escape(name) + r'"\(.*?^  \}\s*$', self.text, re.M | re.S)
        if match is None:
            raise ValueError('missing function ' + name)
        return match.group(0)

    def function(self, name):
        return re.sub(r'^    unattached \{\n.*?^    \}\n', '', self.raw_function(name), flags=re.M | re.S)

    def call(self, line, result, target):
        match = re.search(r'\bcall (!\d+) ' + re.escape(target) + r'(?:\[| |$)', line)
        return match is not None and self.types.get(match.group(1)) == result

    def inlined(self, line, body):
        return re.match(r'\s*asm ;', line) is not None and asm_body(line) == body

    def zero_byte(self, line):
        match = re.search(r'\bstore[.]secret 0 \{kind=2 ty=(!\d+) ', line)
        return match is not None and self.types.get(match.group(1)) == 'i8'


def asm_body(line):
    match = re.search(r'asm=\{isa="[^"]*" body="((?:[^"\\]|\\.)*)"', line)
    return None if match is None else match.group(1)


def kernel_of(text):
    # the zeroize kernel's asm node and its body, as its own function emits them
    for line in IR(text).raw_function('std.crypto.ct.zeroize').splitlines():
        if re.match(r'\s*asm ;', line):
            return line, asm_body(line)
    raise ValueError('zeroize has no asm body')


def first(lines, predicate, label):
    for index, line in enumerate(lines):
        if predicate(line):
            return index
    raise ValueError('missing ' + label)


PORTABLE = 'std.memory.secret.'
ZEROIZE = '@"std.crypto.ct.zeroize"'
TYPED = '$backends.main.SecretRecord'


def verify(native_text, portable_text, main_text, kernel):
    native, portable, main = IR(native_text), IR(portable_text), IR(main_text)
    for name in ('allocate', 'release', 'random_fill', 'read_at', 'write_at'):
        native.function('std.system.os.secret.' + name)
    for name in (PORTABLE + 'allocate_typed', PORTABLE + 'deallocate_typed', PORTABLE + 'wipe_typed',
                 'std.system.os.allocate_secret_typed', 'std.system.os.release_secret_typed'):
        if name + TYPED not in main.text:
            raise ValueError('missing typed boundary ' + name)
    if re.search(r'\b(ptrtoint|inttoptr)\b', native.text + portable.text + main.text):
        raise ValueError('secret boundary materialized an integer pointer alias')
    fixtures = r'(scripted_fill|all_zero|reset_probe_fill|interrupted_fill|probe_release|probe_typed_release|is_ok|refused_as|failed_natively|count_is|count_refused|count_failed)'
    if re.search(re.escape(PORTABLE) + fixtures, portable.text):
        raise ValueError('test-only secret inspection entered production IR')
    body = portable.function(PORTABLE + 'release_all').splitlines()
    wipe = first(body, lambda line: portable.call(line, 'void', ZEROIZE) or portable.inlined(line, kernel), 'release wipe')
    release = first(body, lambda line: portable.call(line, 'i64', '%p3'), 'native release call')
    if wipe >= release:
        raise ValueError('native release precedes secret wipe')
    typed = main.function(PORTABLE + 'release_typed' + TYPED).splitlines()
    typed_release = first(typed, lambda line: main.call(line, 'i64', '%p3'), 'typed native release call')
    typed_wipe = first(typed, lambda line: main.call(line, 'void', '@"' + PORTABLE + 'wipe_typed' + TYPED + '"')
                       or main.call(line, 'void', ZEROIZE) or main.inlined(line, kernel), 'typed release wipe')
    if typed_wipe >= typed_release:
        raise ValueError('native typed release precedes full-layout wipe')
    return portable, body, wipe, release


def controls(native_text, portable_text, main_text, kernel_text):
    kernel_line, kernel = kernel_of(kernel_text)
    portable, body, wipe, release = verify(native_text, portable_text, main_text, kernel)
    original = portable.raw_function(PORTABLE + 'release_all')
    deleted = body[:wipe] + body[wipe + 1:]
    reordered = list(body)
    reordered[wipe], reordered[release] = reordered[release], reordered[wipe]
    foreign = kernel_line.replace(kernel, 'mov rax, 0')
    variants = {
        'deleted wipe': portable_text.replace(original, '\n'.join(deleted)),
        'release before wipe': portable_text.replace(original, '\n'.join(reordered)),
        'integer pointer alias': portable_text.replace(original, original.replace('\n', '\n      %999999 = ptrtoint !0 %p1\n', 1)),
        'foreign inlined body': portable_text.replace(original, original.replace(body[wipe], foreign, 1)),
    }
    for name, changed in variants.items():
        try:
            verify(native_text, changed, main_text, kernel)
        except ValueError:
            continue
        raise ValueError('IR oracle accepted control: ' + name)
    inlined = portable_text.replace(original, original.replace(body[wipe], kernel_line, 1))
    verify(native_text, inlined, main_text, kernel)
    print('OK: IR oracle accepts an inlined kernel, and rejects a deleted wipe, a reordered release, an integer pointer alias and a foreign kernel body')


if __name__ == '__main__':
    native_text, portable_text, main_text, kernel_text = (Path(name).read_text() for name in sys.argv[1:5])
    try:
        verify(native_text, portable_text, main_text, kernel_of(kernel_text)[1])
        controls(native_text, portable_text, main_text, kernel_text)
    except ValueError as error:
        raise SystemExit('FAIL: ' + str(error))
