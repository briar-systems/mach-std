import errno
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import darwin_fixture
from darwin_fixture import Edit, check, succeed


def line(output, mode):
    lines = output.decode().splitlines()
    check(len(lines) == 1, f"{mode} printed {lines!r}, expected one line")
    return lines[0]


def quiet(executable, mode):
    output = succeed([executable, mode], f"socket {mode}")
    check(output == b"", f"{mode} printed {output!r}, expected nothing")
    return True


SHARED = "src/system/os/darwin/shared.mach"

# the flag configuration answers EIO where it sets O_NONBLOCK
REFUSE = Edit(SHARED,
              "        val changed: i64 = set_file_flags(fd, current::i32 | O_NONBLOCK);\n",
              "        val changed: i64 = EIO;\n")

# each cleanup close sits in the creation or the accept path that owns the descriptor
CREATE = "    val raw: i32 = ls.socket(domain, typ, protocol);\n"
ACCEPT = "    val raw: i32 = ls.accept(fd::i32, addr, addrlen);\n"
CLOSE = "    if (raw == -1) { ret ls.fail_errno(); }\n    val configured: i64 = configure_socket_flags(raw, nonblocking, non_inheritable);\n    if (configured < 0) {\n"


def leak(path):
    anchor = path + CLOSE + "        close(raw);\n"
    return Edit(SHARED, anchor, anchor.replace("        close(raw);\n", ""))


PEEK = Edit(SHARED,
            "    val peeked: i64 = ls.recvmsg(fd::i32, ?message, ls.MSG_PEEK);\n",
            "    val peeked: i64 = ls.recvmsg(fd::i32, ?message, 0);\n")


def controls(fixture, executable):
    # the refusal modes only pass against a std whose flag configuration fails, and fail against the honest build
    fixture.exits(executable, "create-refusal", 110, "create-refusal against the honest build")
    fixture.exits(executable, "accept-refusal", 44, "accept-refusal against the honest build")
    refused = fixture.build("socket", fixture.mutate("refuse", REFUSE))
    fixture.exits(refused, "create-refusal", 0, "create-refusal")
    fixture.exits(refused, "accept-refusal", 0, "accept-refusal")
    created = fixture.build("socket", fixture.mutate("leak-create", REFUSE, leak(CREATE)))
    fixture.exits(created, "create-refusal", 111, "create-refusal without the cleanup close")
    accepted = fixture.build("socket", fixture.mutate("leak-accept", REFUSE, leak(ACCEPT)))
    fixture.exits(accepted, "accept-refusal", 45, "accept-refusal without the cleanup close")
    peekless = fixture.build("socket", fixture.mutate("no-peek", PEEK))
    fixture.exits(peekless, "local-bytes", 133, "local-bytes without the peek")


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
    controls(fixture, executable)
    return results


if __name__ == "__main__":
    darwin_fixture.main(__file__, checks)
