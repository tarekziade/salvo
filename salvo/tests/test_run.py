from unittest.mock import patch
import sys
import io
import pytest

from salvo.util import raise_response_error
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


def get_salvo_res(*args):
    return _test(*args)[-2]


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


def test_header():
    assert_code(0, "--header", "blah:foo", "http://localhost:8888")


def test_quiet_and_verbose():
    assert_code(1, "--quiet", "--verbose", "http://localhost:8888")


def test_single_hit_main():
    res = get_molotov_res("http://localhost:8888", "-n", "2")
    assert res["OK"] == 2, res


def test_duration():
    res = get_molotov_res("http://localhost:8888", "-d", "1")
    assert res["OK"] > 1, res


def test_errors():
    res = get_salvo_res("http://localhost:8888/error", "-n", "2")
    assert len(res.status_code_counter[500]) == 2, res


def test_errors_json():
    res = get_salvo_res("http://localhost:8888/error", "-n", "2", "--json")
    assert len(res.status_code_counter[500]) == 2, res


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


async def post_hook_raise(resp):
    raise_response_error(resp, 500, "BAM")


def test_post_hook_raise():

    testargs = [
        "http://localhost:8888",
        "-n",
        "1",
        "--post-hook",
        "salvo.tests.test_run.post_hook_raise",
    ]
    res = get_salvo_res(*testargs)
    assert len(res.status_code_counter[500]) == 1, res


async def hook_fail(*args):
    raise Exception("Hook fail")


def test_post_hook_fail():
    testargs = [
        "http://localhost:8888",
        "-n",
        "10",
        "--post-hook",
        "salvo.tests.test_run.hook_fail",
    ]
    res = get_molotov_res(*testargs)
    assert res["FAILED"] == 10


def hook_sync(*args):
    pass


def test_post_hook_not_async():
    testargs = [
        "http://localhost:8888",
        "-n",
        "10",
        "--post-hook",
        "salvo.tests.test_run.hook_sync",
    ]
    with pytest.raises(Exception):
        get_molotov_res(*testargs)


def test_auth():
    res = get_molotov_res("http://localhost:8888", "--auth", "user:password", "-n", "2")
    assert res["OK"] == 2, res


def get_data(method, url, args):
    return "DATA"


def test_data_callable():
    res = get_molotov_res(
        "http://localhost:8888",
        "-m",
        "POST",
        "-D",
        "py:salvo.tests.test_run.get_data",
        "-n",
        "2",
    )
    assert res["OK"] == 2, res


def test_data_not_callable():
    res = get_molotov_res(
        "http://localhost:8888",
        "-m",
        "POST",
        "-D",
        "DATA",
        "-n",
        "2",
    )
    assert res["OK"] == 2, res
