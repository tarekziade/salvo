import time
import base64
from collections import namedtuple

from break_.util import resolve

import molotov
from molotov.run import run


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

    data = molotov.get_var("data")
    if data and data.startswith("py:"):
        method = molotov.get_var("method")
        url = molotov.get_var("url")
        func = resolve(data.split(":")[1])
        molotov.set_var("data", func(method, url, args))

    return {"headers": headers}


@molotov.scenario()
async def http_test(session):
    url = molotov.get_var("url")
    res = molotov.get_var("results")
    meth = molotov.get_var("method")

    options = {}
    data = molotov.get_var("data")
    if data:
        options["data"] = data

    pre_hook = molotov.get_var("pre_hook")
    if pre_hook is not None:
        meth, url, options = pre_hook(meth, url, options)

    post_hook = molotov.get_var("post_hook")
    meth = getattr(session, meth.lower())
    start = time.time()
    try:
        async with meth(url, **options) as resp:
            if post_hook is not None:
                resp = await post_hook(resp)
            res.incr(resp.status, time.time() - start)
    except Exception as exc:
        res.errors[exc.errno] += 1
        if exc.errno not in res.errors_desc:
            res.errors_desc[exc.errno] = exc


def run_test(url, results, break_args):
    args = namedtuple("args", "")
    args.force_shutdown = False
    args.ramp_up = 0.0
    args.verbose = break_args.verbose
    args.quiet = break_args.quiet
    args.exception = False
    args.processes = 1
    args.debug = False
    args.workers = break_args.concurrency
    args.console = True
    args.statsd = False
    args.single_mode = None
    args.max_runs = break_args.requests
    if break_args.duration:
        args.duration = break_args.duration
    else:
        args.duration = 9999
    args.delay = 0.0
    args.sizing = False
    args.sizing_tolerance = 0.0
    args.console_update = 0.1
    args.use_extension = []
    args.fail = None
    args.force_reconnection = False
    args.scenario = "break_.scenario"
    args.disable_dns_resolve = False
    args.single_run = False

    molotov.set_var("method", break_args.method)
    molotov.set_var("url", url)
    molotov.set_var("results", results)
    molotov.set_var("auth", break_args.auth)
    molotov.set_var("content_type", break_args.content_type)
    molotov.set_var("data", break_args.data)
    if break_args.pre_hook is not None:
        molotov.set_var("pre_hook", resolve(break_args.pre_hook))
    if break_args.post_hook is not None:
        molotov.set_var("post_hook", resolve(break_args.post_hook))

    class Stream:
        def __init__(self):
            self.buffer = []

        def write(self, msg):
            self.buffer.append(msg)

        def flush(self):
            pass

    stream = Stream()
    res = run(args, stream=stream)

    if res["SETUP_FAILED"] > 0 or res["SESSION_SETUP_FAILED"] > 0:
        print("Setup failed. read the Molotov session below to get the error")
        print("".join(stream.buffer))

    return res
