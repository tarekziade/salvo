import time
import base64
from collections import namedtuple
import molotov
from molotov.run import run


@molotov.setup()
async def init_worker(worker_num, args):
    auth = molotov.get_var('auth')
    if auth is None:
        return {}
    basic = base64.b64encode(auth.encode())
    headers = {'Authorization': 'Basic %s' % basic.decode()}
    return {'headers': headers}


@molotov.scenario()
async def http_test(session):
    url = molotov.get_var('url')
    res = molotov.get_var('results')
    start = time.time()

    async with session.get(url) as resp:
        res.incr(resp.status, time.time() - start)


def run_test(url, results, pulse_args):
    args = namedtuple('args', '')
    args.force_shutdown = False
    args.ramp_up = .0
    args.verbose = 0
    args.quiet = True
    args.exception = True
    args.processes = 1
    args.debug = True
    args.workers = pulse_args.concurrency
    args.console = True
    args.statsd = False
    args.single_mode = None
    args.max_runs = pulse_args.requests
    if pulse_args.duration:
        args.duration = pulse_args.duration
    else:
        args.duration = 9999
    args.delay = .0
    args.sizing = False
    args.sizing_tolerance = .0
    args.console_update = 0
    args.use_extension = []
    args.fail = None
    args.force_reconnection = False
    args.scenario = 'break_.scenario'
    molotov.set_var('url', url)
    molotov.set_var('results', results)
    molotov.set_var('auth', pulse_args.auth)
    run(args)
