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
    customer = timechimp.api.customers.get_by_id(
        customer_id=TestGetAll.customers[0]["id"],
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.customers.get_by_id(1)

    def test_is_same_id(self):
        assert(TestGetAll.customers[0]["id"] == TestUpdate.customer["id"])


class TestGetByRelation:
    customers = timechimp.api.customers.get_by_relation(relation_id=TestGetAll.customers[0]["relationId"],
                                                        to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetByRelation.customers, list))

    def test_is_same_id(self):
        assert(all(customer["relationId"] == TestGetAll.customers[0]["id"]
                   for customer in TestGetByRelation.customers))


class TestGetByName:
    customer = timechimp.api.customers.get_by_name(
        customer_name=TestGetAll.customers[0]["name"],
        to_json=True)

    def test_is_dict(self):
        assert(isinstance(TestGetById.customer, dict))

    def test_is_same_id(self):
        assert(TestGetAll.customers[0]["name"] == TestGetByName.customer["name"])


class TestUpdate:
    customer = timechimp.api.customers.update(customer=TestGetAll.customers[0], to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.customers.update({})

    def test_is_same_id(self):
        assert(TestGetAll.customers[0]["id"] == TestUpdate.customer["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.customers.delete(customer_id=1)
