Salvo
=====

This is the replacement for https://github.com/tarekziade/boom

**Salvo** is a simple command line tool to send some load to an HTTP(S)
endpoint.

Salvo is a script you can use to quickly smoke-test your
web app deployment. If you need a more complex tool,
I'd suggest looking at `Molotov <http://molotov.readthedocs.io>`_

Salvo was specifically written to replace my Apache Bench (ab) usage.
Salvo is based on Molotov, which uses Python 3 asyncio & aiohttp.


Installation
============

Salvo requires Python 3.6+ and **Molotov**, which gets installed as a
dependency.

Just do::

    $ pip install salvo


Basic usage
===========

Basic usage example: 100 queries with a maximum concurrency of 10 users::

    % bin/salvo http://localhost:80 -c 10 -n 100
    -------- Server info --------

    Server Software: nginx/1.18.0
    Host: localhost

    -------- Running 100 queries - concurrency 10 --------

    [================================================================>.] 99%

    -------- Results --------

    Successful calls    		1000
    Total time          		16.0587 s
    Average             		0.0161 s
    Fastest             		0.0036 s
    Slowest             		0.2524 s
    Amplitude           		0.2488 s
    Standard deviation  		0.011326
    Requests Per Second 		62.27
    Requests Per Minute 		3736.29

    -------- Status codes --------
    Code 200          		1000 times.


Salvo has more options::

    $ salvo --help
    usage: salvo [-h] [--version] [-v] [-m {GET,POST,DELETE,PUT,HEAD,OPTIONS}]
                 [--content-type CONTENT_TYPE] [-D DATA] [-c CONCURRENCY] [-a AUTH]
                 [--header HEADER] [--pre-hook PRE_HOOK] [--post-hook POST_HOOK]
                 [--json-output] [-q] [-n REQUESTS | -d DURATION]
                 [url]

    Simple HTTP Load runner based on Molotov.

    positional arguments:
    url                   URL to hit

    optional arguments:
    -h, --help            show this help message and exit
    --version             Displays version and exits.
    -v, --verbose         Verbosity level. -v will display tracebacks. -vv requests and responses.
    -m {GET,POST,DELETE,PUT,HEAD,OPTIONS}, --method {GET,POST,DELETE,PUT,HEAD,OPTIONS}
                            HTTP Method
    --content-type CONTENT_TYPE
                            Content-Type
    -D DATA, --data DATA  Data. Prefixed by "py:" to point a python callable.
    -c CONCURRENCY, --concurrency CONCURRENCY
                            Concurrency
    -a AUTH, --auth AUTH  Basic authentication user:password
    --header HEADER       Custom header. name:value
    --pre-hook PRE_HOOK   Python module path (eg: mymodule.pre_hook) to a
                          callable which will be executed before doing a request for example:
                          pre_hook(method, url, options). It must return a tuple of parameters given
                          in function definition
    --post-hook POST_HOOK
                            Python module path (eg: mymodule.post_hook) to a
                            callable which will be executed after a request is
                            done for example: eg. post_hook(response). It must
                            return a given response parameter or raise an
                            `RequestException` for failed request.
    --json-output         Prints the results in JSON instead of the default format
    -q, --quiet           Don't display progress bar
    -n REQUESTS, --requests REQUESTS
                            Number of requests
    -d DURATION, --duration DURATION
                            Duration in seconds


Contribute
==========

Salvo is very simple and anyone familiar with Python can contribute.

If you are interested in this project, you are welcome to join the fun at
https://github.com/tarekziade/salvo

Make sure to add yourself to the contributors list if your PR gets merged. And
make sure it's in alphabetical order!
