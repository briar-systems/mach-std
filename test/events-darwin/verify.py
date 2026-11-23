import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import darwin_fixture
from darwin_fixture import check, succeed


def without_alignment(text):
    return re.sub(rb" alignment=\d+", b"", text)


def checks(fixture):
    # native.c's static asserts hold the SDK's kqueue and kevent signatures, constants and layout
    _, native = fixture.clang("native.c")
    native_layout = succeed([native, "layout"], "native.c layout")
    native_errors = succeed([native, "errors"], "native.c errors")
    results = {"native events": succeed([native, "events"], "native.c events").decode().strip()}
    executable = fixture.build("events")
    # mach's kevent record is aligned more strictly than apple's packed one, so only extent and offsets compare
    layout = succeed([executable, "layout"], "events layout")
    check(without_alignment(layout) == without_alignment(native_layout),
          f"layout {layout!r}, the SDK says {native_layout!r}")
    results["layout"] = layout.decode().strip()
    errors = succeed([executable, "errors"], "events errors")
    check(errors == native_errors, f"errors reports {errors!r}, native.c reports {native_errors!r}")
    results["errors"] = errors.decode().strip()
    for mode in ("nil", "events"):
        results[mode] = succeed([executable, mode], f"events {mode}").decode().strip()
    # the worker wakes the blocked poll once it reads 'g' from stdin
    results["handshake"] = succeed([executable, "handshake"], "events handshake", input=b"g").decode().strip()
    return results


if __name__ == "__main__":
    darwin_fixture.main(__file__, checks)
