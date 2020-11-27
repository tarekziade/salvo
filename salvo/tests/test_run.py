from unittest.mock import patch
import sys
import io

from salvo.run import main
from salvo.tests.support import coserver, dedicatedloop
from salvo import __version__


@dedicatedloop
@patch("sys.stdout", new_callable=io.StringIO)
def test_display_version(stdout):

    testargs = [sys.executable, "--version"]
    with patch.object(sys, "argv", testargs), coserver():
        try:
            main()
        except SystemExit:
            pass
        else:
            raise AssertionError()

    stdout.seek(0)
    res = stdout.read().strip()
    assert res == __version__


@dedicatedloop
@patch("sys.stdout", new_callable=io.StringIO)
def test_no_url(stdout):
    testargs = [sys.executable]
    with patch.object(sys, "argv", testargs):
        try:
            main()
        except SystemExit as e:
            assert e.code == 1
        else:
            raise AssertionError()


@dedicatedloop
@patch("sys.stdout", new_callable=io.StringIO)
def test_data_but_wrong_verb(stdout):
    testargs = [sys.executable, "-D", "OK", "http://localhost:8888"]
    with patch.object(sys, "argv", testargs):
        try:
            main()
        except SystemExit as e:
            assert e.code == 1
        else:
            raise AssertionError()


@dedicatedloop
@patch("sys.stdout", new_callable=io.StringIO)
def test_malformed_header(stdout):
    testargs = [sys.executable, "--header", "blah", "http://localhost:8888"]
    with patch.object(sys, "argv", testargs):
        try:
            main()
        except SystemExit as e:
            assert e.code == 1
        else:
            raise AssertionError()


@dedicatedloop
@patch("sys.stdout", new_callable=io.StringIO)
def test_quiet_and_verbose(stdout):
    testargs = [sys.executable, "--quiet", "--verbose", "http://localhost:8888"]
    with patch.object(sys, "argv", testargs):
        try:
            main()
        except SystemExit as e:
            assert e.code == 1
        else:
            raise AssertionError()


@dedicatedloop
def test_single_hit_main():

    testargs = [sys.executable, "http://localhost:8888", "-n", "2"]
    with patch.object(sys, "argv", testargs), coserver():
        res, molotov_res = main()

    assert molotov_res["OK"] == 2, molotov_res
