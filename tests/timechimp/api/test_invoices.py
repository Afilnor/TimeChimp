import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestGetAll:
    invoices = timechimp.api.invoices.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.invoices, list))


class TestGetById:
    invoice = {}
    if TestGetAll.invoices:
        timechimp.api.invoices.get_by_id(
            invoice_id=TestGetAll.invoices[0]["id"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.invoices.get_by_id(1)

    @pytest.mark.skipif(not TestGetAll.invoices, reason="no invoices found")
    def test_is_dict(self):
        assert(isinstance(TestGetById.invoice, dict))

    @pytest.mark.skipif(not TestGetAll.invoices, reason="no invoices found")
    def test_is_same_id(self):
        assert(TestGetAll.invoices[0]["id"] == TestGetById.invoice["id"])


class TestGetByProject:
    invoices = []
    if TestGetById.invoice:
        invoices = timechimp.api.invoices.get_by_project(
            project_id=TestGetById.invoice["projectId"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.get_by_project(project_id=1)

    @pytest.mark.skipif(not TestGetById.invoice, reason="no invoices found")
    def test_is_list(self):
        assert(isinstance(TestGetByProject.invoices, list))

    @pytest.mark.skipif(not TestGetById.invoice, reason="no invoices found")
    def test_is_same_id(self):
        assert(all(project["projectId"] == TestGetById.invoice["projectId"]
                   for project in TestGetByProject.invoices))
