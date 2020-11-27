from unittest.mock import patch
import sys

from salvo.run import main
from salvo.tests.support import coserver, dedicatedloop


@dedicatedloop
def test_single_hit_main():

    testargs = [sys.executable, "http://localhost:8888", "-n", "2"]
    with patch.object(sys, "argv", testargs), coserver():
        res, molotov_res = main()

    assert molotov_res["OK"] == 2, molotov_res
