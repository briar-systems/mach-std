import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import darwin_fixture
from darwin_fixture import succeed


def checks(fixture):
    # native.c's static asserts hold the SDK's dirent layout and the cursor's signatures
    _, native = fixture.clang("native.c")
    results = {}
    for mode in ("layout", "errors"):
        results["native " + mode] = succeed([native, mode], f"native.c {mode}", cwd=fixture.work).decode().strip()
    executable = fixture.build("directory")
    # each mode holds its own expected values and exits nonzero on a mismatch
    for mode in ("layout", "errors", "borrowed"):
        results[mode] = succeed([executable, mode], f"directory {mode}", cwd=fixture.work).decode().strip()
    return results


if __name__ == "__main__":
    darwin_fixture.main(__file__, checks)
