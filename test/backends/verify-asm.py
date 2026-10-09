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
# argument register, or fed to an operation the pass does not model), the
# caller's memory above the entry stack pointer, and the call's outgoing area.
# that area is [sp, sp + n) at the call, whatever register wrote it, where n is
# the abi's home area plus 8 bytes for each argument past the argument
# registers (apple arm64 packs narrower ones tighter, which that covers). the
# argument count comes from the callee's signature: a std function's header in
# the module IR, the release_fn type for the indirect release, or the native
# release's entry below. a call whose signature the pass cannot get, or whose
# parameters or result are not scalars or pointers, fails.
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


# per abi: integer argument registers, where the hidden result pointer goes
# ('shift' takes the first argument register), the entry stack offset of the
# first stack argument, the home area a callee owns above the call's stack
# pointer, below its stack arguments, the registers a call preserves, and the
# frame pointer
ABIS = {
    'sysv64': dict(args=['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9'], sret='shift', stack=8, home=0,
                   saved={'rbx', 'rbp', 'rsp', 'r12', 'r13', 'r14', 'r15'}, sp='rsp', fp='rbp'),
    'win64': dict(args=['rcx', 'rdx', 'r8', 'r9'], sret='shift', stack=40, home=32,
                  saved={'rbx', 'rbp', 'rdi', 'rsi', 'rsp', 'r12', 'r13', 'r14', 'r15'}, sp='rsp', fp='rbp'),
    'aapcs64': dict(args=['x' + str(n) for n in range(8)], sret='x8', stack=0, home=0,
                    saved={'x' + str(n) for n in range(19, 30)} | {'sp'}, sp='sp', fp='x29'),
    'lp64': dict(args=['a' + str(n) for n in range(8)], sret='shift', stack=0, home=0,
                 saved={'s' + str(n) for n in range(12)} | {'sp'}, sp='sp', fp='s0'),
}

# per isa: the linux syscall's number register, argument registers and clobbers,
# and munmap's number
SYSCALLS = {
    'x86_64': dict(number='rax', args=['rdi', 'rsi', 'rdx', 'r10', 'r8', 'r9'], clobbers={'rax', 'rcx', 'r11'}, munmap=11),
    'aarch64': dict(number='x8', args=['x0', 'x1', 'x2', 'x3', 'x4', 'x5'], clobbers={'x0'}, munmap=215),
    'riscv64': dict(number='a7', args=['a0', 'a1', 'a2', 'a3', 'a4', 'a5'], clobbers={'a0', 'a1'}, munmap=215),
}

# per os: the native release, what it calls, its argument count and which
# arguments carry the region
NATIVE = {
    'linux': dict(syscall=True, args=2, pointer=0, length=1),
    'darwin': dict(symbol='_free', args=1, pointer=0, length=None),
    'windows': dict(symbol='VirtualFree', args=3, pointer=0, length=None),
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
            st.call(abi, abi['args'], lambda reg: reg not in abi['saved'], callees.outgoing(fn, index, st))
        elif inst.kind == 'syscall':
            st.call(abi, syscall['args'] + [syscall['number']], lambda reg: reg in syscall['clobbers'],
                    callees.outgoing(fn, index, st))
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
        self.name, self.os = name, config['os']
        if config['isa'] not in ISAS or config['abi'] not in ABIS or self.os not in NATIVE:
            raise unreadable(name + ': no assembly model for ' + config['isa'] + ' ' + config['abi'] + ' ' + self.os)
        self.isa, self.abi = ISAS[config['isa']](), ABIS[config['abi']]
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
                                 dict(through=3, args=4, pointer=1, length=None)),
}


# a parameter or result one argument register or 8 byte stack slot holds
SCALAR = re.compile(r'i(1|8|16|32|64)|ptr')


class Callees:
    # each callee's signature has one owner: the module IR for a std function, the contract for
    # the indirect release, and NATIVE for the os's release
    def __init__(self, target, contract, ir):
        self.target, self.contract, self.ir = target, contract, ir

    def outgoing(self, fn, index, st):
        # the bytes above the stack pointer that the call at index owns
        inst, abi, release, syscall = fn.insts[index], self.target.abi, self.contract.release, self.target.syscall
        if inst.kind == 'syscall':
            number = st.get(syscall['number'])
            if number is None or number[0] is not None:
                raise unreadable(fn.name + ': syscall with an untraced number at ' + fn.where(index))
            if not release.get('syscall') or number[2] != syscall['munmap']:
                raise unreadable(fn.name + ': no signature for syscall ' + str(number[2]) + ' at ' + fn.where(index))
            if release['args'] > len(syscall['args']):
                raise unreadable(fn.name + ': the syscall at ' + fn.where(index) + ' takes more arguments than registers')
            # on every targeted host the kernel takes all arguments in registers and never writes the caller's stack
            return 0
        if inst.through is not None:
            callee = inst.through(st)
            if callee is None:
                raise unreadable(fn.name + ': indirect call through an untraced value at ' + fn.where(index))
            if 'through' not in release or callee != param(release['through']):
                raise unreadable(fn.name + ': no signature for the indirect call through ' + show(callee)
                                 + ' at ' + fn.where(index))
            count = release['args']
        elif inst.callee == release.get('symbol'):
            count = release['args']
        else:
            try:
                params, result = self.ir.signature(inst.callee)
            except ValueError as error:
                raise unreadable(fn.name + ': no signature for ' + fn.where(index) + ': ' + str(error))
            shape = ' (' + ', '.join(map(str, params)) + ') -> ' + str(result)
            if not all(SCALAR.fullmatch(t or '') for t in params):
                raise unreadable(fn.name + ': ' + fn.where(index) + ' passes a by-value aggregate:' + shape)
            if not (result == 'void' or SCALAR.fullmatch(result or '')):
                raise unreadable(fn.name + ': ' + fn.where(index) + ' returns an aggregate:' + shape)
            count = len(params)
        return abi['home'] + 8 * max(0, count - len(abi['args']))


def wipes(target, fn, states):
    # instruction index -> (pointer, length) of each zeroize call
    regs = target.abi['args']
    return {index: (states[index].get(regs[0]), states[index].get(regs[1]))
            for index, inst in enumerate(fn.insts)
            if index in states and inst.kind == 'call' and inst.callee == ZEROIZE}


def check(target, contract, ir, lines):
    fn = Function(contract.name, lines, target.isa)
    start = entry_state(target.abi, contract.sret, contract.params)
    states = flow(fn, target, start, Callees(target, contract, ir))
    releases = contract.releases(target, fn, states)
    if not releases:
        raise unreadable(fn.name + ': no native release found')
    found = wipes(target, fn, states)
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


def clobbered(target, fn, found, releases, states, ir, via):
    # zeroize takes stack arguments, the wipe's pointer is stored into one of them through via
    # before the call, and each release frees what it reads back from that slot after the call
    abi, isa = target.abi, target.isa
    line = wipe_site(fn, found)
    call = next(iter(found))
    sp, at = states[call].get(abi['sp'])[2], states[call].get(via)
    if not is_frame(at) or at[1] != 1:
        return None
    used = {o for st in states.values() for o in st.mem}
    slot = sp + abi['home']
    while slot in used:
        slot += 8
    count = len(abi['args']) + (slot - sp - abi['home']) // 8 + 1
    if ZEROIZE in fn.lines[line - 1]:
        line -= 1
    edits = [(line, isa.save.format(reg=abi['args'][0], base=via, off=slot - at[2]))]
    for index, regs in releases.items():
        off = slot - states[index].get(abi['sp'])[2]
        edits.append((fn.insts[index].line, isa.restore.format(reg=regs[0], base=abi['sp'], off=off)))
    lines = list(fn.lines)
    for where, text in sorted(edits, reverse=True):
        lines.insert(where, '  ' + text)
    return lines, resigned(ir, ZEROIZE, params=[type_ref(ir, lambda t: t == 'ptr')] * count)


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
        aggregate = type_ref(ir, lambda t: t.startswith('{'))
        rejected = [
            ('deleted wipe', 'order', (deleted(fn, found), ir)),
            ('release on an unwiped path', 'order', (bypass(fn, found), ir)),
            ('wipe of the wrong pointer', 'region', (adjusted(target, fn, found, 0, 'add', 8), ir)),
            ('wipe of a short length', 'region', (adjusted(target, fn, found, 1, 'sub', 1), ir)),
            ('release of another pointer', 'region', (moved(target, fn, releases), ir)),
            ('release of a pointer read back from a clobbered outgoing slot', 'unreadable',
             clobbered(target, fn, found, releases, states, ir, target.abi['sp'])),
            ('release of a pointer read back from an outgoing slot written through the frame pointer', 'unreadable',
             clobbered(target, fn, found, releases, states, ir, target.abi['fp'])),
            ('wipe through a callee with no signature', 'unreadable', (fn.lines, resigned(ir, ZEROIZE, unknown=True))),
            ('wipe through a callee taking a by-value aggregate', 'unreadable',
             (fn.lines, resigned(ir, ZEROIZE, params=[aggregate, type_ref(ir, lambda t: t == 'i64')]))),
            ('wipe through a callee returning an aggregate', 'unreadable',
             (fn.lines, resigned(ir, ZEROIZE, result=aggregate))),
        ]
        for name, reason, changed in rejected:
            name = label + ': ' + name
            if changed is None:
                print('skipped ' + name + ': the frame pointer is not a traced frame address at the wipe')
                continue
            try:
                check(target, contract, changed[1], changed[0])
            except Rejected as error:
                if error.reason != reason:
                    raise unreadable('control ' + name + ' was rejected for ' + error.reason + ', not ' + reason + ': ' + str(error))
                print('rejected ' + name + ' (' + reason + '): ' + str(error))
                counts[reason] = counts.get(reason, 0) + 1
                continue
            raise unreadable('assembly oracle accepted control: ' + name)
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
