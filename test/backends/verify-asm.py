# secret assembly contract: in the final release assembly of every target, every
# path from the entry of deallocate and of release_typed to the native release
# passes a wipe whose pointer and length are the released region.
#
# a wipe is an out-of-line call to the zeroize kernel. the check requires it to
# stay a call in release builds, which #[oblivious] holds today, and reads its
# operands from the abi's argument registers at the call. it does not read an
# inlined kernel: if zeroize ever inlines, the release is reachable without a
# wipe and the failure says so.
#
# the release is identified by what it calls: the os's native release (the
# linux munmap syscall by its number, darwin free, windows VirtualFree), or, in
# release_typed, a call through its release_fn parameter. order is proven on the
# control-flow graph built from the assembly's labels and branches, never on
# text position. operands are traced forward through registers and stack slots
# with a dataflow pass over that graph: a value is an entry parameter, a
# constant, or the entry stack pointer, scaled and offset. anything the pass
# cannot read (an unknown instruction, an indirect call through an untraced
# value, a syscall with an untraced number) fails the check.
#
# stack slots are tracked by their offset from the entry stack pointer. a store
# through a pointer the pass cannot place, and every call, clobbers each slot at
# or above the lowest frame address that escaped (stored to memory, passed in an
# argument register or as the hidden result pointer, or fed to an operation the
# pass does not model), the caller's memory above the entry stack pointer, and
# the call's outgoing area. that area is [sp, sp + n) at the call, whatever
# register wrote it, where n is where the abi places the end of the callee's
# stack arguments, its home area included. the placement is the abi's
# classification of the callee's signature under the platform C convention, as
# the compiler classifies it: which registers each argument takes, which
# aggregates are copied onto the stack, split across registers and the stack,
# or passed by hidden reference, and whether an aggregate result takes a hidden
# result pointer that shifts the arguments. the signature comes from a std
# function's header in the module IR, the release_fn type for the indirect
# release, or the native release's entry below, and aggregate layouts from the
# module IR's types. a call whose signature the pass cannot get or place fails,
# and so does one passing or returning a tag or a vector, whose layout the IR
# does not fully state.
from pathlib import Path
import importlib.util
import re
import sys
import tomllib


def ir_contract():
    # the typed fixture's facts have one owner, the IR check beside this file
    spec = importlib.util.spec_from_file_location('verify_ir', Path(__file__).with_name('verify-ir.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


IR = ir_contract()
ZEROIZE = 'std.crypto.ct.zeroize'
NOWHERE = float('-inf')


class Rejected(Exception):
    # reason is order, region or unreadable
    def __init__(self, reason, message):
        super().__init__(message)
        self.reason = reason


def unreadable(message):
    return Rejected('unreadable', message)


class Unplaceable(Exception):
    # a type the classification cannot place, and why
    pass


def round_up(value, align):
    return value if align <= 1 else -(-value // align) * align


class Node:
    def __init__(self, kind, bits=0, half=False, count=0, members=(), align=0, packed=False):
        self.kind, self.bits, self.half, self.count = kind, bits, half, count
        self.members, self.align, self.packed = list(members), align, packed


class Types:
    # the module IR's types laid out as the compiler lays them out on a 64-bit target. a tag, a vector and
    # a recursive reference have none: the IR states neither a tag's discriminator width nor vector widths
    def __init__(self, table):
        self.table = table

    def node(self, t):
        text = t
        if re.fullmatch(r'!\d+', t):
            if t not in self.table:
                raise Unplaceable('type ' + t + ' is not in the module IR')
            text = self.table[t]
        if text == 'void':
            return Node('void')
        match = re.fullmatch(r'i(\d+)(~f16)?', text)
        if match:
            return Node('int', int(match.group(1)), half=bool(match.group(2)))
        match = re.fullmatch(r'f(\d+)', text)
        if match:
            return Node('float', int(match.group(1)))
        if text == 'ptr' or re.match(r'(ptr |fn\(|handle<)', text):
            return Node('ptr')
        match = re.fullmatch(r'\[(\d+)\](!\d+)', text)
        if match:
            return Node('array', count=int(match.group(1)), members=[match.group(2)])
        match = re.fullmatch(r'(uni)?\{(.*)\}\[align=(\d+) packed=(true|false)\]', text)
        if match:
            return Node('union' if match.group(1) else 'struct', members=re.findall(r'!\d+', match.group(2)),
                        align=int(match.group(3)), packed=match.group(4) == 'true')
        if text.startswith('tag{'):
            raise Unplaceable('the IR does not state the discriminator width of ' + text)
        if re.fullmatch(r'!\d+x\d+', text):
            raise Unplaceable('the IR does not state the vector register widths that lay out ' + text)
        raise Unplaceable('no layout for ' + text)

    def extent(self, t):
        # (size, alignment)
        n = self.node(t)
        if n.kind == 'void':
            return 0, 1
        if n.kind in ('int', 'float'):
            size = (n.bits + 7) // 8
            return size, size
        if n.kind == 'ptr':
            return 8, 8
        if n.kind == 'array':
            size, align = self.extent(n.members[0])
            return size * n.count, align
        align, offset, widest = 1, 0, 0
        for member in n.members:
            size, a = self.extent(member)
            if not n.packed:
                align = max(align, a)
                offset = offset if n.kind == 'union' else round_up(offset, a)
            widest, offset = max(widest, size), offset + size
        align = max(align, n.align)
        return round_up(widest if n.kind == 'union' else offset, align), align

    def fields(self, t):
        # (type, offset) of each member of a struct or union
        n, offset, out = self.node(t), 0, []
        for member in n.members:
            size, align = self.extent(member)
            if n.kind == 'struct' and not n.packed:
                offset = round_up(offset, align)
            out.append((member, offset if n.kind == 'struct' else 0))
            offset += size
        return out

    def natural_align(self, t):
        # the alignment an aggregate's members give it, before its own declared alignment
        n = self.node(t)
        if n.kind not in ('struct', 'union'):
            return self.extent(t)[1]
        if n.packed:
            return 1
        return max([1] + [self.extent(m)[1] for m in n.members])

    def aggregate(self, t):
        return self.node(t).kind in ('struct', 'union', 'array')

    def floating(self, t, abi):
        # a type the convention places as a float, a binary16 among them where its half rule says so
        n = self.node(t)
        return n.kind == 'float' or (n.kind == 'int' and n.half and abi['half'])

    def unaligned(self, t, base=0):
        # the System V rule: a member at an offset its own alignment does not divide makes the aggregate MEMORY
        n = self.node(t)
        if n.kind in ('struct', 'union'):
            return any((base + off) % self.extent(m)[1] != 0 or self.unaligned(m, base + off)
                       for m, off in self.fields(t))
        if n.kind == 'array':
            size = self.extent(n.members[0])[0]
            return any(self.unaligned(n.members[0], base + i * size) for i in range(n.count))
        return False

    def eightbytes(self, t, abi, base, classes):
        # merges each scalar's class into the two eightbytes it covers: 1 sse, 2 integer, 0 neither
        n = self.node(t)
        if n.kind in ('struct', 'union'):
            for member, off in self.fields(t):
                self.eightbytes(member, abi, base + off, classes)
            return
        if n.kind == 'array':
            size = self.extent(n.members[0])[0]
            for i in range(n.count if size else 0):
                self.eightbytes(n.members[0], abi, base + i * size, classes)
            return
        size = self.extent(t)[0]
        for i in range(base // 8, (base + size - 1) // 8 + 1 if size else base // 8):
            if i < 2:
                classes[i] = max(classes[i], 1 if self.floating(t, abi) else 2)

    def homogeneous(self, t, abi):
        # (element size, member count) of an aggregate of one float type, or None
        n = self.node(t)
        if self.floating(t, abi):
            return self.extent(t)[0], 1
        if n.kind == 'array':
            inner = self.homogeneous(n.members[0], abi)
            return None if inner is None else (inner[0], inner[1] * n.count)
        if n.kind not in ('struct', 'union'):
            return None
        elem, total = 0, 0
        for member in n.members:
            inner = self.homogeneous(member, abi)
            if inner is None or (elem and inner[0] != elem):
                return None
            elem = elem or inner[0]
            total = total + inner[1] if n.kind == 'struct' else max(total, inner[1])
        return (elem, total) if (total if n.kind == 'struct' else elem) else None

    def leaves(self, t, abi, base=0, cap=2):
        # (is float, offset, width) of each scalar of an aggregate flattened field by field, or None past cap
        n = self.node(t)
        if n.kind == 'union':
            return None
        if n.kind in ('struct', 'array'):
            out = []
            parts = self.fields(t) if n.kind == 'struct' else \
                [(n.members[0], i * self.extent(n.members[0])[0]) for i in range(n.count)]
            for member, off in parts:
                inner = self.leaves(member, abi, base + off, cap)
                if inner is None or len(out) + len(inner) > cap:
                    return None
                out += inner
            return out
        return [(self.floating(t, abi), base, self.extent(t)[0])]


class Arg:
    # what a convention reads of one parameter or result type
    def __init__(self, types, t, abi):
        self.size, own = types.extent(t)
        self.aggregate = types.aggregate(t)
        self.float = types.floating(t, abi)
        self.align = types.natural_align(t) if self.aggregate and abi.get('agg_natural_align') else own
        self.memory = self.aggregate and self.size > 0 and (self.size > 16 or types.unaligned(t))
        classes = [0, 0]
        if self.aggregate and 0 < self.size <= 16:
            types.eightbytes(t, abi, 0, classes)
        self.sse = [c == 1 for c in classes]
        self.used = [classes[0] != 0, self.size <= 8 or classes[1] != 0]
        same = types.homogeneous(t, abi) if self.aggregate else None
        self.hfa = same if same and 1 <= same[1] <= 4 and same[0] in (2, 4, 8) else (0, 0)
        found = types.leaves(t, abi) if self.aggregate else None
        self.leaves = found if found and len(found) in (1, 2) else []


class Slot:
    # a placement: reg (perhaps with stack words), stack, byref, stack_byref or sret, the ('gp', i),
    # ('fp', i) and ('stack', width) pieces it rides, and what it takes from each register bank
    def __init__(self, kind, pieces=(), size=0, gp=None, fp=None, stack_align=0):
        self.kind, self.pieces, self.size, self.stack_align = kind, list(pieces), size, stack_align
        self.gp = sum(p[0] == 'gp' for p in self.pieces) if gp is None else gp
        self.fp = sum(p[0] == 'fp' for p in self.pieces) if fp is None else fp
        self.offset = None


def in_gp(a, gp, count):
    return Slot('reg', [('gp', gp)], a.size) if gp < count else Slot('stack', size=a.size)


def sysv_param(abi, a, gp, fp):
    count, fps = len(abi['args']), abi['fp_args']
    if a.aggregate and a.size == 0:
        return Slot('reg')
    if a.memory:
        return Slot('stack', size=a.size)
    if a.aggregate and a.size <= 8:
        if a.sse[0]:
            return Slot('reg', [('fp', fp)], a.size) if fp < fps else Slot('stack', size=a.size)
        return in_gp(a, gp, count)
    if a.aggregate:
        banks = [('fp' if a.sse[i] else 'gp') for i in (0, 1) if a.used[i]] or ['gp']
        if gp + banks.count('gp') > count or fp + banks.count('fp') > fps:
            return Slot('stack', size=a.size)
        pieces, at = [], {'gp': gp, 'fp': fp}
        for bank in banks:
            pieces.append((bank, at[bank]))
            at[bank] += 1
        return Slot('reg', pieces, a.size)
    if a.float:
        return Slot('reg', [('fp', fp)], a.size) if fp < fps else Slot('stack', size=a.size)
    if a.size == 16:
        return Slot('reg', [('gp', gp), ('gp', gp + 1)], 16) if gp + 2 <= count else Slot('stack', size=16)
    return in_gp(a, gp, count)


def sysv_result(abi, a):
    return Slot('sret') if a.memory else Slot('reg')


def win64_param(abi, a, gp, fp):
    # every argument owns the positional slot of its index, whatever the other bank holds
    slot, count = gp + fp, len(abi['args'])
    by_value = a.size in (1, 2, 4, 8)
    if (a.aggregate and not by_value) or (not a.aggregate and not a.float and a.size == 16):
        return Slot('byref', [('gp', slot)], 8) if slot < count else Slot('stack_byref', size=8)
    if a.float and not a.aggregate:
        return Slot('reg', [('fp', slot)], a.size) if slot < count else Slot('stack', size=a.size)
    return in_gp(a, slot, count)


def win64_result(abi, a):
    return Slot('sret') if a.aggregate and a.size not in (0, 1, 2, 4, 8) else Slot('reg')


def aapcs64_pair(a, gp, count):
    # C.10 and C.12 round a 16-byte aligned pair up to an even register, and C.13 hands the rest of the
    # bank to nothing once it goes to the stack
    first = gp + 1 if a.align >= 16 and gp % 2 else gp
    if first + 2 <= count:
        return Slot('reg', [('gp', first), ('gp', first + 1)], a.size, gp=first + 2 - gp)
    return Slot('stack', size=a.size, gp=max(0, count - gp))


def aapcs64_param(abi, a, gp, fp):
    count, fps = len(abi['args']), abi['fp_args']
    if a.aggregate and a.size == 0:
        return Slot('reg')
    if a.aggregate and a.hfa[1]:
        # C.3: an hfa that does not fit the vector registers left takes the rest of them with it
        if fp + a.hfa[1] <= fps:
            return Slot('reg', [('fp', fp + i) for i in range(a.hfa[1])], a.size)
        return Slot('stack', size=a.size, fp=max(0, fps - fp))
    if a.aggregate and a.size > 16:
        return Slot('byref', [('gp', gp)], 8) if gp < count else Slot('stack_byref', size=8)
    if a.aggregate and a.size > 8:
        return aapcs64_pair(a, gp, count)
    if a.aggregate:
        return in_gp(a, gp, count)
    if a.float:
        return Slot('reg', [('fp', fp)], a.size) if fp < fps else Slot('stack', size=a.size)
    if a.size == 16:
        return aapcs64_pair(a, gp, count)
    return in_gp(a, gp, count)


def aapcs64_result(abi, a):
    return Slot('sret') if a.aggregate and not a.hfa[1] and a.size > 16 else Slot('reg')


def riscv_words(a, gp, count):
    # two xlen words in a register pair, split across the last register and the stack, or on the stack
    if gp + 2 <= count:
        return Slot('reg', [('gp', gp), ('gp', gp + 1)], a.size)
    if gp + 1 == count:
        return Slot('reg', [('gp', gp), ('stack', 8)], a.size)
    return Slot('stack', size=a.size)


def riscv_param(abi, a, gp, fp):
    count, fps, flen = len(abi['args']), abi['fp_args'], abi['flen']
    in_fp = lambda width: flen and width * 8 <= flen
    if a.aggregate and a.size > 16:
        return Slot('byref', [('gp', gp)], 8) if gp < count else Slot('stack_byref', size=8)
    if a.aggregate and a.hfa[1] in (1, 2) and in_fp(a.hfa[0]) and fp + a.hfa[1] <= fps:
        return Slot('reg', [('fp', fp + i) for i in range(a.hfa[1])], a.size)
    if a.aggregate and len(a.leaves) == 2 and all(in_fp(w) for f, _, w in a.leaves if f):
        floats = sum(f for f, _, _ in a.leaves)
        if floats == 2 and fp + 2 <= fps:
            return Slot('reg', [('fp', fp), ('fp', fp + 1)], a.size)
        if floats == 1 and fp < fps and gp < count:
            return Slot('reg', [('fp', fp), ('gp', gp)], a.size)
    if a.float and not a.aggregate and in_fp(a.size) and fp < fps:
        return Slot('reg', [('fp', fp)], a.size)
    if a.size > 8:
        return riscv_words(a, gp, count)
    return in_gp(a, gp, count)


def riscv_result(abi, a):
    return Slot('sret') if a.aggregate and a.size > 16 else Slot('reg')


class Convention:
    # a call's placement under the abi: each parameter's slot, the result's, the bytes above the call's
    # stack pointer the callee owns, and the register carrying the hidden result pointer, if any
    def __init__(self, abi, params, result, outgoing):
        self.params, self.result, self.outgoing = params, result, outgoing
        self.sret = None
        if result.kind == 'sret':
            self.sret = abi['args'][0] if abi['sret'] == 'shift' else abi['sret']

    def register(self, abi, index):
        # the one argument register that carries parameter index, or None
        slot = self.params[index] if index < len(self.params) else None
        if slot is None or slot.kind != 'reg' or len(slot.pieces) != 1 or slot.pieces[0][0] != 'gp':
            return None
        return abi['args'][slot.pieces[0][1]]


def convention(abi, types, params, result):
    # the abi's placement of a signature, as the compiler classifies one under the platform C convention
    def arg(t, what):
        try:
            return Arg(types, t, abi)
        except Unplaceable as error:
            raise Unplaceable(what + ' ' + t + ': ' + str(error))
    ret = abi['result'](abi, arg(result, 'the result'))
    gp, fp, stack, slots = 1 if ret.kind == 'sret' and abi['sret'] == 'shift' else 0, 0, abi['home'], []
    for index, t in enumerate(params):
        a = arg(t, 'argument ' + str(index))
        placed = a.align
        if abi.get('reg_align'):
            a.align = min(a.align, abi['reg_align'])
        slot = abi['param'](abi, a, gp, fp)
        if slot.kind in ('stack', 'stack_byref'):
            # where fixed arguments pack, a scalar or hfa takes its natural size and alignment
            natural = abi.get('natural_stack') and not (a.aggregate and not a.hfa[1])
            align = 8 if slot.kind == 'stack_byref' else max(placed, slot.stack_align, 1 if natural else 8)
            slot.offset = stack = round_up(stack, align)
            stack += slot.size if natural else round_up(slot.size or 8, 8)
        elif any(p[0] == 'stack' for p in slot.pieces):
            slot.offset = stack = round_up(stack, 8)
            stack += sum(round_up(p[1] or 8, 8) for p in slot.pieces if p[0] == 'stack')
        gp, fp = gp + slot.gp, fp + slot.fp
        slots.append(slot)
    return Convention(abi, slots, ret, stack)


# per abi: integer argument registers, where the hidden result pointer goes
# ('shift' takes the first argument register), the entry stack offset of the
# first stack argument, the home area a callee owns above the call's stack
# pointer, below its stack arguments, the registers a call preserves, the frame
# pointer, and its classification under the platform C convention: the float
# argument registers, whether a binary16 is placed as a float, how a parameter
# and a result are placed, and what an os changes of it. agg_natural_align
# places an aggregate by the alignment its members give it, reg_align caps the
# alignment a register assignment honors, and natural_stack packs fixed stack
# arguments at their natural size and alignment
ABIS = {
    'sysv64': dict(args=['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9'], sret='shift', stack=8, home=0,
                   saved={'rbx', 'rbp', 'rsp', 'r12', 'r13', 'r14', 'r15'}, sp='rsp', fp='rbp',
                   fp_args=8, half=True, param=sysv_param, result=sysv_result),
    'win64': dict(args=['rcx', 'rdx', 'r8', 'r9'], sret='shift', stack=40, home=32,
                  saved={'rbx', 'rbp', 'rdi', 'rsi', 'rsp', 'r12', 'r13', 'r14', 'r15'}, sp='rsp', fp='rbp',
                  fp_args=4, half=True, param=win64_param, result=win64_result),
    'aapcs64': dict(args=['x' + str(n) for n in range(8)], sret='x8', stack=0, home=0,
                    saved={'x' + str(n) for n in range(19, 30)} | {'sp'}, sp='sp', fp='x29',
                    fp_args=8, half=True, param=aapcs64_param, result=aapcs64_result, agg_natural_align=True,
                    os={'darwin': dict(agg_natural_align=False, reg_align=8, natural_stack=True)}),
    'lp64': dict(args=['a' + str(n) for n in range(8)], sret='shift', stack=0, home=0,
                 saved={'s' + str(n) for n in range(12)} | {'sp'}, sp='sp', fp='s0',
                 fp_args=8, flen=0, half=True, param=riscv_param, result=riscv_result),
}

# per isa: the linux syscall's number register, argument registers and clobbers,
# and munmap's number
SYSCALLS = {
    'x86_64': dict(number='rax', args=['rdi', 'rsi', 'rdx', 'r10', 'r8', 'r9'], clobbers={'rax', 'rcx', 'r11'}, munmap=11),
    'aarch64': dict(number='x8', args=['x0', 'x1', 'x2', 'x3', 'x4', 'x5'], clobbers={'x0'}, munmap=215),
    'riscv64': dict(number='a7', args=['a0', 'a1', 'a2', 'a3', 'a4', 'a5'], clobbers={'a0', 'a1'}, munmap=215),
}

# per os: the native release, what it calls, its signature and which arguments
# carry the region
NATIVE = {
    'linux': dict(syscall=True, params=['ptr', 'i64'], result='i64', pointer=0, length=1),
    'darwin': dict(symbol='_free', params=['ptr'], result='void', pointer=0, length=None),
    'windows': dict(symbol='VirtualFree', params=['ptr', 'i64', 'i32'], result='i32', pointer=0, length=None),
}


# a value: base None (a constant), ('param', i) or 'sp' (the entry stack
# pointer), times scale, plus offset. an untraced value is None
def const(n):
    return (None, 0, n)


def param(i):
    return (('param', i), 1, 0)


def is_frame(v):
    return v is not None and v[0] == 'sp'


def add(a, b):
    if a is None or b is None:
        return None
    if b[0] is None:
        return (a[0], a[1], a[2] + b[2])
    if a[0] is None:
        return (b[0], b[1], a[2] + b[2])
    return None


def sub(a, b):
    if a is None or b is None:
        return None
    if b[0] is None:
        return (a[0], a[1], a[2] - b[2])
    if a[0] == b[0] and a[1] == b[1]:
        return const(a[2] - b[2])
    return None


def mul(a, b):
    if a is None or b is None:
        return None
    if a[0] is not None:
        a, b = b, a
    if a[0] is not None or b[0] == 'sp':
        return None
    return (b[0], b[1] * a[2], b[2] * a[2])


def show(v):
    if v is None:
        return 'an untraced value'
    base, scale, offset = v
    if base is None:
        return str(offset)
    name = '%p' + str(base[1]) if base != 'sp' else 'the frame'
    text = (str(scale) + ' * ' if scale != 1 else '') + name
    return text + (' + ' + str(offset) if offset > 0 else ' - ' + str(-offset) if offset < 0 else '')


class State:
    def __init__(self, regs, mem, floor):
        self.regs, self.mem, self.floor = regs, mem, floor

    def copy(self):
        return State(dict(self.regs), dict(self.mem), self.floor)

    def __eq__(self, other):
        return (self.regs, self.mem, self.floor) == (other.regs, other.mem, other.floor)

    def join(self, other):
        regs = {r: v for r, v in self.regs.items() if other.regs.get(r) == v}
        mem = {o: v for o, v in self.mem.items() if other.mem.get(o) == v}
        return State(regs, mem, min(self.floor, other.floor))

    def get(self, reg):
        return self.regs.get(reg)

    def derive(self, value, *inputs):
        # a frame address that becomes an untraced value escapes the pass
        if value is None and any(is_frame(v) for v in inputs):
            self.floor = NOWHERE
        return value

    def set(self, reg, value, *inputs):
        if self.derive(value, *inputs) is None:
            self.regs.pop(reg, None)
        else:
            self.regs[reg] = value

    def escape(self, value):
        if is_frame(value):
            self.floor = min(self.floor, value[2])

    def clobber(self, floor):
        self.mem = {o: v for o, v in self.mem.items() if o < floor}

    def forget(self, low, width):
        # slots are 8 bytes wide, so only those starting within 7 bytes below can overlap
        for o in range(low - 7, low + width):
            self.mem.pop(o, None)

    def load(self, addr, width):
        if not is_frame(addr) or addr[1] != 1 or width != 8:
            return None
        return self.mem.get(addr[2])

    def store(self, addr, width, value):
        self.escape(value)
        if is_frame(addr) and addr[1] == 1:
            self.forget(addr[2], width)
            if width == 8 and value is not None:
                self.mem[addr[2]] = value
        else:
            self.clobber(min(self.floor, 0))

    def call(self, abi, args, clobbers, outgoing):
        # the callee reads its argument registers, may write through any escaped address,
        # and owns the outgoing bytes above the stack pointer
        for reg in args:
            self.escape(self.regs.get(reg))
        self.clobber(min(self.floor, 0))
        sp = self.regs.get(abi['sp'])
        if not is_frame(sp):
            raise unreadable('the stack pointer is untraced at a call')
        # an over-sized area only makes the check stricter: forgetting a slot never counts as wiping it
        if outgoing:
            self.forget(sp[2], outgoing)
        self.regs = {reg: v for reg, v in self.regs.items() if not clobbers(reg)}


class Inst:
    # kind: op, branch, jump, call, tail, ret or syscall
    def __init__(self, text, line, kind, apply=None, label=None, callee=None, through=None):
        self.text, self.line, self.kind = text, line, kind
        self.apply, self.label, self.callee, self.through = apply, label, callee, through
        self.after = None


def split_operands(text):
    parts, depth, current = [], 0, ''
    for ch in text:
        if ch in '[(':
            depth += 1
        elif ch in '])':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(current.strip())
            current = ''
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())
    return parts


def number(text):
    try:
        return int(text, 0)
    except ValueError:
        return None


X86_NAMES = {}
for full, names in {
    'rax': ('eax', 'ax', 'al', 'ah'), 'rbx': ('ebx', 'bx', 'bl', 'bh'), 'rcx': ('ecx', 'cx', 'cl', 'ch'),
    'rdx': ('edx', 'dx', 'dl', 'dh'), 'rsi': ('esi', 'si', 'sil'), 'rdi': ('edi', 'di', 'dil'),
    'rbp': ('ebp', 'bp', 'bpl'), 'rsp': ('esp', 'sp', 'spl'),
}.items():
    X86_NAMES[full] = (full, 8)
    for name, width in zip(names, (4, 2, 1, 1)):
        X86_NAMES[name] = (full, width)
for n in range(8, 16):
    for suffix, width in (('', 8), ('d', 4), ('w', 2), ('b', 1)):
        X86_NAMES['r' + str(n) + suffix] = ('r' + str(n), width)
for n in range(16):
    X86_NAMES['xmm' + str(n)] = ('xmm' + str(n), 16)
X86_WIDTHS = {'byte': 1, 'word': 2, 'dword': 4, 'qword': 8, 'xmmword': 16}


class X86:
    isa = 'x86_64'
    jump = 'jmp {label}'
    adjust = {'add': 'add {reg}, {imm}', 'sub': 'sub {reg}, {imm}'}
    save = 'mov qword ptr [{base}{off:+d}], {reg}'
    restore = 'mov {reg}, qword ptr [{base}{off:+d}]'
    aim = 'lea {reg}, [{base}{off:+d}]'

    def mem(self, operand, st):
        # (address, width) of a memory operand, or None when it is not one
        match = re.fullmatch(r'(?:(\w+) ptr )?\[(.*)\]', operand)
        if match is None:
            return None
        width = X86_WIDTHS.get(match.group(1)) if match.group(1) else None
        if match.group(1) and width is None:
            raise unreadable('unknown operand size ' + match.group(1))
        addr, sign = const(0), '+'
        for token in re.findall(r'[+-]|[^\s+-]+', match.group(2)):
            if token in '+-':
                sign = token
                continue
            term = token.split('*')
            if term[0] in X86_NAMES:
                value = self.reg(term[0], st)
                if len(term) == 2:
                    value = mul(value, const(int(term[1])))
            elif number(token) is not None:
                value = const(number(token))
            else:
                value = None
            addr = st.derive(add(addr, value) if sign == '+' else sub(addr, value), addr, value)
        return addr, width

    def reg(self, name, st):
        full, width = X86_NAMES[name]
        return st.get(full) if width == 8 else None

    def read(self, operand, st, width=8):
        if operand in X86_NAMES:
            return self.reg(operand, st)
        if number(operand) is not None:
            return const(number(operand))
        mem = self.mem(operand, st)
        if mem is not None:
            return st.load(mem[0], mem[1] or width)
        raise unreadable('unreadable operand ' + operand)

    def width(self, operand):
        return X86_NAMES[operand][1] if operand in X86_NAMES else None

    def write(self, operand, st, value, *inputs, width=None):
        if operand in X86_NAMES:
            full, w = X86_NAMES[operand]
            if w == 4 and value is not None and value[0] is None:
                value = const(value[2] & 0xffffffff)
            elif w != 8:
                value = None
            st.set(full, value, *inputs)
            return
        mem = self.mem(operand, st)
        if mem is None:
            raise unreadable('unwritable operand ' + operand)
        st.store(mem[0], mem[1] or width or 8, value)

    def decode(self, text, line, labels):
        text = re.sub(r'^\{disp32\}\s*', '', text)
        op, _, rest = text.partition(' ')
        ops = split_operands(rest)
        if op == 'ret':
            return Inst(text, line, 'ret')
        if op == 'syscall':
            return Inst(text, line, 'syscall')
        if op in ('jmp', 'call') or (op.startswith('j') and op != 'jmp'):
            target = ops[0]
            if op == 'jmp' and target in labels:
                return Inst(text, line, 'jump', label=target)
            if op.startswith('j') and op != 'jmp':
                if target not in labels:
                    raise unreadable('branch to unknown label: ' + text)
                return Inst(text, line, 'branch', label=target)
            kind = 'call' if op == 'call' else 'tail'
            if target in X86_NAMES or target.endswith(']'):
                return Inst(text, line, kind, through=lambda st: self.read(target, st))
            return Inst(text, line, kind, callee=target)
        handler = getattr(self, 'op_' + op, None)
        if handler is None:
            if op.startswith('set'):
                handler = lambda st, ops: self.write(ops[0], st, None)
            elif op.startswith('cmov'):
                handler = lambda st, ops: self.write(ops[0], st, self.cmov(st, ops))
            else:
                raise unreadable('unknown instruction ' + op + ': ' + text)
        return Inst(text, line, 'op', apply=lambda st: handler(st, ops))

    def cmov(self, st, ops):
        a, b = self.read(ops[0], st), self.read(ops[1], st)
        return a if a == b else None

    def op_mov(self, st, ops):
        value = self.read(ops[1], st, self.width(ops[0]) or 8)
        self.write(ops[0], st, value, width=self.width(ops[1]))

    def op_movzx(self, st, ops):
        self.read(ops[1], st, 1)
        self.write(ops[0], st, None)

    op_movsx = op_movsxd = op_movzx

    def op_lea(self, st, ops):
        self.write(ops[0], st, self.mem(ops[1], st)[0])

    def arith(self, st, ops, fn):
        a, b = self.read(ops[0], st), self.read(ops[1], st)
        self.write(ops[0], st, fn(a, b), a, b, width=self.width(ops[1]))

    def op_add(self, st, ops):
        self.arith(st, ops, add)

    def op_sub(self, st, ops):
        self.arith(st, ops, sub)

    def op_imul(self, st, ops):
        if len(ops) == 3:
            a, b = self.read(ops[1], st), self.read(ops[2], st)
            self.write(ops[0], st, mul(a, b), a, b)
        else:
            self.arith(st, ops, mul)

    def op_shl(self, st, ops):
        self.arith(st, ops, lambda a, b: mul(a, const(1 << b[2])) if b is not None and b[0] is None else None)

    def op_xor(self, st, ops):
        if ops[0] == ops[1] and ops[0] in X86_NAMES:
            self.write(ops[0], st, const(0))
        else:
            self.arith(st, ops, lambda a, b: None)

    def op_and(self, st, ops):
        self.arith(st, ops, lambda a, b: None)

    op_or = op_shr = op_sar = op_and

    def op_inc(self, st, ops):
        a = self.read(ops[0], st)
        self.write(ops[0], st, add(a, const(1)), a)

    def op_dec(self, st, ops):
        a = self.read(ops[0], st)
        self.write(ops[0], st, sub(a, const(1)), a)

    def op_neg(self, st, ops):
        a = self.read(ops[0], st)
        self.write(ops[0], st, None, a)

    op_not = op_neg

    def op_cmp(self, st, ops):
        for operand in ops:
            self.read(operand, st)

    op_test = op_cmp

    def op_push(self, st, ops):
        value = self.read(ops[0], st)
        st.set('rsp', sub(st.get('rsp'), const(8)))
        st.store(st.get('rsp'), 8, value)

    def op_pop(self, st, ops):
        value = st.load(st.get('rsp'), 8)
        st.set('rsp', add(st.get('rsp'), const(8)))
        self.write(ops[0], st, value)


def a64_reg(name):
    # (register, width) of an aarch64 register name, or None
    if name in ('sp', 'xzr', 'wzr'):
        return name if name != 'wzr' else 'xzr', 8 if name != 'wzr' else 4
    match = re.fullmatch(r'([xw])(\d+)', name)
    if match is None or int(match.group(2)) > 30:
        return None
    return 'x' + match.group(2), 8 if match.group(1) == 'x' else 4


class AArch64:
    isa = 'aarch64'
    jump = 'b {label}'
    adjust = {'add': 'add {reg}, {reg}, #{imm}', 'sub': 'sub {reg}, {reg}, #{imm}'}
    save = 'str {reg}, [{base}, #{off}]'
    restore = 'ldr {reg}, [{base}, #{off}]'
    aim = 'add {reg}, {base}, #{off}'
    widths = {'ldr': None, 'str': None, 'ldrb': 1, 'strb': 1, 'ldrh': 2, 'strh': 2, 'ldrsw': 4,
              'ldur': None, 'stur': None, 'ldp': None, 'stp': None}

    def value(self, operand, st):
        reg = a64_reg(operand)
        if reg is not None:
            if reg[0] == 'xzr':
                return const(0)
            return st.get(reg[0]) if reg[1] == 8 else None
        if operand.startswith('#') and number(operand[1:]) is not None:
            return const(number(operand[1:]))
        raise unreadable('unreadable operand ' + operand)

    def write(self, operand, st, value, *inputs):
        reg = a64_reg(operand)
        if reg is None:
            raise unreadable('unwritable operand ' + operand)
        if reg[0] == 'xzr':
            return
        if reg[1] == 4 and not (value is not None and value[0] is None):
            value = None
        st.set(reg[0], value, *inputs)

    def address(self, ops, st):
        # (access address, base register, base after writeback) of a memory operand and its index
        match = re.fullmatch(r'\[(\w+)(?:, (#?[-\w]+))?\](!?)', ops[0])
        if match is None:
            raise unreadable('unreadable address ' + ops[0])
        base = self.value(match.group(1), st)
        offset = self.value(match.group(2), st) if match.group(2) else const(0)
        addr = st.derive(add(base, offset), base, offset)
        if match.group(3):
            return addr, match.group(1), addr
        if len(ops) == 2:
            return base, match.group(1), st.derive(add(base, self.value(ops[1], st)), base)
        return addr, None, None

    def decode(self, text, line, labels):
        op, _, rest = text.partition(' ')
        ops = split_operands(rest)
        if op == 'ret':
            return Inst(text, line, 'ret')
        if op == 'svc':
            return Inst(text, line, 'syscall')
        if op in ('b', 'bl'):
            if op == 'b' and ops[0] in labels:
                return Inst(text, line, 'jump', label=ops[0])
            return Inst(text, line, 'call' if op == 'bl' else 'tail', callee=ops[0])
        if op in ('blr', 'br'):
            return Inst(text, line, 'call' if op == 'blr' else 'tail', through=lambda st: self.value(ops[0], st))
        if op.startswith('b.') or op in ('cbz', 'cbnz', 'tbz', 'tbnz'):
            if ops[-1] not in labels:
                raise unreadable('branch to unknown label: ' + text)
            return Inst(text, line, 'branch', label=ops[-1])
        if op in self.widths:
            return Inst(text, line, 'op', apply=lambda st: self.memory(st, op, ops))
        handler = getattr(self, 'op_' + op, None)
        if handler is None:
            raise unreadable('unknown instruction ' + op + ': ' + text)
        return Inst(text, line, 'op', apply=lambda st: handler(st, ops))

    def memory(self, st, op, ops):
        pair = op in ('ldp', 'stp')
        regs, address = (ops[:2], ops[2:]) if pair else (ops[:1], ops[1:])
        addr, base, writeback = self.address(address, st)
        for index, reg in enumerate(regs):
            parsed = a64_reg(reg)
            if parsed is None:
                raise unreadable('unreadable register ' + reg)
            width = self.widths[op] or parsed[1]
            at = add(addr, const(index * width))
            if op.startswith('st'):
                st.store(at, width, self.value(reg, st) if width == 8 else None)
            else:
                self.write(reg, st, st.load(at, width) if op != 'ldrsw' else None)
        if base is not None:
            self.write(base, st, writeback)

    def op_mov(self, st, ops):
        self.write(ops[0], st, self.value(ops[1], st))

    def op_movz(self, st, ops):
        value = self.value(ops[1], st)
        if len(ops) == 3:
            shift = re.fullmatch(r'lsl #(\d+)', ops[2])
            value = mul(value, const(1 << int(shift.group(1)))) if shift else None
        self.write(ops[0], st, value)

    def op_movk(self, st, ops):
        self.write(ops[0], st, None)

    op_cset = op_movk

    def three(self, st, ops, fn):
        a, b = self.value(ops[1], st), self.value(ops[2], st)
        if len(ops) == 4:
            shift = re.fullmatch(r'lsl #(\d+)', ops[3])
            b = mul(b, const(1 << int(shift.group(1)))) if shift else None
        self.write(ops[0], st, fn(a, b), a, b)

    def op_add(self, st, ops):
        self.three(st, ops, add)

    def op_sub(self, st, ops):
        self.three(st, ops, sub)

    def op_mul(self, st, ops):
        self.three(st, ops, mul)

    def op_and(self, st, ops):
        self.three(st, ops, lambda a, b: None)

    op_orr = op_eor = op_lsr = op_asr = op_and

    def op_lsl(self, st, ops):
        self.three(st, ops, lambda a, b: mul(a, const(1 << b[2])) if b is not None and b[0] is None else None)

    def op_uxtb(self, st, ops):
        a = self.value(ops[1], st)
        self.write(ops[0], st, None, a)

    op_uxth = op_sxtw = op_uxtb

    def op_cmp(self, st, ops):
        for operand in ops:
            self.value(operand, st)

    op_cmn = op_tst = op_cmp


RV_REGS = {'zero', 'ra', 'sp', 'gp', 'tp'} | {'t' + str(n) for n in range(7)} | \
    {'s' + str(n) for n in range(12)} | {'a' + str(n) for n in range(8)}
RV_LOADS = {'ld': 8, 'lw': 4, 'lwu': 4, 'lh': 2, 'lhu': 2, 'lb': 1, 'lbu': 1}
RV_STORES = {'sd': 8, 'sw': 4, 'sh': 2, 'sb': 1}
RV_BRANCHES = {'beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu', 'beqz', 'bnez'}


class RiscV64:
    isa = 'riscv64'
    jump = 'jal zero, {label}'
    adjust = {'add': 'addi {reg}, {reg}, {imm}', 'sub': 'addi {reg}, {reg}, -{imm}'}
    save = 'sd {reg}, {off}({base})'
    restore = 'ld {reg}, {off}({base})'
    aim = 'addi {reg}, {base}, {off}'

    def value(self, operand, st):
        if operand == 'zero':
            return const(0)
        if operand in RV_REGS:
            return st.get(operand)
        if number(operand) is not None:
            return const(number(operand))
        raise unreadable('unreadable operand ' + operand)

    def write(self, operand, st, value, *inputs):
        if operand not in RV_REGS:
            raise unreadable('unwritable operand ' + operand)
        if operand != 'zero':
            st.set(operand, value, *inputs)

    def address(self, operand, st):
        match = re.fullmatch(r'(-?\w+)\((\w+)\)', operand)
        if match is None:
            raise unreadable('unreadable address ' + operand)
        return add(self.value(match.group(2), st), const(int(match.group(1), 0)))

    def decode(self, text, line, labels):
        op, _, rest = text.partition(' ')
        ops = split_operands(rest)
        if op == 'ret' or (op == 'jalr' and ops == ['zero', '0(ra)']):
            return Inst(text, line, 'ret')
        if op == 'ecall':
            return Inst(text, line, 'syscall')
        if op in ('jal', 'j', 'call', 'tail'):
            link = ops[0] if op == 'jal' and len(ops) == 2 else {'call': 'ra', 'j': 'zero', 'tail': 'zero'}.get(op, 'ra')
            target = ops[-1]
            if link == 'zero' and target in labels:
                return Inst(text, line, 'jump', label=target)
            return Inst(text, line, 'call' if link == 'ra' else 'tail', callee=target)
        if op == 'jalr':
            kind = 'call' if ops[0] == 'ra' else 'tail'
            direct = re.fullmatch(r'%pcrel_lo\(([^)]+)\)\(\w+\)', ops[-1])
            if direct is not None:
                return Inst(text, line, kind, callee=direct.group(1))
            return Inst(text, line, kind, through=lambda st: self.address(ops[-1], st))
        if op in RV_BRANCHES:
            if ops[-1] not in labels:
                raise unreadable('branch to unknown label: ' + text)
            return Inst(text, line, 'branch', label=ops[-1])
        if op in RV_LOADS:
            width = RV_LOADS[op]
            return Inst(text, line, 'op', apply=lambda st: self.write(
                ops[0], st, st.load(self.address(ops[1], st), width) if op == 'ld' else None))
        if op in RV_STORES:
            width = RV_STORES[op]
            return Inst(text, line, 'op', apply=lambda st: st.store(
                self.address(ops[1], st), width, self.value(ops[0], st) if width == 8 else None))
        handler = getattr(self, 'op_' + op, None)
        if handler is None:
            raise unreadable('unknown instruction ' + op + ': ' + text)
        return Inst(text, line, 'op', apply=lambda st: handler(st, ops))

    def three(self, st, ops, fn):
        a, b = self.value(ops[1], st), self.value(ops[2], st)
        self.write(ops[0], st, fn(a, b), a, b)

    def op_addi(self, st, ops):
        self.three(st, ops, add)

    op_add = op_addi

    def op_sub(self, st, ops):
        self.three(st, ops, sub)

    def op_mul(self, st, ops):
        self.three(st, ops, mul)

    def op_slli(self, st, ops):
        self.three(st, ops, lambda a, b: mul(a, const(1 << b[2])) if b is not None and b[0] is None else None)

    def op_and(self, st, ops):
        self.three(st, ops, lambda a, b: None)

    op_andi = op_or = op_ori = op_xor = op_xori = op_slt = op_sltu = op_sltiu = op_srli = op_srai = op_and

    def op_mv(self, st, ops):
        self.write(ops[0], st, self.value(ops[1], st))

    op_li = op_mv

    def op_lui(self, st, ops):
        imm = number(ops[1])
        if imm is None:
            raise unreadable('unreadable lui immediate ' + ops[1])
        self.write(ops[0], st, const(imm << 12))

    def op_auipc(self, st, ops):
        self.write(ops[0], st, None)


ISAS = {'x86_64': X86, 'aarch64': AArch64, 'riscv64': RiscV64}
LABEL = re.compile(r'^(\.?[\w.$]+):$')
# directives that only pad: any other directive is read as an unknown instruction
LAYOUT = {'.balign', '.p2align', '.align'}


def function_lines(text, name):
    # the lines of one function, header to the next header
    lines = text.split('\n')
    starts = [i for i, line in enumerate(lines) if line == '# ' + name + ':']
    if len(starts) != 1:
        raise unreadable(name + ' appears ' + str(len(starts)) + ' times in the assembly, expected once')
    end = starts[0] + 1
    while end < len(lines) and not lines[end].startswith('# '):
        end += 1
    return lines[starts[0] + 1:end]


class Function:
    def __init__(self, name, lines, isa):
        self.name, self.lines = name, lines
        labels = {m.group(1) for m in map(LABEL.match, lines) if m}
        self.insts, self.labels, pending, after = [], {}, [], None
        for line, raw in enumerate(lines):
            text = raw.strip()
            if not text or text.split()[0] in LAYOUT:
                continue
            match = LABEL.match(text)
            if match is not None:
                if match.group(1) in self.labels or match.group(1) in pending:
                    raise unreadable(name + ': label ' + match.group(1) + ' is defined twice')
                pending.append(match.group(1))
                after = match.group(1)
                continue
            for label in pending:
                self.labels[label] = len(self.insts)
            pending = []
            inst = isa.decode(text, line, labels)
            inst.after = after
            self.insts.append(inst)
        if pending or not self.insts:
            raise unreadable(name + ': a label or the entry holds no instruction')

    def successors(self, index):
        inst = self.insts[index]
        out = []
        if inst.kind in ('op', 'call', 'syscall', 'branch'):
            if index + 1 == len(self.insts):
                raise unreadable(self.name + ': control falls off the end after ' + inst.text)
            out.append(index + 1)
        if inst.kind in ('branch', 'jump'):
            out.append(self.labels[inst.label])
        return out

    def reaches(self, barriers, target, start=0):
        # whether a path from start meets target before any barrier
        work, seen = [start], set()
        while work:
            index = work.pop()
            if index in seen or index in barriers:
                continue
            if index == target:
                return True
            seen.add(index)
            work.extend(self.successors(index))
        return False

    def where(self, index):
        inst = self.insts[index]
        return '`' + inst.text + '`' + (' after ' + inst.after if inst.after else ' in the entry block')


def entry_state(abi, sret, params):
    regs, mem = {abi['sp']: ('sp', 1, 0)}, {}
    slots = list(abi['args'])
    positions = (['sret'] if sret and abi['sret'] == 'shift' else []) + list(range(params))
    for position, what in enumerate(positions):
        if what == 'sret':
            continue
        if position < len(slots):
            regs[slots[position]] = param(what)
        else:
            mem[abi['stack'] + 8 * (position - len(slots))] = param(what)
    return State(regs, mem, 0)


def flow(fn, target, start, callees):
    # the state before each instruction, joined over every path from the entry
    abi, syscall = target.abi, target.syscall
    states, work = {0: start}, [0]
    while work:
        index = work.pop()
        inst, st = fn.insts[index], states[index].copy()
        if inst.kind == 'op':
            inst.apply(st)
        elif inst.kind in ('call', 'tail'):
            # the callee writes its result through the hidden result pointer
            conv = callees.convention(fn, index, st)
            st.call(abi, abi['args'] + ([conv.sret] if conv.sret else []), lambda reg: reg not in abi['saved'],
                    conv.outgoing)
        elif inst.kind == 'syscall':
            callees.convention(fn, index, st)
            st.call(abi, syscall['args'] + [syscall['number']], lambda reg: reg in syscall['clobbers'], 0)
        for successor in fn.successors(index):
            old = states.get(successor)
            new = st if old is None else old.join(st)
            if old is None or new != old:
                states[successor] = new
                work.append(successor)
    return states


class Target:
    def __init__(self, manifest, name):
        config = tomllib.loads(Path(manifest).read_text()).get('target', {}).get(name)
        if config is None:
            raise unreadable('target ' + name + ' is not in ' + manifest)
        self.name, self.os, self.abi_name = name, config['os'], config['abi']
        if config['isa'] not in ISAS or config['abi'] not in ABIS or self.os not in NATIVE:
            raise unreadable(name + ': no assembly model for ' + config['isa'] + ' ' + config['abi'] + ' ' + self.os)
        abi = ABIS[config['abi']]
        self.isa, self.abi = ISAS[config['isa']](), dict(abi, **abi.get('os', {}).get(self.os, {}))
        self.syscall = SYSCALLS[config['isa']]


class Contract:
    # one checked function: its parameter count, whether it returns through a hidden result pointer,
    # the region it releases, and how its release is recognised
    def __init__(self, name, params, sret, region, release):
        self.name, self.params, self.sret = name, params, sret
        self.region, self.release = region, release

    def releases(self, target, fn, states):
        # instruction index -> the registers that carry the region it frees: (pointer,) or (pointer, length)
        found = {}
        for index, inst in enumerate(fn.insts):
            # an instruction no path reaches never runs
            if index not in states:
                continue
            st = states[index]
            if inst.through is not None:
                callee = inst.through(st)
                if callee is None:
                    raise unreadable(fn.name + ': indirect call through an untraced value at ' + fn.where(index))
                if 'through' in self.release and callee == param(self.release['through']):
                    found[index] = carriers(self.release, target.abi['args'])
            elif inst.kind == 'syscall':
                number = st.get(target.syscall['number'])
                if number is None or number[0] is not None:
                    raise unreadable(fn.name + ': syscall with an untraced number at ' + fn.where(index))
                if self.release.get('syscall') and number[2] == target.syscall['munmap']:
                    found[index] = carriers(self.release, target.syscall['args'])
            elif inst.kind in ('call', 'tail') and inst.callee == self.release.get('symbol'):
                found[index] = carriers(self.release, target.abi['args'])
        return found


def carriers(release, args):
    return tuple(args[release[role]] for role in ('pointer', 'length') if release[role] is not None)


# both return err[io_error.Error], which every abi returns through memory. deallocate's
# release is the os's native one, release_typed's a call through release_fn, a
# fun(ptr, *T, *T, usize) i64 with data second
CONTRACTS = {
    'storage': lambda os: Contract(IR.PORTABLE + 'deallocate', 2, True, (param(0), param(1)), NATIVE[os]),
    'typed': lambda os: Contract(IR.PORTABLE + 'release_typed' + IR.TYPED, 4, True,
                                 (param(1), mul(const(IR.TYPED_SIZE), param(2))),
                                 dict(through=3, params=['ptr', 'ptr', 'ptr', 'i64'], result='i64', pointer=1,
                                      length=None)),
}


class Callees:
    # each callee's signature has one owner: the module IR for a std function, the contract for
    # the indirect release, and NATIVE for the os's release. its placement comes from the abi
    def __init__(self, target, contract, ir):
        self.target, self.contract, self.ir = target, contract, ir
        self.types = Types(ir.table)

    def convention(self, fn, index, st):
        # the placement of the call at index, or None for the release's syscall
        inst, abi, release, syscall = fn.insts[index], self.target.abi, self.contract.release, self.target.syscall
        if inst.kind == 'syscall':
            number = st.get(syscall['number'])
            if number is None or number[0] is not None:
                raise unreadable(fn.name + ': syscall with an untraced number at ' + fn.where(index))
            if not release.get('syscall') or number[2] != syscall['munmap']:
                raise unreadable(fn.name + ': no signature for syscall ' + str(number[2]) + ' at ' + fn.where(index))
            if len(release['params']) > len(syscall['args']):
                raise unreadable(fn.name + ': the syscall at ' + fn.where(index) + ' takes more arguments than registers')
            # on every targeted host the kernel takes all arguments in registers and never writes the caller's stack
            return None
        if inst.through is not None:
            callee = inst.through(st)
            if callee is None:
                raise unreadable(fn.name + ': indirect call through an untraced value at ' + fn.where(index))
            if 'through' not in release or callee != param(release['through']):
                raise unreadable(fn.name + ': no signature for the indirect call through ' + show(callee)
                                 + ' at ' + fn.where(index))
            params, result = release['params'], release['result']
        elif inst.callee == release.get('symbol'):
            params, result = release['params'], release['result']
        else:
            try:
                params, result, variadic = self.ir.signature(inst.callee)
            except ValueError as error:
                raise unreadable(fn.name + ': no signature for ' + fn.where(index) + ': ' + str(error))
            if variadic:
                raise unreadable(fn.name + ': ' + fn.where(index) + ' calls a variadic function, which this check'
                                 ' does not place')
        try:
            return convention(abi, self.types, params, result)
        except Unplaceable as error:
            raise unreadable(fn.name + ': the ' + self.target.abi_name + ' convention cannot place ' + str(error)
                             + ' at ' + fn.where(index))


def wipes(target, fn, states, callees):
    # instruction index -> (pointer, length) of each zeroize call, read where its signature places them
    found = {}
    for index, inst in enumerate(fn.insts):
        if index not in states or inst.kind != 'call' or inst.callee != ZEROIZE:
            continue
        conv = callees.convention(fn, index, states[index])
        regs = [conv.register(target.abi, i) for i in (0, 1)]
        if None in regs:
            raise unreadable(fn.name + ': the wipe ' + fn.where(index) + ' does not take its pointer and length'
                             ' in one argument register each')
        found[index] = tuple(states[index].get(reg) for reg in regs)
    return found


def check(target, contract, ir, lines):
    fn = Function(contract.name, lines, target.isa)
    start = entry_state(target.abi, contract.sret, contract.params)
    callees = Callees(target, contract, ir)
    states = flow(fn, target, start, callees)
    releases = contract.releases(target, fn, states)
    if not releases:
        raise unreadable(fn.name + ': no native release found')
    found = wipes(target, fn, states, callees)
    want = show(contract.region[0]) + ' for ' + show(contract.region[1]) + ' bytes'
    for index, regs in sorted(releases.items()):
        freed = tuple(states[index].get(reg) for reg in regs)
        if None in freed:
            raise unreadable(fn.name + ': the release ' + fn.where(index) + ' frees an untraced region')
        if freed != contract.region[:len(freed)]:
            raise Rejected('region', fn.name + ': the release ' + fn.where(index) + ' frees '
                           + ' for '.join(map(show, freed)) + (' bytes' if len(freed) == 2 else '')
                           + ', not the released region ' + want)
        if fn.reaches(set(found), index):
            hint = '' if found else (' (no call to ' + ZEROIZE + ' remains: this check requires zeroize to stay'
                                      ' a call in release builds and does not read an inlined kernel)')
            raise Rejected('order', fn.name + ': the release ' + fn.where(index) + ' is reachable without any wipe' + hint)
        matching = {i for i, region in found.items() if region == contract.region}
        if fn.reaches(matching, index):
            others = ', '.join(fn.where(i) + ' wipes ' + show(r[0]) + ' for ' + show(r[1]) + ' bytes'
                               for i, r in sorted(found.items()) if r != contract.region)
            raise Rejected('region', fn.name + ': the release ' + fn.where(index) + ' is reachable without a wipe of '
                           + want + ' (' + others + ')')
    return fn, found, releases, states


def wipe_site(fn, found):
    if len(found) != 1:
        raise unreadable('control: ' + fn.name + ' holds ' + str(len(found)) + ' wipes, expected one')
    return fn.insts[next(iter(found))].line


def deleted(fn, found):
    # the call removed, with the address setup that names the kernel beside it
    line = wipe_site(fn, found)
    drop = {line} | ({line - 1} if ZEROIZE in fn.lines[line - 1] else set())
    return [text for n, text in enumerate(fn.lines) if n not in drop]


def adjust(target, lines, line, reg, op, imm):
    # the register changed by imm just before the instruction on line
    return lines[:line] + ['  ' + target.isa.adjust[op].format(reg=reg, imm=imm)] + lines[line:]


def adjusted(target, fn, found, arg, op, imm):
    return adjust(target, fn.lines, wipe_site(fn, found), target.abi['args'][arg], op, imm)


def moved(target, fn, releases):
    # every release frees a pointer 16 bytes past the region it was given
    lines = fn.lines
    for index, regs in sorted(releases.items(), reverse=True):
        lines = adjust(target, lines, fn.insts[index].line, regs[0], 'add', 16)
    return lines


def bypass(fn, found):
    # a branch whose taken arm never reaches the wipe now lands just past it, on the release path
    line = wipe_site(fn, found)
    wipe = next(iter(found))
    for inst in fn.insts:
        if inst.kind == 'branch' and not fn.reaches(set(), wipe, fn.labels[inst.label]):
            lines = list(fn.lines)
            lines[inst.line] = re.sub(re.escape(inst.label) + r'$', '.Lbypass', lines[inst.line])
            return lines[:line + 1] + ['.Lbypass:'] + lines[line + 1:]
    raise unreadable('control: ' + fn.name + ' has no branch whose taken arm avoids the wipe')


def resigned(ir, name, params=None, result=None, unknown=False):
    # the module IR with name's header taking params or returning result, or renamed away
    pattern = r'^(  fn @"' + re.escape(name) + r')("\()(.*?)(\): )(!\d+)( \[)'
    edit = lambda m: (m.group(1) + ('.unknown' if unknown else '') + m.group(2)
                      + (m.group(3) if params is None else ', '.join(params)) + m.group(4)
                      + (result or m.group(5)) + m.group(6))
    text, n = re.subn(pattern, edit, ir.text, flags=re.M)
    if n == 0:
        raise unreadable('control: no header for ' + name + ' in the module IR')
    return IR.IR(text)


def type_ref(ir, test):
    ref = next((k for k, v in ir.table.items() if test(v)), None)
    if ref is None:
        raise unreadable('control: the module IR has no type for the control')
    return ref


def defined(ir, texts):
    # the module IR with each type spelled in texts in its table, and their references
    refs, lines, table = [], [], dict(ir.table)
    for text in texts:
        ref = next((k for k, v in table.items() if v == text), None)
        if ref is None:
            ref = '!' + str(max([-1] + [int(k[1:]) for k in table]) + 1)
            table[ref] = text
            lines.append('    ' + ref + ' = ' + text + '\n')
        refs.append(ref)
    head = ir.text.index('  types {\n') + len('  types {\n')
    return IR.IR(ir.text[:head] + ''.join(lines) + ir.text[head:]), refs


def control_types(ir):
    # the module IR with the scalars and records the controls sign zeroize with
    ir, (i32, i64, ptr) = defined(ir, ['i32', 'i64', 'ptr'])
    record = lambda *fields: '{' + ', '.join(fields) + '}[align=0 packed=false]'
    ir, records = defined(ir, [record(i64, i64, i64), record(i64, i64), record(i32, i32)])
    return ir, dict(i64=i64, ptr=ptr, records=records, large=records[0])


def stack_bytes(slot):
    # the [start, end) of the outgoing area a slot's value is copied into, or None
    if slot.kind == 'stack':
        return slot.offset, slot.offset + slot.size
    words = [p[1] for p in slot.pieces if p[0] == 'stack']
    if slot.kind == 'reg' and words:
        return slot.offset, slot.offset + sum(round_up(w or 8, 8) for w in words)
    return None


def covering(target, ir, last, offset):
    # zeroize's parameters with enough integers ahead of last that last is copied over offset, or None
    abi, (ir, kinds) = target.abi, control_types(ir)
    for n in range(4 * len(abi['args']) + offset // 8):
        params = [kinds['ptr'], kinds['i64']] + [kinds['i64']] * n + [last(kinds)]
        where = stack_bytes(convention(abi, Types(ir.table), params, 'void').params[-1])
        if where is not None and where[0] <= offset < where[1]:
            return ir, params
    return None


def outgoing_pointer(target, ir, offset):
    # zeroize takes pointers until one is an outgoing argument over offset
    found = covering(target, ir, lambda kinds: kinds['ptr'], offset)
    return None if found is None else (resigned(found[0], ZEROIZE, params=found[1]), ir)


def outgoing_record(target, ir, offset):
    # zeroize takes the first record the abi copies by value over offset, past enough integers
    for index in range(3):
        found = covering(target, ir, lambda kinds: kinds['records'][index], offset)
        if found is not None:
            changed, params = found
            return resigned(changed, ZEROIZE, params=params), resigned(changed, ZEROIZE, params=params[:-1])
    return None


def shifted_result(target, ir, offset):
    # zeroize takes integers up to offset and returns a record through a hidden result pointer
    abi, (ir, kinds) = target.abi, control_types(ir)
    params = [kinds['ptr'], kinds['i64']] + [kinds['i64']] * (len(abi['args']) + (offset - abi['home']) // 8 - 2)
    if convention(abi, Types(ir.table), params, kinds['large']).result.kind != 'sret':
        raise unreadable('control: the ' + kinds['large'] + ' record does not return through a hidden pointer')
    return resigned(ir, ZEROIZE, params=params, result=kinds['large']), resigned(ir, ZEROIZE, params=params)


def free_slot(target, states, call):
    # the call's stack pointer and the lowest outgoing slot above its home area the function never tracks
    abi = target.abi
    sp = states[call].get(abi['sp'])[2]
    used = {o for st in states.values() for o in st.mem}
    slot = sp + abi['home']
    while slot in used:
        slot += 8
    return sp, slot


def readback(target, fn, found, releases, states, via, slot, before=()):
    # the wipe's pointer stored into slot through via before the wipe, with before after it, and each
    # release freeing what it reads back from that slot
    abi, isa = target.abi, target.isa
    line = wipe_site(fn, found)
    at = states[next(iter(found))].get(via)
    if ZEROIZE in fn.lines[line - 1]:
        line -= 1
    edits = [(line, text) for text in reversed(before)]
    edits.append((line, isa.save.format(reg=abi['args'][0], base=via, off=slot - at[2])))
    for index, regs in releases.items():
        off = slot - states[index].get(abi['sp'])[2]
        edits.append((fn.insts[index].line, isa.restore.format(reg=regs[0], base=abi['sp'], off=off)))
    lines = list(fn.lines)
    for where, text in sorted(edits, key=lambda e: e[0], reverse=True):
        lines.insert(where, '  ' + text)
    return lines


def clobbered(target, fn, found, releases, states, ir, via, resign):
    # zeroize signed by resign so that an outgoing slot is its, the wipe's pointer stored there, and read back
    # by each release. with the baseline signature resign also gives, the same edit is accepted
    call = next(iter(found))
    sp, slot = free_slot(target, states, call)
    at = states[call].get(via)
    if not is_frame(at) or at[1] != 1:
        return 'the frame pointer is not a traced frame address at the wipe'
    signed = resign(target, ir, slot - sp)
    if signed is None:
        return 'no signature makes the slot an outgoing argument'
    lines = readback(target, fn, found, releases, states, via, slot)
    return lines, signed[0], signed[1]


def result_buffer(target, fn, found, releases, states, ir):
    # zeroize returns a record through a hidden result pointer aimed at the slot holding the wipe's pointer
    abi = target.abi
    if abi['sret'] == 'shift':
        return 'the hidden result pointer rides an argument register, which every call escapes'
    sp, slot = free_slot(target, states, next(iter(found)))
    aim = target.isa.aim.format(reg=abi['sret'], base=abi['sp'], off=slot - sp)
    lines = readback(target, fn, found, releases, states, abi['sp'], slot, before=[aim])
    changed, kinds = control_types(ir)
    return lines, resigned(changed, ZEROIZE, result=kinds['large']), ir


def reversed_layout(target, fn):
    # the same graph with every labelled block after the first laid out in reverse
    blocks, current = [], []
    for text in fn.lines:
        if LABEL.match(text.strip()) and current:
            blocks.append(current)
            current = []
        current.append(text)
    blocks.append(current)
    labels = [LABEL.match(block[0].strip()) for block in blocks]
    if any(label is None for label in labels[1:]):
        raise unreadable('control: ' + fn.name + ' has an unlabelled block')
    jump = lambda label: '  ' + target.isa.jump.format(label=label)
    for index in range(len(blocks) - 1):
        blocks[index] = blocks[index] + [jump(labels[index + 1].group(1))]
    return blocks[0] + [line for block in reversed(blocks[1:]) for line in block]


def controls(target, sources):
    accepted, counts = [], {}
    for key, make in CONTRACTS.items():
        contract = make(target.os)
        asm, ir = sources[key]
        fn, found, releases, states = check(target, contract, ir, function_lines(asm, contract.name))
        label = contract.name.split('$')[0].rsplit('.', 1)[-1]
        name = label + ': reversed block layout'
        try:
            check(target, contract, ir, reversed_layout(target, fn))
        except Rejected as error:
            raise unreadable('assembly oracle rejected control ' + name + ': ' + str(error))
        accepted.append(name)
        tag = type_ref(ir, lambda t: t.startswith('tag{'))
        sp, fp = target.abi['sp'], target.abi['fp']
        shift = target.abi['sret'] == 'shift'
        # reason None is a control the oracle must accept
        cases = [
            ('deleted wipe', 'order', (deleted(fn, found), ir, None)),
            ('release on an unwiped path', 'order', (bypass(fn, found), ir, None)),
            ('wipe of the wrong pointer', 'region', (adjusted(target, fn, found, 0, 'add', 8), ir, None)),
            ('wipe of a short length', 'region', (adjusted(target, fn, found, 1, 'sub', 1), ir, None)),
            ('release of another pointer', 'region', (moved(target, fn, releases), ir, None)),
            ('release of a pointer read back from a clobbered outgoing slot', 'unreadable',
             clobbered(target, fn, found, releases, states, ir, sp, outgoing_pointer)),
            ('release of a pointer read back from an outgoing slot written through the frame pointer', 'unreadable',
             clobbered(target, fn, found, releases, states, ir, fp, outgoing_pointer)),
            ('release of a pointer read back from a by-value record argument copied onto the stack', 'unreadable',
             clobbered(target, fn, found, releases, states, ir, sp, outgoing_record)),
            ('release of a pointer read back from the stack slot an aggregate result shifts an argument onto' if shift
             else 'release of a pointer read back from past the register arguments of a callee returning an aggregate',
             'unreadable' if shift else None, clobbered(target, fn, found, releases, states, ir, sp, shifted_result)),
            ('release of a pointer read back from the hidden result buffer', 'unreadable',
             result_buffer(target, fn, found, releases, states, ir)),
            ('wipe through a callee with no signature', 'unreadable',
             (fn.lines, resigned(ir, ZEROIZE, unknown=True), None)),
            ('wipe through a callee taking an aggregate the convention cannot place', 'unreadable',
             (fn.lines, resigned(ir, ZEROIZE, params=[tag, type_ref(ir, lambda t: t == 'i64')]), None)),
            ('wipe through a callee returning an aggregate the convention cannot place', 'unreadable',
             (fn.lines, resigned(ir, ZEROIZE, result=tag), None)),
        ]
        for name, reason, changed in cases:
            name = label + ': ' + name
            if isinstance(changed, str):
                print('skipped ' + name + ': ' + changed)
                continue
            lines, signed, baseline = changed
            if baseline is not None:
                try:
                    check(target, contract, baseline, lines)
                except Rejected as error:
                    raise unreadable('control ' + name + ' is rejected without the signature it tests: ' + str(error))
            try:
                check(target, contract, signed, lines)
            except Rejected as error:
                if error.reason != reason:
                    raise unreadable('control ' + name + ' was rejected for ' + error.reason + ', not '
                                     + str(reason) + ': ' + str(error))
                print('rejected ' + name + ' (' + reason + '): ' + str(error))
                counts[reason] = counts.get(reason, 0) + 1
                continue
            if reason is not None:
                raise unreadable('assembly oracle accepted control: ' + name)
            accepted.append(name)
    print('OK: ' + target.name + ' assembly oracle accepts ' + ', '.join(accepted) + ', and rejects '
          + ', '.join(str(n) + ' ' + reason for reason, n in sorted(counts.items())) + ' controls')


if __name__ == '__main__':
    if len(sys.argv) != 7:
        raise SystemExit('usage: verify-asm.py <mach.toml> <target> <storage.s> <storage.ir> <main.s> <main.ir>')
    manifest, name, storage, storage_ir, main, main_ir = sys.argv[1:7]
    try:
        sources = {key: (Path(asm).read_text(), IR.IR(Path(ir).read_text()))
                   for key, asm, ir in (('storage', storage, storage_ir), ('typed', main, main_ir))}
        controls(Target(manifest, name), sources)
    except Rejected as error:
        raise SystemExit('FAIL: ' + str(error))
