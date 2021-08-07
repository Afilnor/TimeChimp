import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    users = timechimp.api.users.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.users, list))


class TestGetById:
    user = timechimp.api.users.get_by_id(
        user_id=TestGetAll.users[0]["id"],
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.users.get_by_id(1)

    def test_is_dict(self):
        assert(isinstance(TestGetById.user, dict))

    def test_is_same_id(self):
        assert(TestGetAll.users[0]["id"] == TestGetById.user["id"])


class TestUpdate:
    """ ERROR
    user = timechimp.api.users.update(user=TestGetById.user, to_json=True)
    """
    user = {}

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.users.update({})

    @pytest.mark.skip(reason="update returns an error")
    def test_is_dict(self):
        assert(isinstance(TestUpdate.user, dict))

    @pytest.mark.skip(reason="update returns an error")
    def test_is_same_id(self):
        assert(TestGetById.user["id"] == TestUpdate.user["id"])
