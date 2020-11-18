import pytest
import io
from unittest import mock

from salvo.util import print_server_info, resolve


@mock.patch("salvo.util.request")
def test_print_server_info(request):
    request.return_value = {"headers": {"server": "Super"}}
    headers = {"one": "two"}
    stream = io.StringIO()
    print_server_info("http://example.com", "GET", headers, stream=stream)
    stream.seek(0)
    res = stream.read()
    assert "Server Software: Super" in res


def test_resolve():
    res = resolve("salvo.util.print_server_info")
    assert res is print_server_info

    res = resolve("resolve")
    assert res is resolve

    with pytest.raises(ImportError):
        resolve("OoO")
