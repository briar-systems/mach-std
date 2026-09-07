import array
import copy
import fcntl
import json
import os
import pathlib
import select
import subprocess
import sys
import termios
import time


def write(fd, data):
    assert os.write(fd, data) == len(data)


def queued(fd):
    count = array.array("i", [0])
    fcntl.ioctl(fd, termios.FIONREAD, count, True)
    return count[0]


def wait_queued(fd, expected):
    deadline = time.monotonic() + 10
    while queued(fd) != expected:
        if time.monotonic() >= deadline:
            raise AssertionError(f"input count {queued(fd)}, expected {expected}")
        time.sleep(0.001)


def line(child, expected):
    data = b""
    deadline = time.monotonic() + 10
    while not data.endswith(b"\n"):
        left = deadline - time.monotonic()
        if left <= 0 or not select.select([child.stdout], [], [], left)[0]:
            raise AssertionError(f"missing phase {expected!r}, child={child.poll()}")
        byte = os.read(child.stdout.fileno(), 1)
        if not byte:
            child.wait(timeout=10)
            raise AssertionError(f"EOF awaiting {expected!r}, child={child.returncode}")
        data += byte
    assert data == expected, (data, expected)


def run(executable, layout, native_errors):
    actual = subprocess.check_output([executable, "layout"], timeout=10)
    assert actual == layout, (actual, layout)
    refusal = subprocess.run([executable, "nonterminal"], stdin=subprocess.DEVNULL,
                             capture_output=True, timeout=10)
    assert refusal.returncode == 0 and refusal.stdout == native_errors, refusal
    master, slave = os.openpty()
    control_read, control_write = os.pipe()
    child = None
    try:
        baseline = termios.tcgetattr(slave)
        baseline[1] |= termios.OPOST | termios.ONLCR
        baseline[3] |= termios.ICANON | termios.ECHO
        baseline[6][termios.VMIN] = b"\x01"
        baseline[6][termios.VTIME] = b"\x00"
        termios.tcsetattr(slave, termios.TCSANOW, baseline)
        baseline = termios.tcgetattr(slave)
        write(master, b"before\n")
        wait_queued(slave, 7)
        echo = b""
        while len(echo) < 8:
            assert select.select([master], [], [], 10)[0], "missing initial echo"
            echo += os.read(master, 8 - len(echo))
        assert echo == b"before\r\n", echo
        child = subprocess.Popen([executable, "pty", str(control_read)], stdin=slave,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 pass_fds=(control_read,))
        os.close(control_read)
        control_read = -1
        line(child, b"raw\n")
        raw = termios.tcgetattr(slave)
        expected = copy.deepcopy(baseline)
        expected[3] &= ~(termios.ICANON | termios.ECHO)
        expected[6][termios.VMIN] = 0
        expected[6][termios.VTIME] = 0
        assert raw == expected, (raw, expected)
        assert queued(slave) == 0
        write(master, b"A")
        wait_queued(slave, 1)
        write(control_write, b"a")
        line(child, b"empty\n")
        write(master, b"discard")
        wait_queued(slave, 7)
        write(control_write, b"f")
        line(child, b"flushed\n")
        assert queued(slave) == 0
        write(master, b"Z")
        wait_queued(slave, 1)
        write(control_write, b"z")
        line(child, b"post\n")
        write(master, b"restore-discard\n")
        wait_queued(slave, 16)
        write(control_write, b"r")
        line(child, b"restored\n")
        restored = termios.tcgetattr(slave)
        assert queued(slave) == 0, "restored input was not flushed"
        assert restored == baseline, ("settings were not restored", restored, baseline)
        write(control_write, b"q")
        out, err = child.communicate(timeout=10)
        assert child.returncode == 0 and not out and not err, (child.returncode, out, err)
        return {"executable": executable, "layout": actual.decode().strip(),
                "nonterminal": True, "native_errors": native_errors.decode().strip(),
                "raw": True, "poll": True,
                "flush": True, "post_flush_input": True, "restored": True}
    finally:
        if child is not None and child.poll() is None:
            child.kill()
            child.wait(timeout=10)
        if control_read >= 0:
            os.close(control_read)
        os.close(control_write)
        os.close(master)
        os.close(slave)


if __name__ == "__main__":
    assert sys.platform == "darwin", "the terminal probe requires native Darwin"
    layout = subprocess.check_output([sys.argv[2]], timeout=10)
    native = subprocess.run([sys.argv[2], "nonterminal"], stdin=subprocess.DEVNULL,
                            capture_output=True, timeout=10)
    assert native.returncode == 0, native
    print(json.dumps(run(str(pathlib.Path(sys.argv[1]).resolve()), layout, native.stdout), sort_keys=True))
