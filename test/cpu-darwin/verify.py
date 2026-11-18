import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import darwin_fixture
from darwin_fixture import check, succeed


def checks(fixture):
    # native.c's static asserts hold the SDK's sysctlbyname signature and widths
    _, native = fixture.clang("native.c")
    results = {"native observe": succeed([native, "observe"], "native.c observe").decode().strip()}
    native_errors = succeed([native, "errors"], "native.c errors")
    executable = fixture.build("cpu")
    results["observe"] = succeed([executable, "observe"], "cpu observe").decode().strip()
    # the direct binding fails with exactly the SDK's result and errno
    errors = succeed([executable, "errors"], "cpu errors")
    check(errors == native_errors, f"errors reports {errors!r}, native.c reports {native_errors!r}")
    results["errors"] = errors.decode().strip()
    return results


if __name__ == "__main__":
    darwin_fixture.main(__file__, checks)
