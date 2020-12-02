import asyncio
import time
import base64
from collections import namedtuple
from aiohttp import ClientResponseError

from salvo.util import resolve

import molotov
from molotov.run import run
from molotov import util, api


@molotov.setup()
async def init_worker(worker_num, args):
    headers = {}

    content_type = molotov.get_var("content_type")
    if content_type:
        headers["Content-Type"] = content_type

    auth = molotov.get_var("auth")
    if auth is not None:
        basic = base64.b64encode(auth.encode())
        headers["Authorization"] = "Basic %s" % basic.decode()

    return {"headers": headers}


@molotov.scenario()
async def http_test(session):
    url = molotov.get_var("url")
    res = molotov.get_var("results")
    meth = molotov.get_var("method")

    options = {}
    pre_hook = molotov.get_var("pre_hook")
    if pre_hook is not None:
        meth, url, options = pre_hook(meth, url, options)

    post_hook = molotov.get_var("post_hook")
    data = molotov.get_var("data")
    if data:
        if callable(data):
            options["data"] = data(meth, url, options)
        else:
            options["data"] = data

    meth = getattr(session, meth.lower())
    start = time.time()
    try:
        # XXX we should implement raise_for_status globally in
        # the session in Molotov
        async with meth(url, raise_for_status=True, **options) as resp:
            if post_hook is not None:
                resp = await post_hook(resp)
            res.incr(resp.status, time.time() - start)
    except ClientResponseError as exc:
        res.incr(exc.status, time.time() - start)
        res.errors[exc.status] += 1
        if exc.message not in res.errors_desc:
            res.errors_desc[exc.message] = exc


def run_test(url, results, salvoargs):
    args = namedtuple("args", "")
    args.force_shutdown = False
    args.ramp_up = 0.0
    args.verbose = salvoargs.verbose
    args.quiet = salvoargs.quiet
    args.exception = False
    args.processes = 1
    args.debug = False
    args.workers = salvoargs.concurrency
    args.console = True
    args.statsd = False
    args.single_mode = None
    if salvoargs.duration:
        args.duration = salvoargs.duration
        args.max_runs = None
    else:
        args.duration = 9999
        args.max_runs = salvoargs.requests
    args.delay = 0.0
    args.sizing = False
    args.sizing_tolerance = 0.0
    args.console_update = 0.1
    args.use_extension = []
    args.fail = None
    args.force_reconnection = False
    args.scenario = __file__
    args.disable_dns_resolve = False
    args.single_run = False

    molotov.set_var("method", salvoargs.method)
    molotov.set_var("url", url)
    molotov.set_var("results", results)
    molotov.set_var("auth", salvoargs.auth)
    molotov.set_var("content_type", salvoargs.content_type)

    data = salvoargs.data
    if data and data.startswith("py:"):
        data = resolve(data.split(":")[1])
    molotov.set_var("data", data)

    if salvoargs.pre_hook is not None:
        molotov.set_var("pre_hook", resolve(salvoargs.pre_hook))
    else:
        molotov.set_var("pre_hook", None)

    if salvoargs.post_hook is not None:
        post_hook = resolve(salvoargs.post_hook)
        if not asyncio.iscoroutinefunction(post_hook):
            raise Exception("The post hook needs to be a coroutine")
        molotov.set_var("post_hook", post_hook)
    else:
        molotov.set_var("post_hook", None)

    class Stream:
        def __init__(self):
            self.buffer = []

        def write(self, msg):
            self.buffer.append(msg)

        def flush(self):
            pass

    # this module is going to be loaded by molotov,
    # so we need to clear up its internal state
    # XXX we should have a better way to do this
    util._STOP = False
    util._STOP_WHY = []
    util._TIMER = None
    api._SCENARIO.clear()
    api._FIXTURES.clear()

    stream = Stream()
    res = run(args, stream=stream)

    if res["SETUP_FAILED"] > 0 or res["SESSION_SETUP_FAILED"] > 0:
        print("Setup failed. read the Molotov session below to get the error")
        print("".join(stream.buffer))

    return res
