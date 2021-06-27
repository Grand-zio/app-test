import pytest
from util import HttpRequest

DEVICE_LIST = []


@pytest.fixture
def http_request():
    return HttpRequest.HttpRequest


def pytest_addoption(parser):
    parser.addoption(
        "--device", action="store", default="", help="get device name"
    )


@pytest.fixture
def device_name(request):
    return request.config.getoption("--device")


