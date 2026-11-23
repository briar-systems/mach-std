import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import darwin_fixture
from darwin_fixture import check, succeed


def checks(fixture):
    # native.c's static asserts hold the SDK's getentropy signature and widths
    _, native = fixture.clang("native.c")
    native_smoke = succeed([native, "smoke"], "native.c smoke")
    native_errors = succeed([native, "errors"], "native.c errors")
    executable = fixture.build("entropy")
    results = {}
    for mode, oracle in (("smoke", native_smoke), ("errors", native_errors)):
        got = succeed([executable, mode], f"entropy {mode}")
        check(got == oracle, f"{mode} reports {got!r}, native.c reports {oracle!r}")
        results[mode] = got.decode().strip()
    return results


if __name__ == "__main__":
    darwin_fixture.main(__file__, checks)
