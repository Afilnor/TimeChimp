import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    users = timechimp.api.users.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.users, list))


class TestGetById:
    user = {}
    if TestGetAll.users:
        user = timechimp.api.users.get_by_id(
            user_id=TestGetAll.users[0]["id"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.users.get_by_id(1)

    def test_is_dict(self):
        assert(isinstance(TestGetById.user, dict))

    @pytest.mark.skipif(not TestGetAll.users, reason="no users found")
    def test_is_same_id(self):
        assert(TestGetAll.users[0]["id"] == TestGetById.user["id"])


class TestUpdate:
    user = {}
    is_ok_updated_endpoint = True
    if TestGetById.user:
        try:
            user = timechimp.api.users.update(user=TestGetById.user, to_json=True)
        except timechimp.exceptions.TimeChimpAPIError:
            logger.error("users.update endpoint is failing")
            is_ok_updated_endpoint = False

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.users.update({})

    def test_is_dict(self):
        assert(isinstance(TestUpdate.user, dict))

    @pytest.mark.skipif(not TestGetAll.users, reason="no users found")
    def test_is_same_id(self):
        if not TestUpdate.is_ok_updated_endpoint:
            pytest.xfail("update endpoint is failing")
        assert(TestGetById.user["id"] == TestUpdate.user["id"])
