[std](../README.md) / **system**

# std.system

| Module | |
| :--- | :--- |
| [`capability`](capability.md) | which operating system capabilities the build target provides |
| [`cpu`](cpu.md) | the running processor's instruction-set extensions |
| [`dit`](dit.md) | the processor's data-independent-timing mode (PSTATE.DIT) on aarch64 |
| [`file_identity`](file_identity.md) | observational identity within one host and its current mounted namespace |
| [`os`](os.md) | the OS contract: a small set of primitives, one implementation per OS |
| [`panic`](panic.md) | low-level panic: write message to stderr and terminate, or on bare metal hand it to the program's sink and park the core |
| [`timing`](timing.md) | the data-independent-timing mode the processor provides, as a run-time query |
| [`uefi`](uefi.md) | the uefi firmware's tables, as a program finds them from the system table its entry is passed |

| Directory | |
| :--- | :--- |
| [`cpu/`](cpu/README.md) | the running processor's instruction-set extensions |
| [`os/`](os/README.md) | the OS contract: a small set of primitives, one implementation per OS |

