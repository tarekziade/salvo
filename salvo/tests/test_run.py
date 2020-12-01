from unittest.mock import patch
import sys
import io

from salvo.run import main
from salvo.tests.support import coserver, dedicatedloop
from salvo import __version__


@dedicatedloop
def _test(*args):
    code = 0
    testargs = [sys.executable] + list(args)
    main_res = molotov_res = None

    with patch("sys.stdout", new_callable=io.StringIO) as stdout, patch.object(
        sys, "argv", testargs
    ), coserver():
        try:
            main_res, molotov_res = main()
        except SystemExit as e:
            code = e.code

        stdout.seek(0)
        stdout = stdout.read().strip()

    return code, stdout, main_res, molotov_res


def assert_code(expected, *args):
    assert _test(*args)[0] == expected


def assert_stdout(expected, *args):
    assert _test(*args)[1] == expected


def get_molotov_res(*args):
    return _test(*args)[-1]


def test_display_version():
    assert_stdout(__version__, "--version")


def test_no_url():
    assert_code(1)


def test_data_but_wrong_verb():
    assert_code(1, "-D", "OK", "http://localhost:8888")


def test_malformed_header():
    assert_code(1, "--header", "blah", "http://localhost:8888")


def test_quiet_and_verbose():
    assert_code(1, "--quiet", "--verbose", "http://localhost:8888")


def test_single_hit_main():
    res = get_molotov_res("http://localhost:8888", "-n", "2")
    assert res["OK"] == 2, res


_CALLS = []


def pre_hook(meth, url, options):
    _CALLS.append(["PRE", meth, url, options])
    return meth, url, options


# XXX check that it's a coroutine
# and make a test to control
async def post_hook(resp):
    _CALLS.append(["POST", resp])
    return resp


def test_hooks():

    testargs = [
        "http://localhost:8888",
        "-n",
        "10",
        "--pre-hook",
        "salvo.tests.test_run.pre_hook",
        "--post-hook",
        "salvo.tests.test_run.post_hook",
        "--verbose",
    ]
    get_molotov_res(*testargs)
    assert len(_CALLS) == 20
