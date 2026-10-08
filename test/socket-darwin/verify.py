import errno
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import darwin_fixture
from darwin_fixture import check, succeed


def line(output, mode):
    lines = output.decode().splitlines()
    check(len(lines) == 1, f"{mode} printed {lines!r}, expected one line")
    return lines[0]


def quiet(executable, mode):
    output = succeed([executable, mode], f"socket {mode}")
    check(output == b"", f"{mode} printed {output!r}, expected nothing")
    return True


def checks(fixture):
    layout_object, layout = fixture.clang("layout.c")
    _, control = fixture.clang("control.c")
    executable = fixture.build("socket")
    results = {}

    native_layout = succeed([layout], "layout.c")
    mach_layout = succeed([executable, "layout"], "socket layout")
    check(mach_layout == native_layout, f"layout {mach_layout!r}, the SDK says {native_layout!r}")
    results["layout"] = native_layout.decode().strip()
    results["imports"] = fixture.imports("layout.c", layout_object, executable)

    results["errors"] = quiet(executable, "errors")

    option = line(succeed([layout, "option"], "layout.c option"), "layout.c option")
    check(re.fullmatch(r"keepalive=[1-9]\d* length=4", option), f"layout.c option printed {option!r}")
    stream = line(succeed([executable, "stream"], "socket stream"), "stream")
    check(stream == option, f"stream reports {stream!r}, the native option is {option!r}")
    results["stream"] = stream

    vectors = line(succeed([executable, "vectors"], "socket vectors"), "vectors")
    partial = re.fullmatch(r"partial=(\d+)", vectors)
    check(partial and 0 < int(partial[1]) < 65536, f"vectors printed {vectors!r}, expected a partial count")
    results["vectors"] = vectors

    native_control = line(succeed([control], "control.c"), "control.c")
    messages = line(succeed([executable, "messages"], "socket messages"), "messages")
    check(messages == native_control, f"messages reports {messages!r}, control.c reports {native_control!r}")
    results["messages"] = messages

    results["datagrams"] = quiet(executable, "datagrams")

    expected = {
        "local-bytes": f"local-bytes prefix=3 refusals=8 peek-fault={-errno.EFAULT} rights-released=32",
        "local-async": f"local-async refusal={-errno.ENOTSUP} bytes=0 rights-released=16",
        "internet-async-capability": f"internet-async local-refused={-errno.ENOTSUP} invalid={-errno.EBADF}",
    }
    for mode, want in expected.items():
        got = line(succeed([executable, mode], f"socket {mode}"), mode)
        check(got == want, f"{mode} printed {got!r}, expected {want!r}")
        results[mode] = got
    return results


if __name__ == "__main__":
    darwin_fixture.main(__file__, checks)
