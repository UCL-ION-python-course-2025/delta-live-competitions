import time

import pytest

from src.timeout import TimeoutException, timeout


def test_timeout_happens():
    @timeout(1)
    def slow_function():
        time.sleep(2)

    with pytest.raises(TimeoutException):
        slow_function()
