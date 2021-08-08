import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.user_contracts.create({}, to_json=True)


class TestGetAll:
    user_contracts = timechimp.api.user_contracts.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.user_contracts, list))


class TestGetById:
    user_contract = {}
    if TestGetAll.user_contracts:
        user_contract = timechimp.api.user_contracts.get_by_id(
            user_contract_id=TestGetAll.user_contracts[0]["id"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.user_contracts.get_by_id(1)

    @pytest.mark.skipif(not TestGetAll.user_contracts, reason="no user contracts found")
    def test_is_dict(self):
        assert(isinstance(TestGetById.user_contract, dict))

    @pytest.mark.skipif(not TestGetAll.user_contracts, reason="no user contracts found")
    def test_is_same_id(self):
        assert(TestGetAll.user_contracts[0]["id"] == TestGetById.user_contract["id"])


class TestGetByUser:
    user_contract = []
    if TestGetById.user_contract:
        user_contract = timechimp.api.user_contracts.get_by_user(user_id=TestGetById.user_contract["userId"],
                                                                 to_json=True)

    @pytest.mark.skipif(not TestGetAll.user_contracts, reason="no user contracts found")
    def test_is_list(self):
        assert(isinstance(TestGetByUser.user_contract, list))

    @pytest.mark.skipif(not TestGetAll.user_contracts, reason="no user contracts found")
    def test_is_same_id(self):
        assert(all(user_contract["userId"] == TestGetById.user_contract["userId"]
                   for user_contract in TestGetByUser.user_contract))


@pytest.mark.skipif(not TestGetAll.user_contracts, reason="no user contracts found")
class TestUpdate:
    user_contract = []
    if TestGetById.user_contract:
        user_contract = timechimp.api.user_contracts.update(user_contract=TestGetById.user_contract,
                                                            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.user_contracts.update({})

    @pytest.mark.skipif(not TestGetAll.user_contracts, reason="no user contracts found")
    def test_is_dict(self):
        assert(isinstance(TestUpdate.user_contract, dict))

    @pytest.mark.skipif(not TestGetAll.user_contracts, reason="no user contracts found")
    def test_is_same_id(self):
        assert(TestGetById.user_contract["id"] == TestUpdate.user_contract["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.user_contracts.delete(user_contract_id=1)
