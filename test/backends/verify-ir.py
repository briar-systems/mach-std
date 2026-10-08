# secret IR contract: the native secret primitives exist, std.memory.secret
# wipes before it calls the native release, no integer pointer alias is
# materialized, and no test-only inspection enters production IR.
#
# a wipe is a call to the zeroize kernel, the kernel's own asm node where it
# inlined, or, in release_typed, a call to wipe_typed. the order is proven on
# the control-flow graph built from each block's terminator: every path from
# the entry to a native release passes a wipe first, whatever the block layout.
# a wipe counts only when its pointer and length are the released region, read
# from the call's arguments or the asm node's binds and traced through the
# copies the IR emits (stack slots with one writer, and wipe_typed's byte view).
# a value the tracer cannot follow fails the check.
from pathlib import Path
import re
import sys


PORTABLE = 'std.memory.secret.'
ZEROIZE = '@"std.crypto.ct.zeroize"'
TYPED = '$backends.main.SecretRecord'
WIPE_TYPED = '@"' + PORTABLE + 'wipe_typed' + TYPED + '"'
# $size_of(SecretRecord): an 8192-aligned record of two u64 fields in src/main.mach
TYPED_SIZE = 8192
# the pointer copy wipe_typed takes its secret byte view through, per isa
VIEWS = {
    'x86_64': ('mov rax, {src}', 'mov {dst}, rax'),
    'aarch64': ('ldr x0, {src}', 'str x0, {dst}'),
    'riscv64': ('ld t0, {src}', 'sd t0, {dst}'),
}
TERMINATORS = ('br', 'cbr', 'ret', 'unreachable')


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
        return Function(self, name)


class Inst:
    def __init__(self, line, line_no):
        self.raw, self.line_no = line, line_no
        text = line.strip()
        self.dest = self.type = None
        self.asm = None
        if re.match(r'asm ;', text):
            self.op = 'asm'
            match = re.search(r'asm=\{isa="([^"]*)" body="((?:[^"\\]|\\.)*)" binds=\[(.*?)\]\}', text)
            if match is None:
                raise ValueError('unreadable asm node: ' + text[:120])
            binds = dict(re.findall(r'\{name="([^"]*)" instr=(%\w+)', match.group(3)))
            self.asm = (match.group(1), match.group(2), binds)
            self.operands, self.uses = [], list(binds.values())
            return
        head = re.sub(r' \{kind=[^}]*\}', '', text.split(' ; state{', 1)[0])
        match = re.match(r'(?:(%\w+) = )?(\S+)\s*(.*)$', head)
        self.dest, self.op, rest = match.groups()
        typed = re.match(r'(!\d+)\s*(.*)$', rest)
        if typed is not None:
            self.type, rest = typed.groups()
        self.operands = [part.split()[0] for part in rest.split(', ')] if rest else []
        self.uses = re.findall(r'%\w+', rest)

    def calls(self, callee):
        return self.op == 'call' and re.sub(r'\[fn=\d+\]$', '', self.operands[0]) == callee

    def args(self):
        return self.operands[1:]


class Function:
    def __init__(self, ir, name):
        self.ir, self.name = ir, name
        self.raw = ir.raw_function(name)
        self.lines = self.raw.split('\n')
        self.blocks, self.defs, self.users = {}, {}, {}
        self.entry, current = None, None
        for line_no, line in enumerate(self.lines):
            header = re.match(r'    block (bb\d+) \[', line)
            if header is not None:
                current = header.group(1)
                if current in self.blocks:
                    raise ValueError(name + ': block ' + current + ' is defined twice')
                self.blocks[current] = []
                self.entry = self.entry or current
            elif line.startswith('      ') and current is not None:
                inst = Inst(line, line_no)
                pos = (current, len(self.blocks[current]))
                self.blocks[current].append(inst)
                if inst.dest is not None:
                    if inst.dest in self.defs:
                        raise ValueError(name + ': ' + inst.dest + ' is defined twice')
                    self.defs[inst.dest] = pos
                for value in set(inst.uses):
                    self.users.setdefault(value, []).append(pos)
            elif not line.startswith('      '):
                current = None
        if self.entry is None:
            raise ValueError(name + ' has no blocks')
        for block, insts in self.blocks.items():
            if not insts or insts[-1].op not in TERMINATORS:
                raise ValueError(name + ': block ' + block + ' does not end in a known terminator')

    def at(self, pos):
        return self.blocks[pos[0]][pos[1]]

    def positions(self):
        for block, insts in self.blocks.items():
            for index in range(len(insts)):
                yield block, index

    def successors(self, block):
        last = self.blocks[block][-1]
        targets = {'br': last.operands[:1], 'cbr': last.operands[1:3]}.get(last.op, [])
        for target in targets:
            if target not in self.blocks:
                raise ValueError(self.name + ': ' + block + ' branches to unknown block ' + target)
        return targets

    def reaches(self, barriers, targets, start=None):
        # the first target a path from start (the entry) meets before any barrier, else None
        work, seen = [start or (self.entry, 0)], set()
        while work:
            block, first = work.pop()
            if first == 0:
                if block in seen:
                    continue
                seen.add(block)
            for index in range(first, len(self.blocks[block])):
                if (block, index) in barriers:
                    break
                if (block, index) in targets:
                    return block, index
            else:
                work.extend((successor, 0) for successor in self.successors(block))
        return None

    def dominates(self, a, b):
        return self.reaches({a}, {b}) is None


def asm_lines(body):
    return [line.strip() for line in body.replace('\\n', '\n').split('\n') if line.strip()]


def view_binds(asm):
    # (source bind, destination bind) when the node is a plain pointer copy
    isa, body, binds = asm
    template, lines = VIEWS.get(isa), asm_lines(body)
    if template is None or len(lines) != len(template):
        return None
    names = {}
    for pattern, line in zip(template, lines):
        regex = re.escape(pattern).replace(r'\{src\}', r'\{(?P<src>\w+)\}').replace(r'\{dst\}', r'\{(?P<dst>\w+)\}')
        match = re.fullmatch(regex, line)
        if match is None:
            return None
        for role, name in match.groupdict().items():
            if names.setdefault(role, name) != name:
                return None
    if set(names) != {'src', 'dst'} or names['src'] == names['dst'] or not set(names.values()) <= set(binds):
        return None
    return names['src'], names['dst']


def show(value):
    kind, *rest = value
    if kind == 'param':
        return '%p' + str(rest[0])
    if kind == 'const':
        return str(rest[0])
    return ' * '.join(show(part) for part in rest[0])


def product(a, b):
    return ('mul', tuple(sorted((a, b), key=repr)))


class Tracer:
    def __init__(self, kernel_text):
        zeroize = IR(kernel_text).function('std.crypto.ct.zeroize')
        nodes = [pos for pos in zeroize.positions() if zeroize.at(pos).op == 'asm']
        if len(nodes) != 1:
            raise ValueError('zeroize must hold exactly one asm node, found ' + str(len(nodes)))
        self.kernel = zeroize.at(nodes[0]).asm[1]
        self.kernel_fn = zeroize
        operands = {name: self.slot(zeroize, slot, nodes[0]) for name, slot in zeroize.at(nodes[0]).asm[2].items()}
        roles = {value: name for name, value in operands.items()}
        if set(roles) != {('param', 0), ('param', 1)}:
            raise ValueError('zeroize asm binds do not read its pointer and length parameters')
        self.kernel_binds = roles[('param', 0)], roles[('param', 1)]

    def is_kernel(self, inst):
        return inst.asm is not None and inst.asm[1] == self.kernel

    def value(self, fn, token, reader):
        match = re.fullmatch(r'%p(\d+)', token)
        if match is not None:
            return 'param', int(match.group(1))
        if re.fullmatch(r'-?\d+|null', token):
            return 'const', int(token) if token != 'null' else token
        if token not in fn.defs:
            raise ValueError(fn.name + ': cannot trace ' + token + ', it has no definition')
        inst = fn.at(fn.defs[token])
        if inst.op == 'load':
            return self.slot(fn, inst.operands[0], fn.defs[token])
        if inst.op == 'mul':
            return product(*(self.value(fn, operand, fn.defs[token]) for operand in inst.operands))
        raise ValueError(fn.name + ': cannot trace ' + token + ' through ' + inst.op)

    def slot(self, fn, slot, reader):
        # the one value a stack slot holds where it is read
        if slot not in fn.defs or fn.at(fn.defs[slot]).op != 'alloca':
            raise ValueError(fn.name + ': cannot trace a load from ' + slot + ', it is not a stack slot')
        writers = []
        for pos in fn.users.get(slot, []):
            inst = fn.at(pos)
            if inst.op in ('load', 'dbg_value') and inst.operands[0] == slot:
                continue
            if inst.op in ('store', 'store.secret') and inst.operands[1] == slot and inst.operands[0] != slot:
                writers.append((pos, lambda pos=pos, inst=inst: self.value(fn, inst.operands[0], pos)))
                continue
            if self.is_kernel(inst):
                continue
            view = inst.asm is not None and view_binds(inst.asm)
            if view and inst.asm[2][view[0]] == slot and inst.asm[2][view[1]] != slot:
                continue
            if view and inst.asm[2][view[1]] == slot:
                source = inst.asm[2][view[0]]
                writers.append((pos, lambda pos=pos, source=source: self.slot(fn, source, pos)))
                continue
            raise ValueError(fn.name + ': cannot trace ' + slot + ', ' + inst.op + ' in ' + pos[0] + ' may write it')
        # the writers whose store reaches the read, no other writer between
        kills = {pos for pos, _ in writers}
        if fn.reaches(kills, {reader}) is not None:
            raise ValueError(fn.name + ': cannot trace ' + slot + ', a path reads it before any write')
        reaching = [(pos, resolve) for pos, resolve in writers if fn.reaches(kills, {reader}, (pos[0], pos[1] + 1)) is not None]
        if len(reaching) != 1:
            raise ValueError(fn.name + ': cannot trace ' + slot + ', ' + str(len(reaching)) + ' writes reach the read')
        pos, resolve = reaching[0]
        return resolve()

    def wipe(self, fn, pos, typed):
        # (pointer, byte length) the instruction wipes, or None when it is not a wipe
        inst = fn.at(pos)
        void = inst.type is not None and fn.ir.types.get(inst.type) == 'void'
        if inst.calls(ZEROIZE) and void:
            pointer, length = inst.args()
            return self.value(fn, pointer, pos), self.value(fn, length, pos)
        if self.is_kernel(inst):
            binds = inst.asm[2]
            return tuple(self.slot(fn, binds[name], pos) for name in self.kernel_binds)
        if typed and inst.calls(WIPE_TYPED) and void:
            # the call wipes what wipe_typed's own body wipes before it returns
            wipe_typed = fn.ir.function(WIPE_TYPED[2:-1])
            rets = {pos for pos in wipe_typed.positions() if wipe_typed.at(pos).op == 'ret'}
            self.require(wipe_typed, rets, lambda site: (('param', 0), product(('const', TYPED_SIZE), ('param', 1))),
                         False, 'wipe_typed return')
            pointer, count = inst.args()
            return self.value(fn, pointer, pos), product(('const', TYPED_SIZE), self.value(fn, count, pos))
        return None

    def require(self, fn, sites, expected, typed, label):
        # every path from the entry to each site passes a wipe of the region the site expects
        if not sites:
            raise ValueError(fn.name + ': missing ' + label)
        wipes = {pos: region for pos in fn.positions() for region in [self.wipe(fn, pos, typed)] if region is not None}
        for site in sorted(sites):
            want = expected(site)
            barriers = {pos for pos, region in wipes.items() if region == want}
            if fn.reaches(barriers, {site}) is None:
                continue
            others = ', '.join(pos[0] + ' wipes ' + show(region[0]) + ' for ' + show(region[1]) + ' bytes'
                               for pos, region in sorted(wipes.items()) if region != want)
            raise ValueError(fn.name + ': ' + label + ' in ' + site[0] + ' is reachable without a wipe of ' + show(want[0])
                             + ' for ' + show(want[1]) + ' bytes' + (' (' + others + ')' if others else ''))
        return wipes


def releases(fn):
    # calls through the release_fn parameter, returning the native i64 status
    return {pos for pos in fn.positions() if fn.at(pos).calls('%p3') and fn.ir.types.get(fn.at(pos).type) == 'i64'}


def verify(native_text, portable_text, main_text, tracer):
    native, portable, main = IR(native_text), IR(portable_text), IR(main_text)
    for name in ('allocate', 'release', 'random_fill', 'read_at', 'write_at'):
        native.raw_function('std.system.os.secret.' + name)
    for name in (PORTABLE + 'allocate_typed', PORTABLE + 'deallocate_typed', PORTABLE + 'wipe_typed',
                 'std.system.os.allocate_secret_typed', 'std.system.os.release_secret_typed'):
        if name + TYPED not in main.text:
            raise ValueError('missing typed boundary ' + name)
    if re.search(r'\b(ptrtoint|inttoptr)\b', native.text + portable.text + main.text):
        raise ValueError('secret boundary materialized an integer pointer alias')
    fixtures = r'(scripted_fill|all_zero|reset_probe_fill|interrupted_fill|probe_release|probe_typed_release|is_ok|refused_as|failed_natively|count_is|count_refused|count_failed)'
    if re.search(re.escape(PORTABLE) + fixtures, portable.text):
        raise ValueError('test-only secret inspection entered production IR')
    release_all = portable.function(PORTABLE + 'release_all')
    released = lambda site: tuple(tracer.value(release_all, token, site) for token in release_all.at(site).args()[1:3])
    tracer.require(release_all, releases(release_all), released, False, 'native release call')
    release_typed = main.function(PORTABLE + 'release_typed' + TYPED)
    tracer.require(release_typed, releases(release_typed),
                   lambda site: (('param', 1), product(('const', TYPED_SIZE), ('param', 2))), True, 'typed native release call')
    return release_all, release_typed


def edit(fn, changes):
    # the module text with fn's raw lines replaced, line number -> replacement lines
    lines = []
    for line_no, line in enumerate(fn.lines):
        lines.extend(changes.get(line_no, [line]))
    return fn.ir.text.replace(fn.raw, '\n'.join(lines))


def with_args(inst, args):
    head, sep, state = inst.raw.partition(' ; state{')
    parts = head.split(', ')
    for index, arg in args.items():
        old = parts[index + 1].split()
        parts[index + 1] = ' '.join([arg] + old[1:])
    return ', '.join(parts) + sep + state


def inline_kernel(tracer, inst):
    # zeroize's body in place of a call to it, its values renamed and its parameters bound to the call's arguments
    if len(tracer.kernel_fn.blocks) != 1:
        raise ValueError('control: zeroize spans more than one block')
    args = inst.args()
    body = []
    for kernel_inst in tracer.kernel_fn.blocks[tracer.kernel_fn.entry][:-1]:
        line = re.sub(r'%(\d+)\b', lambda m: '%' + str(900000 + int(m.group(1))), kernel_inst.raw)
        body.append(re.sub(r'%p(\d+)\b', lambda m: args[int(m.group(1))], line))
    return body


def wipe_site(tracer, fn, typed):
    sites = [pos for pos in fn.positions() if tracer.wipe(fn, pos, typed) is not None]
    if len(sites) != 1:
        raise ValueError('control: ' + fn.name + ' holds ' + str(len(sites)) + ' wipes, expected one')
    return sites[0]


def with_binds(inst, roles):
    # the kernel asm node with the named binds reading fresh slots that hold the given values
    lines, raw = [], inst.raw
    for index, (name, value) in enumerate(roles.items()):
        slot = '%' + str(910000 + index)
        lines += ['      ' + slot + ' = alloca !0 1', '      store ' + value + ', ' + slot]
        raw, count = re.subn(r'(\{name="' + re.escape(name) + r'" instr=)%\w+', r'\g<1>' + slot, raw)
        if count != 1:
            raise ValueError('control: the kernel asm node has no ' + name + ' bind')
    return lines + [raw]


def operand_controls(tracer, fn, typed, label):
    # wrong pointer and short length, as the IR emits the wipe and with the kernel inlined in its place
    site = fn.at(wipe_site(tracer, fn, typed))
    pointer, length = tracer.kernel_binds
    if site.calls(WIPE_TYPED):
        callee = fn.ir.function(WIPE_TYPED[2:-1])
        yield from operand_controls(tracer, callee, False, label + ' (in wipe_typed)')
    if site.op == 'call':
        wrong, short = with_args(site, {0: 'null'}), with_args(site, {1: '1'})
        yield label + ': wipe of the wrong pointer', edit(fn, {site.line_no: [wrong]})
        yield label + ': wipe of a short length', edit(fn, {site.line_no: [short]})
    if site.calls(ZEROIZE):
        yield label + ': inlined wipe of the wrong pointer', edit(fn, {site.line_no: inline_kernel(tracer, Inst(wrong, 0))})
        yield label + ': inlined wipe of a short length', edit(fn, {site.line_no: inline_kernel(tracer, Inst(short, 0))})
    if tracer.is_kernel(site):
        yield label + ': inlined wipe of the wrong pointer', edit(fn, {site.line_no: with_binds(site, {pointer: 'null'})})
        yield label + ': inlined wipe of a short length', edit(fn, {site.line_no: with_binds(site, {length: '1'})})


def segments(fn):
    # each block's raw line span, header through terminator
    return {block: (insts[0].line_no - 1, insts[-1].line_no) for block, insts in fn.blocks.items()}


def bypass(tracer, fn, typed):
    # a branch arm that never reaches the wipe now leads to a release of its own
    wipe, release = wipe_site(tracer, fn, typed), min(releases(fn))
    for block, insts in fn.blocks.items():
        last = insts[-1]
        if last.op != 'cbr':
            continue
        avoids = [arm for arm in last.operands[1:3] if fn.reaches(set(), {wipe}, (arm, 0)) is None]
        if len(avoids) != 1:
            continue
        unwiped = fn.at(release).raw.replace(fn.at(release).dest + ' =', '%999999 =', 1)
        branch = re.sub(r'\b' + avoids[0] + r'\b', 'bb999999', last.raw, count=1)
        return edit(fn, {last.line_no: [branch, '    block bb999999 [preds=' + block + ']:', unwiped, '      ret']})
    raise ValueError('control: ' + fn.name + ' has no branch that avoids its wipe')


def reversed_layout(fn):
    # the same graph with every block after the entry laid out in reverse
    spans = segments(fn)
    entry, rest = spans[fn.entry], [span for block, span in spans.items() if block != fn.entry]
    first, last = min(start for start, _ in spans.values()), max(end for _, end in spans.values())
    order = [entry] + sorted(rest, reverse=True)
    lines = fn.lines[:first] + [line for start, end in order for line in fn.lines[start:end + 1]] + fn.lines[last + 1:]
    if sorted(lines) != sorted(fn.lines):
        raise ValueError('control: ' + fn.name + ' blocks are not contiguous')
    return fn.ir.text.replace(fn.raw, '\n'.join(lines))


def inlined(tracer, fn, typed):
    # the module with fn's zeroize call replaced by the kernel's body, or None when it holds no such call
    site = fn.at(wipe_site(tracer, fn, typed))
    if not site.calls(ZEROIZE):
        return None
    return edit(fn, {site.line_no: inline_kernel(tracer, site)})


def controls(native_text, portable_text, main_text, kernel_text):
    tracer = Tracer(kernel_text)
    release_all, release_typed = verify(native_text, portable_text, main_text, tracer)
    typed_host = release_typed
    if release_typed.at(wipe_site(tracer, release_typed, True)).calls(WIPE_TYPED):
        typed_host = release_typed.ir.function(WIPE_TYPED[2:-1])
    wipe, release = wipe_site(tracer, release_all, False), min(releases(release_all))
    wipe_line, release_line = release_all.at(wipe).raw, release_all.at(release).raw
    # where the IR already holds the kernel inline, the emitted form is the inlined one
    kernel_inlined = inlined(tracer, release_all, False)
    typed_inlined = inlined(tracer, typed_host, False)
    foreign = (kernel_inlined or portable_text).replace(tracer.kernel, 'mov rax, 0')
    rejected = {
        'deleted wipe': edit(release_all, {release_all.at(wipe).line_no: []}),
        'release before wipe': edit(release_all, {release_all.at(wipe).line_no: [release_line],
                                                  release_all.at(release).line_no: [wipe_line]}),
        'release on an unwiped path': bypass(tracer, release_all, False),
        'integer pointer alias': portable_text.replace(release_all.raw, release_all.raw.replace('\n', '\n      %999999 = ptrtoint !0 %p1\n', 1)),
        'foreign inlined body': foreign,
    }
    rejected_typed = {'typed release on an unwiped path': bypass(tracer, release_typed, True)}
    rejected.update(operand_controls(tracer, release_all, False, 'release_all'))
    rejected_typed.update(operand_controls(tracer, release_typed, True, 'release_typed'))
    accepted = {'reversed block layout': (reversed_layout(release_all), reversed_layout(release_typed))}
    if kernel_inlined is not None:
        accepted['inlined kernel'] = (kernel_inlined, main_text)
    if typed_inlined is not None:
        accepted['typed inlined kernel'] = (portable_text, typed_inlined)
    for name, (portable_changed, main_changed) in accepted.items():
        try:
            verify(native_text, portable_changed, main_changed, tracer)
        except ValueError as error:
            raise ValueError('IR oracle rejected control: ' + name + ': ' + str(error))
    cases = [(name, changed, main_text) for name, changed in rejected.items()]
    cases += [(name, portable_text, changed) for name, changed in rejected_typed.items()]
    for name, portable_changed, main_changed in cases:
        try:
            verify(native_text, portable_changed, main_changed, tracer)
        except ValueError as error:
            print('rejected ' + name + ': ' + str(error))
            continue
        raise ValueError('IR oracle accepted control: ' + name)
    print('OK: IR oracle accepts ' + ', '.join(accepted) + ', and rejects ' + str(len(cases)) + ' controls')


if __name__ == '__main__':
    native_text, portable_text, main_text, kernel_text = (Path(name).read_text() for name in sys.argv[1:5])
    try:
        controls(native_text, portable_text, main_text, kernel_text)
    except ValueError as error:
        raise SystemExit('FAIL: ' + str(error))
