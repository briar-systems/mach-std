# secret IR contract: the native secret primitives exist, std.memory.secret
# wipes before it calls the native release, no integer pointer alias is
# materialized, and no test-only inspection enters production IR.
# every wipe goes through std.crypto.ct.zeroize, which is never inlined, so
# release_all holds a call to it in both profiles and the ordering is asserted
# on that call. release inlines wipe_typed into release_typed, leaving only its
# own zeroize call, so the typed wipe is either call.
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

    def zero_byte(self, line):
        match = re.search(r'\bstore[.]secret 0 \{kind=2 ty=(!\d+) ', line)
        return match is not None and self.types.get(match.group(1)) == 'i8'


def first(lines, predicate, label):
    for index, line in enumerate(lines):
        if predicate(line):
            return index
    raise ValueError('missing ' + label)


PORTABLE = 'std.memory.secret.'
ZEROIZE = '@"std.crypto.ct.zeroize"'
TYPED = '$backends.main.SecretRecord'


def verify(native_text, portable_text, main_text):
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
    wipe = first(body, lambda line: portable.call(line, 'void', ZEROIZE), 'release wipe')
    release = first(body, lambda line: portable.call(line, 'i64', '%p3'), 'native release call')
    if wipe >= release:
        raise ValueError('native release precedes secret wipe')
    typed = main.function(PORTABLE + 'release_typed' + TYPED).splitlines()
    typed_release = first(typed, lambda line: main.call(line, 'i64', '%p3'), 'typed native release call')
    typed_wipe = first(typed, lambda line: main.call(line, 'void', '@"' + PORTABLE + 'wipe_typed' + TYPED + '"')
                       or main.call(line, 'void', ZEROIZE), 'typed release wipe')
    if typed_wipe >= typed_release:
        raise ValueError('native typed release precedes full-layout wipe')
    return portable, body, wipe, release


def controls(native_text, portable_text, main_text):
    portable, body, wipe, release = verify(native_text, portable_text, main_text)
    original = portable.raw_function(PORTABLE + 'release_all')
    deleted = body[:wipe] + body[wipe + 1:]
    reordered = list(body)
    reordered[wipe], reordered[release] = reordered[release], reordered[wipe]
    variants = {
        'deleted wipe': portable_text.replace(original, '\n'.join(deleted)),
        'release before wipe': portable_text.replace(original, '\n'.join(reordered)),
        'integer pointer alias': portable_text.replace(original, original.replace('\n', '\n      %999999 = ptrtoint !0 %p1\n', 1)),
    }
    for name, changed in variants.items():
        try:
            verify(native_text, changed, main_text)
        except ValueError:
            continue
        raise ValueError('IR oracle accepted control: ' + name)
    print('OK: IR oracle rejects deleted wipe, reordered release, and integer pointer alias')


if __name__ == '__main__':
    native_text, portable_text, main_text = (Path(name).read_text() for name in sys.argv[1:4])
    try:
        verify(native_text, portable_text, main_text)
        controls(native_text, portable_text, main_text)
    except ValueError as error:
        raise SystemExit('FAIL: ' + str(error))
