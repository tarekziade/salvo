Break
=====

WORK IN PROGRESS. THIS IS NOT WORKING YET, DO NOT INSTALL

This is the replacement for https://github.com/tarekziade/boom


**Break** is a simple command line tool to send some load to a web app.


**Break** is a script you can use to quickly smoke-test your
web app deployment. If you need a more complex tool,
I'd suggest looking at `Molotov <http://molotov.readthedocs.io>`_

Break was specifically written to replace my Apache Bench (ab) usage,
to provide a few missing features and fix a few annoyances I had
with ab.

I have no special ambitions for this tool, and since I have not
found any tool like this in the Python-land, I wrote this one.

There are a lot of other tools out there, like Siege which
seems very popular.

However, Break is a good choice because it works on any platform
and is able to simulate thousands of users by using Molotov.


Installation
============

Break requires Python 3.5.x+ and **Molotov**, which gets installed as a dependency.

Just do::


    $ pip install break


Basic usage
===========

Basic usage example: 100 queries with a maximum concurrency of
10 users::

    $ break http://localhost:80 -c 10 -n 100
    Server Software: nginx/1.2.2
    Running 100 queries - concurrency: 10.
    Starting the load [===================================] Done

    -------- Results --------
    Successful calls        100
    Total time              0.3260 s
    Average                 0.0192 s
    Fastest                 0.0094 s
    Slowest                 0.0285 s
    Amplitude               0.0191 s
    RPS                     306



Break has more options::

    $ break --help
    usage: break [-h] [--version] [-m {GET,POST,DELETE,PUT,HEAD,OPTIONS}]
                [--content-type CONTENT_TYPE] [-D DATA] [-c CONCURRENCY] [-a AUTH]
                [--header HEADER] [--pre-hook PRE_HOOK] [--post-hook POST_HOOK]
                [--json-output] [-n REQUESTS | -d DURATION]
                [url]

    Simple HTTP Load runner.

    positional arguments:
      url                   URL to hit

    optional arguments:
      -h, --help            show this help message and exit
      --version             Displays version and exits.
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
                            callable which will be executed before doing a request
                            for example: pre_hook(method, url, options). It must
                            return a tupple of parameters given in function
                            definition
      --post-hook POST_HOOK
                            Python module path (eg: mymodule.post_hook) to a
                            callable which will be executed after a request is
                            done for example: eg. post_hook(response). It must
                            return a given response parameter or raise an
                            `break.break.RequestException` for failed request.
      --json-output         Prints the results in JSON instead of the default
                            format
      -n REQUESTS, --requests REQUESTS
                            Number of requests
      -d DURATION, --duration DURATION
                            Duration in seconds


Calling from Python code
========================

You can trigger load testing from Python code by importing the function
`break_.load` directly, as follows::

    from break_ import load

    result = load('http://example.com/', 1, 1, 0, 'GET', None, 'text/plain', None, quiet=True)


Design
======

Boom uses **Molotov** under the hood. It's just a simple Molotov script that makes
it simple to runs an AB-like test against a single HTTP endpoint using command line
options.

If you are interested in this project, you are welcome to join the fun at
https://github.com/tarekziade/break

Make sure to add yourself to the contributors list if your PR gets merged. And
make sure it's in alphabetical order!
