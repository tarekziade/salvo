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


def test_run_results_with_progress_no_res():
    res = RunResults(server_info={"extra": "info"}, num=10)
    output = one_print(res.print_stats)
    output = json.loads(one_print(res.print_json))
    assert output["count"] == 0


def test_run_results_with_progress_no_tot():
    # corner case when total time is zero
    res = RunResults(server_info={"extra": "info"}, num=10)
    res.incr(duration=1)
    res.total_time = 0
    output = one_print(res.print_stats)
    output = json.loads(one_print(res.print_json))
    assert output["count"] == 1


def test_run_results_quiet():
    res = RunResults(server_info={"extra": "info"}, num=10, quiet=True)
    for i in range(10):
        res.incr(duration=10)

    output = one_print(res.print_stats)
    assert "10 times" in output

    output = json.loads(one_print(res.print_json))
    assert output["count"] == 10


def test_run_results_with_progress():
    res = RunResults(server_info={"extra": "info"}, num=10)
    for i in range(10):
        res.incr(duration=10)

    output = one_print(res.print_stats)
    assert "10 times" in output

    output = json.loads(one_print(res.print_json))
    assert output["count"] == 10


def test_run_results():
    res = RunResults(num=None)
    for i in range(10):
        res.incr(duration=10)

    output = one_print(res.print_stats)
    assert "10 times" in output

    output = json.loads(one_print(res.print_json))
    assert output["count"] == 10
