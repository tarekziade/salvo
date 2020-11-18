import importlib
import sys

from molotov.util import request


def print_server_info(url, method, headers=None, stream=sys.stdout):
    stream.write("-------- Server info --------\n\n")
    res = request(url, "HEAD", headers=headers)
    server = res["headers"].get("server", "Unknown")
    stream.write(f"Server Software: {server}\n")
    if headers:
        for k, v in headers.items():
            stream.write(f"{k}: {v}\n")
    stream.write("\n")
    stream.flush()


def resolve(name):
    func = None

    if "." in name:
        splitted = name.split(".")
        mod_name = ".".join(splitted[:-1])
        func_name = splitted[-1]
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
    else:
        for ns in globals(), __builtins__:
            if name in ns:
                func = ns[name]
                break

    if func is None:
        raise ImportError(f"Cannot find '{name}'")
    return func
