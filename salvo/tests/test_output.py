import json
import io
from salvo.output import print_errors, RunResults


def one_print(func, *args):
    stream = io.StringIO()
    func(*args, stream=stream)
    stream.seek(0)
    return stream.read()


def test_print_errors():
    assert one_print(print_errors, []) == ""
    assert "two\n" in one_print(print_errors, ["one", "two"])


def test_run_results():
    res = RunResults()
    for i in range(10):
        res.incr()

    output = one_print(res.print_stats)
    assert "10 times" in output

    output = json.loads(one_print(res.print_json))
    assert output["count"] == 10
