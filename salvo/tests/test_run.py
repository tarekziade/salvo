from collections import namedtuple
from salvo.run import load
from salvo.tests.support import coserver


def test_single_hit():
    args = namedtuple("Arguments", [])
    args.quiet = False
    args.method = "GET"
    args.headers = {}
    args.requests = 1
    args.concurrency = 1
    args.verbose = True
    args.duration = 9999
    args.auth = None
    args.content_type = "text/plain"
    args.data = None
    args.pre_hook = args.post_hook = None

    with coserver():
        res, molotov_res = load("http://localhost:8888", args)

    assert molotov_res["OK"] == 1
