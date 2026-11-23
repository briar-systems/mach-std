[std](../../README.md) / [system](../README.md) / [cpu](README.md) / **features**

# std.system.cpu.features

the per-architecture feature record, its build-time selection, and the probe that
needs no operating system

this module imports nothing OS-bound. std.system.cpu reports features at run
time through it, and the per-OS modules fill it for the isas whose feature
bits are only readable through the OS (aarch64). it is a separate module so
that std.system.os can name the record without importing std.system.cpu.

the record is declared once per architecture under `$if ($mach.build.arch == ...)`,
and its field names are exactly the compiler's extension names for that architecture
(`$mach.build.ext.<name>`). a field of another architecture is a compile error,
as it is for the compiler. beside each field one `val` reads the compiler's
row, so this record fails to compile the moment the compiler drops or renames
an extension. the SELECTED_* values say what the build target selects: a
selected extension is required by the binary, so it is reported present
without a probe.

Source: [`src/system/cpu/features.mach`](../../../../src/system/cpu/features.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Features`](#features) | `rec` | x86_64 extensions std detects |

| On `Features` | |
| :--- | :--- |
| [`selected`](#selected) | the features the build target selects, which the binary requires |
| [`probe`](#probe) | the features the running processor reports through cpuid |
| [`merge`](#merge) | the union of what the build selects and what the processor reports |
| [`from_hwprobe`](#from_hwprobe) | decode the riscv_hwprobe values for the base behaviour and IMA_EXT_0 keys |
| [`from_hwcap`](#from_hwcap) | decode AT_HWCAP, which names single-letter extensions only |

| Constants | |
| :--- | :--- |
| [`SELECTED_SHA`](#constants), [`SELECTED_SSSE3`](#constants), [`SELECTED_SSE41`](#constants), [`SELECTED_AES`](#constants), [`SELECTED_PCLMUL`](#constants), [`SELECTED_SHA2`](#constants), [`SELECTED_PMULL`](#constants), [`SELECTED_I`](#constants), [`SELECTED_M`](#constants), [`SELECTED_A`](#constants), [`SELECTED_F`](#constants), [`SELECTED_D`](#constants), [`SELECTED_C`](#constants), [`SELECTED_ZICSR`](#constants), [`SELECTED_ZIFENCEI`](#constants), [`SELECTED_ZKT`](#constants) | |
| [`HWPROBE_BASE_BEHAVIOR`](#constants) | riscv_hwprobe keys, and the bits of the two values std reads |
| [`HWPROBE_IMA_EXT_0`](#constants), [`SELECTED_SIMD128`](#constants) | |

---

## Features

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

| Field | Type | |
| :--- | :--- | :--- |
| `sha` | `bool` | SHA-NI (sha256rnds2, sha256msg1, sha256msg2) |
| `ssse3` | `bool` | pshufb, palignr |
| `sse41` | `bool` | pblendw, pinsrd, pextrd, ptest |
| `aes` | `bool` | AES-NI (aesenc, aesenclast, aesdec, aesdeclast, aesimc, aeskeygenassist) |
| `pclmul` | `bool` | pclmulqdq |

### selected

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
pub fun selected() Features
```

Where `$mach.build.arch == $mach.arch.aarch64`:

```mach
pub fun selected() Features
```

Where `$mach.build.arch == $mach.arch.riscv64 || $mach.build.arch == $mach.arch.riscv32`:

```mach
pub fun selected() Features
```

Where `$mach.build.arch == $mach.arch.wasm32`:

```mach
pub fun selected() Features
```

the features the build target selects, which the binary requires

### probe

Only where `$mach.build.arch == $mach.arch.x86_64`.

```mach
pub fun probe(out: *Features)
```

the features the running processor reports through cpuid

leaf 1 ecx bit 9 is ssse3, bit 19 is sse4.1, bit 25 is aes and bit 1 is
pclmulqdq. leaf 7 subleaf 0 ebx bit 29 is sha, and leaf 0 eax says
whether leaf 7 exists. all five use only xmm state, which every x86_64
operating system enables, so no xgetbv check is needed. cpuid is
baseline on x86_64 and needs no OS

### merge

Declared by the first of these arms whose condition holds.

Where `$mach.build.arch == $mach.arch.x86_64`:

```mach
pub fun merge(out: *Features, probed: Features)
```

Where `$mach.build.arch == $mach.arch.aarch64`:

```mach
pub fun merge(out: *Features, probed: Features)
```

Where `$mach.build.arch == $mach.arch.riscv64 || $mach.build.arch == $mach.arch.riscv32`:

```mach
pub fun merge(out: *Features, probed: Features)
```

the union of what the build selects and what the processor reports

### from_hwprobe

Only where `$mach.build.arch == $mach.arch.riscv64 || $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64`.

```mach
pub fun from_hwprobe(out: *Features, base: u64, ext0: u64)
```

decode the riscv_hwprobe values for the base behaviour and IMA_EXT_0 keys

| Parameter | |
| :--- | :--- |
| `out` | record to fill, zicsr and zifencei set false |
| `base` | the value for HWPROBE_BASE_BEHAVIOR, 0 when the key is unknown |
| `ext0` | the value for HWPROBE_IMA_EXT_0, 0 when the key is unknown |

### from_hwcap

Only where `$mach.build.arch == $mach.arch.riscv64 || $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64`.

```mach
pub fun from_hwcap(out: *Features, hwcap: u64)
```

decode AT_HWCAP, which names single-letter extensions only

| Parameter | |
| :--- | :--- |
| `out` | record to fill, zkt, zicsr and zifencei set false |
| `hwcap` | the AT_HWCAP auxv value |

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `SELECTED_SHA` | `bool` | `$mach.build.ext.sha == 1` where `$mach.build.arch == $mach.arch.x86_64` |  |
| `SELECTED_SSSE3` | `bool` | `$mach.build.ext.ssse3 == 1` where `$mach.build.arch == $mach.arch.x86_64` |  |
| `SELECTED_SSE41` | `bool` | `$mach.build.ext.sse41 == 1` where `$mach.build.arch == $mach.arch.x86_64` |  |
| `SELECTED_AES` | `bool` | `$mach.build.ext.aes == 1` where `$mach.build.arch == $mach.arch.x86_64`; `$mach.build.ext.aes == 1` where `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_PCLMUL` | `bool` | `$mach.build.ext.pclmul == 1` where `$mach.build.arch == $mach.arch.x86_64` |  |
| `SELECTED_SHA2` | `bool` | `$mach.build.ext.sha2 == 1` where `$mach.build.arch == $mach.arch.aarch64` and not `$mach.build.arch == $mach.arch.x86_64` |  |
| `SELECTED_PMULL` | `bool` | `$mach.build.ext.pmull == 1` where `$mach.build.arch == $mach.arch.aarch64` and not `$mach.build.arch == $mach.arch.x86_64` |  |
| `SELECTED_I` | `bool` | `$mach.build.ext.i == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_M` | `bool` | `$mach.build.ext.m == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_A` | `bool` | `$mach.build.ext.a == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_F` | `bool` | `$mach.build.ext.f == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_D` | `bool` | `$mach.build.ext.d == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_C` | `bool` | `$mach.build.ext.c == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_ZICSR` | `bool` | `$mach.build.ext.zicsr == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_ZIFENCEI` | `bool` | `$mach.build.ext.zifencei == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_ZKT` | `bool` | `$mach.build.ext.zkt == 1` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `HWPROBE_BASE_BEHAVIOR` | `i64` | `3` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` | riscv_hwprobe keys, and the bits of the two values std reads |
| `HWPROBE_IMA_EXT_0` | `i64` | `4` where `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` and not `$mach.build.arch == $mach.arch.x86_64` nor `$mach.build.arch == $mach.arch.aarch64` |  |
| `SELECTED_SIMD128` | `bool` | `$mach.build.ext.simd128 == 1` where `$mach.build.arch == $mach.arch.wasm32` and not `$mach.build.arch == $mach.arch.x86_64`, `$mach.build.arch == $mach.arch.aarch64` nor `$mach.build.arch == $mach.arch.riscv64 \|\| $mach.build.arch == $mach.arch.riscv32` |  |

