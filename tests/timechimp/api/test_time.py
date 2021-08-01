from datetime import datetime, timedelta
import logging

import pytest
import requests.models

import timechimp

logger = logging.getLogger(__name__)


class TestGetByTimeRange:
    times = timechimp.api.time.get_by_date_range(
            date_from=datetime.now().strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"),
            to_json=True)

    response = timechimp.api.time.get_by_date_range(
            date_from=datetime.now().strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"))

    def test_is_list(self):
        assert(isinstance(TestGetByTimeRange.times, list))

    def test_is_request_response_instance(self):
        assert (isinstance(TestGetByTimeRange.response, requests.models.Response))

    def test_is_date_range_exception(self):
        with pytest.raises(timechimp.exceptions.TimeChimpDateRangeError):
            timechimp.api.time.get_by_date_range(
                date_from=datetime.now().strftime("%Y-%m-%d"),
                date_to=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))


class TestGetAll:
    times = timechimp.api.time.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.times, list))


class TestGetById:
    time = timechimp.api.time.get_by_id(
        time_id=TestGetAll.times[0]["id"],
        to_json=True) if TestGetAll.times else {}

    def test_is_dict(self):
        assert(isinstance(TestGetById.time, dict))

    def test_is_api_exception(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.delete(
                time_id=10,
                to_json=True)