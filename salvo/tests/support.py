import pathlib
import os
import socketserver
import multiprocessing
import signal
import time
import sys
from contextlib import contextmanager
import functools
import http.server
from http.client import HTTPConnection

HERE = pathlib.Path(__file__).parent


def _run(port):
    os.chdir(str(HERE))
    socketserver.TCPServer.allow_reuse_address = True
    attempts = 0
    httpd = None
    error = None

    while attempts < 3:
        try:
            httpd = socketserver.TCPServer(("", port), RequestHandler)
            break
        except Exception as e:
            error = e
            attempts += 1
            time.sleep(0.1)

    if httpd is None:
        raise OSError("Could not start the coserver: %s" % str(error))

    def _shutdown(*args, **kw):
        httpd.server_close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)
    httpd.serve_forever()


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


def run_server(port=8888):
    """Running in a subprocess to avoid any interference"""
    p = multiprocessing.Process(target=functools.partial(_run, port))
    p.start()
    start = time.time()
    connected = False

    while time.time() - start < 5 and not connected:
        try:
            conn = HTTPConnection("localhost", 8888)
            conn.request("GET", "/")
            conn.getresponse()
            connected = True
        except Exception:
            time.sleep(0.1)
    if not connected:
        os.kill(p.pid, signal.SIGTERM)
        p.join(timeout=1.0)
        raise OSError("Could not connect to coserver")
    return p


_CO = {"clients": 0, "server": None}


@contextmanager
def coserver(port=8888):
    if _CO["clients"] == 0:
        _CO["server"] = run_server(port)

    _CO["clients"] += 1
    try:
        yield
    finally:
        _CO["clients"] -= 1
        if _CO["clients"] == 0:
            os.kill(_CO["server"].pid, signal.SIGTERM)
            _CO["server"].join(timeout=1.0)
            _CO["server"].terminate()
            _CO["server"] = None
