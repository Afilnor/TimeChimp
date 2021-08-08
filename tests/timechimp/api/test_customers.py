import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.customers.create({}, to_json=True)


class TestGetAll:
    customers = timechimp.api.customers.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.customers, list))


class TestGetById:
    customer = {}
    if TestGetAll.customers:
        customer = timechimp.api.customers.get_by_id(
            customer_id=TestGetAll.customers[0]["id"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.customers.get_by_id(1)

    @pytest.mark.skipif(not TestGetAll.customers, reason="no customer found")
    def test_is_dict(self):
        assert(isinstance(TestGetById.customer, dict))

    @pytest.mark.skipif(not TestGetAll.customers, reason="no customer found")
    def test_is_same_id(self):
        assert(TestGetAll.customers[0]["id"] == TestUpdate.customer["id"])


class TestGetByRelation:
    customers = []
    if TestGetById.customer:
        customers = timechimp.api.customers.get_by_relation(relation_id=TestGetById.customer["id"],
                                                            to_json=True)

    @pytest.mark.skipif(not TestGetById.customer, reason="no customer found")
    def test_is_list(self):
        assert(isinstance(TestGetByRelation.customers, list))

    @pytest.mark.skipif(not TestGetById.customer, reason="no customer found")
    def test_is_same_id(self):
        assert(all(customer["relationId"] == TestGetAll.customers[0]["id"]
                   for customer in TestGetByRelation.customers))


class TestGetByName:
    customers = []
    if TestGetById.customer:
        customer = timechimp.api.customers.get_by_name(
            customer_name=TestGetById.customer["name"],
            to_json=True)

    @pytest.mark.skipif(not TestGetById.customer, reason="no customer found")
    def test_is_dict(self):
        assert(isinstance(TestGetById.customer, dict))

    @pytest.mark.skipif(not TestGetById.customer, reason="no customer found")
    def test_is_same_id(self):
        assert(TestGetById.customer["name"] == TestGetByName.customer["name"])


class TestUpdate:
    customers = {}
    if TestGetById.customer:
        customer = timechimp.api.customers.update(customer=TestGetById.customer,
                                                  to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.customers.update({})

    @pytest.mark.skipif(not TestGetById.customer, reason="no customer found")
    def test_is_dict(self):
        assert(isinstance(TestUpdate.customer, dict))

    @pytest.mark.skipif(not TestGetById.customer, reason="no customer found")
    def test_is_same_id(self):
        assert(TestGetById.customer["id"] == TestUpdate.customer["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.customers.delete(customer_id=1)
