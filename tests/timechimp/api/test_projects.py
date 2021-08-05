import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.projects.create({}, to_json=True)


class TestGetAll:
    projects = timechimp.api.projects.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.projects, list))


class TestGetById:
    project = timechimp.api.projects.get_by_id(
        project_id=TestGetAll.projects[0]["id"],
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.projects.get_by_id(1)

    def test_is_dict(self):
        assert(isinstance(TestGetAll.projects[0], dict))

    def test_is_same_id(self):
        assert(TestGetAll.projects[0]["id"] == TestGetById.project["id"])


class TestGetByCustomer:
    project = timechimp.api.projects.get_by_customer(customer_id=TestGetById.project["customerId"],
                                                     to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetByCustomer.project, list))

    def test_is_same_id(self):
        assert(all(project["customerId"] == TestGetById.project["customerId"]
                   for project in TestGetByCustomer.project))


class TestGetByInsight:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.projects.get_by_insight(insight_id=1,
                                                  to_json=True)


class TestUpdate:
    project = timechimp.api.projects.update(project=TestGetById.project, to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.projects.update({})

    def test_is_dict(self):
        assert(isinstance(TestUpdate.project, dict))

    def test_is_same_id(self):
        assert(TestGetById.project["id"] == TestUpdate.project["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.projects.delete(project_id=1)
