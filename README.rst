Salvo
=====

.. image:: http://coveralls.io/repos/github/tarekziade/salvo/badge.svg?branch=master
   :target: https://coveralls.io/github/tarekziade/salvo?branch=master

.. image:: http://travis-ci.org/tarekziade/salvo.svg?branch=master
   :target: https://travis-ci.org/tarekziade/salvo



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

    % salvo http://localhost:80 -c 10 -n 100
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


You can also use `--duration` if you want to run for a given amount of time.

For a full list of features, run `salvo --help`


Contribute
==========

Salvo is very simple and anyone familiar with Python can contribute.

If you are interested in this project, you are welcome to join the fun at
https://github.com/tarekziade/salvo

Make sure to add yourself to the contributors list if your PR gets merged. And
make sure it's in alphabetical order!
