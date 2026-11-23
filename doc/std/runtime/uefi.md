[std](../README.md) / [runtime](README.md) / **uefi**

# std.runtime.uefi

uefi program entrypoint

provides `efi_main`, the entry mink's uefi rows name for the image. the firmware loads the
image where it chooses, applies its base relocations, and calls the entry with the image's
handle and the system table, in the target's own convention (win64 on x86_64, aapcs64win
on aarch64, which calls the firmware as AAPCS64 does), so the entry is ordinary mach code. the
firmware has already given it a stack, its `.bss` zeroed and floating point enabled
(UEFI specification 2.10, 2.3.4 and 2.3.6). this entrypoint:
  1. keeps the image handle and the system table, which `image_handle` and `system_table`
     return from then on
  2. calls user-supplied `main(0, nil)`, as the firmware passes no arguments on the call
     (an application reads its load options through the loaded image protocol)
  3. returns main's result to the firmware as the image's status, so 0 is EFI_SUCCESS.
     the firmware takes a return from the entry as a call to Exit with that status

user code must define:
  #[symbol("main")]
  fun main(argc: i64, argv: **u8) i64 { ... }

Source: [`src/runtime/uefi.mach`](../../../src/runtime/uefi.mach)

| Functions | |
| :--- | :--- |
| [`efi_main`](#efi_main) | the uefi entry: keep the firmware's handle and table, then run main |
| [`image_handle`](#image_handle) | the handle the firmware passed for this image |
| [`system_table`](#system_table) | the system table the firmware passed, through which a program reaches the console and the boot and runtime services |

---

## Functions

### efi_main

```mach
#[symbol("efi_main")]
pub fun efi_main(handle: ptr, system: *SystemTable) Status
```

the uefi entry: keep the firmware's handle and table, then run main

| Parameter | |
| :--- | :--- |
| `handle` | the handle of this image |
| `system` | the system table |
| **returns** | main's return value as the image's status |

### image_handle

```mach
pub fun image_handle() ptr
```

the handle the firmware passed for this image

### system_table

```mach
pub fun system_table() *SystemTable
```

the system table the firmware passed, through which a program reaches the console and the
boot and runtime services

