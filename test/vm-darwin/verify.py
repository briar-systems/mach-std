import os
import signal
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import darwin_fixture
from darwin_fixture import Edit, check, run, succeed

# the mapping probe's file offset, past 32 bits so a truncated offset maps byte zero
FAR = 0x140000000


SHARED = "src/system/os/darwin/shared.mach"

# the heap reservation fails, and separately the protection that extends it fails
RESERVE = Edit(SHARED,
               "    val mapped: ptr = ls.mmap(nil, os_shared.HEAP_RESERVE, PROT_NONE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);\n",
               "    val mapped: ptr = ((-1)::isize::usize)::ptr;\n")
PROTECT = Edit(SHARED,
               "    val result: i32   = ls.mprotect(_brk_end::ptr, size, PROT_READ | PROT_WRITE);\n",
               "    val result: i32   = -1;\n")


def controls(fixture, executable):
    # the refusal modes only pass against a std whose heap fails, and fail against the honest build
    fixture.exits(executable, "heap-refused", 55, "heap-refused against the honest build")
    fixture.exits(executable, "heap-refusal", 51, "heap-refusal against the honest build")
    reserve = fixture.build("vm", fixture.mutate("reserve", RESERVE))
    fixture.exits(reserve, "heap-refused", 0, "heap-refused")
    protect = fixture.build("vm", fixture.mutate("protect", PROTECT))
    fixture.exits(protect, "heap-refusal", 0, "heap-refusal")


def denied(command, label):
    result = run(command)
    check(result.stdout == b"fault-ready\n", f"{label} printed {result.stdout!r} before the fault, expected the readiness marker")
    check(result.returncode < 0, f"{label} exited {result.returncode} instead of dying by a fault signal")
    return -result.returncode


def mapping(fixture, executable):
    page = os.sysconf("SC_PAGE_SIZE")
    descriptor, path = tempfile.mkstemp(prefix="mapping-", dir=fixture.work)
    try:
        os.ftruncate(descriptor, FAR + page)
        check(os.pwrite(descriptor, b"A", 0) == 1 and os.pwrite(descriptor, b"B", FAR) == 1,
              "writing the sparse mapping file failed")
        os.fsync(descriptor)
        succeed([executable, "mapping", path], "vm mapping")
        check(os.pread(descriptor, 1, 0) == b"A", "the mapping wrote byte zero, so its offset was truncated")
        check(os.pread(descriptor, 1, FAR) == b"Z", "the mapped write did not reach the file")
    finally:
        os.close(descriptor)
        os.unlink(path)
    return True


def checks(fixture):
    native_object, native = fixture.clang("native.c")
    results = {}
    native_layout = succeed([native, "layout"], "native.c layout")
    native_errors = succeed([native, "errors"], "native.c errors")
    native_access = succeed([native, "access"], "native.c access")
    results["released_oracle"] = succeed([native, "released"], "native.c released").decode().strip()
    fault = denied([native, "denied"], "native.c denied")
    check(fault in (signal.SIGSEGV, signal.SIGBUS), f"native.c denied died by signal {fault}, not a fault")

    executable = fixture.build("vm")
    results["imports"] = fixture.imports("native.c", native_object, executable)
    layout = succeed([executable, "layout"], "vm layout")
    check(layout == native_layout, f"layout {layout!r}, the SDK says {native_layout!r}")
    results["layout"] = layout.decode().strip()
    for mode, oracle in (("errors", native_errors), ("access", native_access)):
        got = succeed([executable, mode], f"vm {mode}")
        check(got == oracle, f"{mode} reports {got!r}, native.c reports {oracle!r}")
        results[mode] = got.decode().strip()
    for mode in ("basic", "heap", "adapters"):
        got = succeed([executable, mode], f"vm {mode}")
        check(got == b"", f"{mode} printed {got!r}, expected nothing")
        results[mode] = True
    mach_fault = denied([executable, "denied"], "vm denied")
    check(mach_fault == fault, f"vm denied died by signal {mach_fault}, native.c by {fault}")
    results["denied"] = signal.Signals(fault).name
    results["mapping"] = mapping(fixture, executable)
    controls(fixture, executable)
    return results


if __name__ == "__main__":
    darwin_fixture.main(__file__, checks)
