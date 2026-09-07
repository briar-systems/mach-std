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


def verify(secret_text, main_text, profile):
    secret, main = IR(secret_text), IR(main_text)
    for name in ('allocate', 'deallocate', 'random_fill'):
        secret.function('std.system.os.secret.' + name)
    for name in ('std.system.os.secret_allocate_typed', 'std.system.os.secret_deallocate_typed',
                 'std.system.os.secret.wipe_typed'):
        if name + '$backends.main.SecretRecord' not in main.text:
            raise ValueError('missing typed boundary ' + name)
    if re.search(r'\b(ptrtoint|inttoptr)\b', secret.text + main.text):
        raise ValueError('secret boundary materialized an integer pointer alias')
    if re.search(r'std[.]system[.]os[.]secret[.](scripted_fill|all_zero|reset_probe_fill|interrupted_fill|probe_release|probe_typed_release)', secret.text):
        raise ValueError('test-only secret inspection entered production IR')
    body = secret.function('std.system.os.secret.release_all').splitlines()
    wipe = first(body, secret.zero_byte if profile == 'release' else
                 lambda line: secret.call(line, 'void', '@"std.system.os.secret.wipe"'), 'release wipe')
    release = first(body, lambda line: secret.call(line, 'i64', '%p3'), 'native release call')
    if wipe >= release:
        raise ValueError('native release precedes secret wipe')
    typed = main.function('std.system.os.secret.release_typed$backends.main.SecretRecord').splitlines()
    typed_release = first(typed, lambda line: main.call(line, 'i64', '%p3'), 'typed native release call')
    if profile != 'release':
        typed_wipe = first(typed, lambda line: main.call(line, 'void', '@"std.system.os.secret.wipe_typed$backends.main.SecretRecord"'), 'typed release wipe')
        if typed_wipe >= typed_release:
            raise ValueError('native typed release precedes full-layout wipe')
    return secret, body, wipe, release


def controls(secret_text, main_text, profile):
    secret, body, wipe, release = verify(secret_text, main_text, profile)
    original = secret.raw_function('std.system.os.secret.release_all')
    deleted = body[:wipe] + body[wipe + 1:]
    reordered = list(body)
    reordered[wipe], reordered[release] = reordered[release], reordered[wipe]
    variants = {
        'deleted wipe': (secret_text.replace(original, '\n'.join(deleted)), main_text),
        'release before wipe': (secret_text.replace(original, '\n'.join(reordered)), main_text),
        'integer pointer alias': (secret_text.replace(original, original.replace('\n', '\n      %999999 = ptrtoint !0 %p1\n', 1)), main_text),
    }
    for name, (changed_secret, changed_main) in variants.items():
        try:
            verify(changed_secret, changed_main, profile)
        except ValueError:
            continue
        raise ValueError('IR oracle accepted control: ' + name)
    print('OK: IR oracle rejects deleted wipe, reordered release, and integer pointer alias')


if __name__ == '__main__':
    secret_text, main_text = (Path(name).read_text() for name in sys.argv[1:3])
    profile = sys.argv[3]
    try:
        verify(secret_text, main_text, profile)
        controls(secret_text, main_text, profile)
    except ValueError as error:
        raise SystemExit('FAIL: ' + str(error))
