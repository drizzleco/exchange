import pytest
import datetime
from backend import helpers


def test_to_date_obj():
    assert helpers.toDateObj("2020-08-01 12:52") == datetime.datetime(
        2020, 8, 1, 12, 52
    )
