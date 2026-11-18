[std](../README.md) / [system](README.md) / **cpu**

# std.system.cpu

the running processor's instruction-set extensions

`features()` is the one facility std uses to pick a hardware path at run
time, such as the SHA-NI and ARMv8 SHA2 backends of mach-crypto's sha256 and
its AES and carry-less multiply paths. the record and its field names are the
compiler's own extension vocabulary, declared per architecture in
std.system.cpu.features, so `have.sha2` on x86_64 is a compile error exactly
as `$mach.build.ext.sha2` is.

the answer is computed once and cached. an extension the build target
selects is reported present without a probe, because the binary already
requires it. the rest comes from cpuid on x86_64, which needs no operating
system, and from the OS on aarch64 (linux auxv AT_HWCAP, darwin sysctl),
where the id registers are not readable from user mode, and on riscv64 linux
(riscv_hwprobe, else auxv AT_HWCAP). a freestanding aarch64 or riscv build
without the cpu group reports only what it selects, so the portable path
runs, and so does every wasm32 build, which has no query at all.

selecting an extension admits its instructions and nothing more. selecting
`dit`, when it exists, will say the instructions may be emitted, never that
the mode is on.

this module builds freestanding.

Source: [`src/system/cpu.mach`](../../../src/system/cpu.mach)

| Functions | |
| :--- | :--- |
| [`features`](#features) | the extensions the running processor has |

| Forwards | |
| :--- | :--- |
| [`Features`](#features-1) | |

---

## Functions

### features

```mach
pub fun features() Features
```

the extensions the running processor has

computed on the first call and cached. every call returns the same value
for the life of the process. a concurrent first call computes the same
value twice and stores it twice, which is harmless

| Parameter | |
| :--- | :--- |
| **returns** | the per-architecture record, every field true when the processor has it |

## Forwards

### Features

Forwards [`std.system.cpu.features.Features`](cpu/features.md#features).

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
pub rec Features {
    sha:    bool;
    ssse3:  bool;
    sse41:  bool;
    aes:    bool;
    pclmul: bool;
}
```

Where `$mach.build.arch == $mach.arch.aarch64`:

```mach
pub rec Features {
    sha2:  bool;
    aes:   bool;
    pmull: bool;
}
```

Where `$mach.build.arch == $mach.arch.riscv64 || $mach.build.arch == $mach.arch.riscv32`:

```mach
pub rec Features {
    i:        bool;
    m:        bool;
    a:        bool;
    f:        bool;
    d:        bool;
    c:        bool;
    zicsr:    bool;
    zifencei: bool;
    zkt:      bool;
}
```

Where `$mach.build.arch == $mach.arch.wasm32`:

```mach
pub rec Features {
    simd128: bool;
}
```

x86_64 extensions std detects

