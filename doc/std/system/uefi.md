[std](../README.md) / [system](README.md) / **uefi**

# std.system.uefi

the uefi firmware's tables, as a program finds them from the system table its entry is passed

Source: [`src/system/uefi.mach`](../../../src/system/uefi.mach)

| Type | | |
| :--- | :--- | :--- |
| [`Status`](#status) | `def` | a service's result: zero is success, and an error has the high bit set |
| [`TableHeader`](#tableheader) | `rec` | EFI_TABLE_HEADER, which begins every table |
| [`Guid`](#guid) | `rec` | EFI_GUID |
| [`ConfigurationTable`](#configurationtable) | `rec` | EFI_CONFIGURATION_TABLE |
| [`SystemTable`](#systemtable) | `rec` | EFI_SYSTEM_TABLE, passed to the image's entry |
| [`InputKey`](#inputkey) | `rec` | EFI_INPUT_KEY |
| [`SimpleTextInputProtocol`](#simpletextinputprotocol) | `rec` | EFI_SIMPLE_TEXT_INPUT_PROTOCOL |
| [`SimpleTextOutputMode`](#simpletextoutputmode) | `rec` | SIMPLE_TEXT_OUTPUT_MODE |
| [`SimpleTextOutputProtocol`](#simpletextoutputprotocol) | `rec` | EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL |
| [`Time`](#time) | `rec` | EFI_TIME |
| [`TimeCapabilities`](#timecapabilities) | `rec` | EFI_TIME_CAPABILITIES |
| [`MemoryDescriptor`](#memorydescriptor) | `rec` | EFI_MEMORY_DESCRIPTOR |
| [`RuntimeServices`](#runtimeservices) | `rec` | EFI_RUNTIME_SERVICES |
| [`BootServices`](#bootservices) | `rec` | EFI_BOOT_SERVICES |

| On `Status` | |
| :--- | :--- |
| [`SUCCESS`](#status) | |
| [`ERROR`](#status) | the bit every error status carries |
| [`ABORTED`](#status) | EFI_ABORTED, the operation was aborted |

| Constants | |
| :--- | :--- |
| [`RESET_COLD`](#constants) | EFI_RESET_TYPE, what RuntimeServices.reset_system does |
| [`RESET_WARM`](#constants), [`RESET_SHUTDOWN`](#constants), [`RESET_PLATFORM_SPECIFIC`](#constants) | |

---

## Status

```mach
pub def Status: u64
```

a service's result: zero is success, and an error has the high bit set

| Name | Value | |
| :--- | :--- | :--- |
| `SUCCESS` | `0` |  |
| `ERROR` | `0x8000_0000_0000_0000` | the bit every error status carries |
| `ABORTED` | `ERROR \| 21` | EFI_ABORTED, the operation was aborted |

## TableHeader

```mach
pub rec TableHeader {
    signature:   u64;
    revision:    u32;
    header_size: u32;
    crc32:       u32;
    reserved:    u32;
}
```

EFI_TABLE_HEADER, which begins every table

## Guid

```mach
pub rec Guid {
    data1: u32;
    data2: u16;
    data3: u16;
    data4: [8]u8;
}
```

EFI_GUID

## ConfigurationTable

```mach
pub rec ConfigurationTable {
    vendor_guid:  Guid;
    vendor_table: ptr;
}
```

EFI_CONFIGURATION_TABLE

## SystemTable

```mach
pub rec SystemTable {
    hdr:                     TableHeader;
    firmware_vendor:         *u16;
    firmware_revision:       u32;
    console_in_handle:       ptr;
    con_in:                  *SimpleTextInputProtocol;
    console_out_handle:      ptr;
    con_out:                 *SimpleTextOutputProtocol;
    standard_error_handle:   ptr;
    std_err:                 *SimpleTextOutputProtocol;
    runtime_services:        *RuntimeServices;
    boot_services:           *BootServices;
    number_of_table_entries: usize;
    configuration_table:     *ConfigurationTable;
}
```

EFI_SYSTEM_TABLE, passed to the image's entry

## InputKey

```mach
pub rec InputKey {
    scan_code:    u16;
    unicode_char: u16;
}
```

EFI_INPUT_KEY

## SimpleTextInputProtocol

```mach
pub rec SimpleTextInputProtocol {
    reset:           fun(*SimpleTextInputProtocol, u8) Status;
    read_key_stroke: fun(*SimpleTextInputProtocol, *InputKey) Status;
    wait_for_key:    ptr;
}
```

EFI_SIMPLE_TEXT_INPUT_PROTOCOL

## SimpleTextOutputMode

```mach
pub rec SimpleTextOutputMode {
    max_mode:       i32;
    mode:           i32;
    attribute:      i32;
    cursor_column:  i32;
    cursor_row:     i32;
    cursor_visible: u8;
}
```

SIMPLE_TEXT_OUTPUT_MODE

## SimpleTextOutputProtocol

```mach
pub rec SimpleTextOutputProtocol {
    reset:               fun(*SimpleTextOutputProtocol, u8) Status;
    output_string:       fun(*SimpleTextOutputProtocol, *u16) Status;
    test_string:         fun(*SimpleTextOutputProtocol, *u16) Status;
    query_mode:          fun(*SimpleTextOutputProtocol, usize, *usize, *usize) Status;
    set_mode:            fun(*SimpleTextOutputProtocol, usize) Status;
    set_attribute:       fun(*SimpleTextOutputProtocol, usize) Status;
    clear_screen:        fun(*SimpleTextOutputProtocol) Status;
    set_cursor_position: fun(*SimpleTextOutputProtocol, usize, usize) Status;
    enable_cursor:       fun(*SimpleTextOutputProtocol, u8) Status;
    mode:                *SimpleTextOutputMode;
}
```

EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL. a string is nul-terminated UCS-2

## Time

```mach
pub rec Time {
    year:       u16;
    month:      u8;
    day:        u8;
    hour:       u8;
    minute:     u8;
    second:     u8;
    pad1:       u8;
    nanosecond: u32;
    time_zone:  i16;
    daylight:   u8;
    pad2:       u8;
}
```

EFI_TIME

## TimeCapabilities

```mach
pub rec TimeCapabilities {
    resolution:   u32;
    accuracy:     u32;
    sets_to_zero: u8;
}
```

EFI_TIME_CAPABILITIES

## MemoryDescriptor

```mach
pub rec MemoryDescriptor {
    kind:            u32;
    physical_start:  u64;
    virtual_start:   u64;
    number_of_pages: u64;
    attribute:       u64;
}
```

EFI_MEMORY_DESCRIPTOR. a memory map's descriptors are DescriptorSize bytes apart, which may
exceed this record's size

## RuntimeServices

```mach
pub rec RuntimeServices {
    hdr:                           TableHeader;
    get_time:                      fun(*Time, *TimeCapabilities) Status;
    set_time:                      fun(*Time) Status;
    get_wakeup_time:               fun(*u8, *u8, *Time) Status;
    set_wakeup_time:               fun(u8, *Time) Status;
    set_virtual_address_map:       fun(usize, usize, u32, *MemoryDescriptor) Status;
    convert_pointer:               fun(usize, *ptr) Status;
    get_variable:                  fun(*u16, *Guid, *u32, *usize, ptr) Status;
    get_next_variable_name:        fun(*usize, *u16, *Guid) Status;
    set_variable:                  fun(*u16, *Guid, u32, usize, ptr) Status;
    get_next_high_monotonic_count: fun(*u32) Status;
    reset_system:                  fun(u32, Status, usize, ptr);
    update_capsule:                fun(*ptr, usize, u64) Status;
    query_capsule_capabilities:    fun(*ptr, usize, *u64, *u32) Status;
    query_variable_info:           fun(u32, *u64, *u64, *u64) Status;
}
```

EFI_RUNTIME_SERVICES

## BootServices

```mach
pub rec BootServices {
    hdr:                                    TableHeader;
    raise_tpl:                              fun(u64) u64;
    restore_tpl:                            fun(u64);
    allocate_pages:                         fun(u32, u32, usize, *u64) Status;
    free_pages:                             fun(u64, usize) Status;
    get_memory_map:                         fun(*usize, *MemoryDescriptor, *usize, *usize, *u32) Status;
    allocate_pool:                          fun(u32, usize, *ptr) Status;
    free_pool:                              fun(ptr) Status;
    create_event:                           fun(u32, u64, fun(ptr, ptr), ptr, *ptr) Status;
    set_timer:                              fun(ptr, u32, u64) Status;
    wait_for_event:                         fun(usize, *ptr, *usize) Status;
    signal_event:                           fun(ptr) Status;
    close_event:                            fun(ptr) Status;
    check_event:                            fun(ptr) Status;
    install_protocol_interface:             fun(*ptr, *Guid, u32, ptr) Status;
    reinstall_protocol_interface:           fun(ptr, *Guid, ptr, ptr) Status;
    uninstall_protocol_interface:           fun(ptr, *Guid, ptr) Status;
    handle_protocol:                        fun(ptr, *Guid, *ptr) Status;
    reserved:                               ptr;
    register_protocol_notify:               fun(*Guid, ptr, *ptr) Status;
    locate_handle:                          fun(u32, *Guid, ptr, *usize, *ptr) Status;
    locate_device_path:                     fun(*Guid, *ptr, *ptr) Status;
    install_configuration_table:            fun(*Guid, ptr) Status;
    load_image:                             fun(u8, ptr, ptr, ptr, usize, *ptr) Status;
    start_image:                            fun(ptr, *usize, **u16) Status;
    exit:                                   fun(ptr, Status, usize, *u16) Status;
    unload_image:                           fun(ptr) Status;
    exit_boot_services:                     fun(ptr, usize) Status;
    get_next_monotonic_count:               fun(*u64) Status;
    stall:                                  fun(usize) Status;
    set_watchdog_timer:                     fun(usize, u64, usize, *u16) Status;
    connect_controller:                     fun(ptr, *ptr, ptr, u8) Status;
    disconnect_controller:                  fun(ptr, ptr, ptr) Status;
    open_protocol:                          fun(ptr, *Guid, *ptr, ptr, ptr, u32) Status;
    close_protocol:                         fun(ptr, *Guid, ptr, ptr) Status;
    open_protocol_information:              fun(ptr, *Guid, *ptr, *usize) Status;
    protocols_per_handle:                   fun(ptr, ***Guid, *usize) Status;
    locate_handle_buffer:                   fun(u32, *Guid, ptr, *usize, **ptr) Status;
    locate_protocol:                        fun(*Guid, ptr, *ptr) Status;
    install_multiple_protocol_interfaces:   ptr;
    uninstall_multiple_protocol_interfaces: ptr;
    calculate_crc32:                        fun(ptr, usize, *u32) Status;
    copy_mem:                               fun(ptr, ptr, usize);
    set_mem:                                fun(ptr, usize, u8);
    create_event_ex:                        fun(u32, u64, fun(ptr, ptr), ptr, *Guid, *ptr) Status;
}
```

EFI_BOOT_SERVICES. the two multiple-interface services take a variable argument list, which
a mach function pointer does not spell, so they are `ptr`

## Constants

| Name | Type | Value | |
| :--- | :--- | :--- | :--- |
| `RESET_COLD` | `u32` | `0` | EFI_RESET_TYPE, what RuntimeServices.reset_system does |
| `RESET_WARM` | `u32` | `1` |  |
| `RESET_SHUTDOWN` | `u32` | `2` |  |
| `RESET_PLATFORM_SPECIFIC` | `u32` | `3` |  |

