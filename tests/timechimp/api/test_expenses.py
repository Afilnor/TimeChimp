from datetime import datetime, timedelta

import logging
import json

import pytest
import requests.models

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    expenses = timechimp.api.expenses.create({}, to_json=True)

    def test_is_dict(self):
        assert (isinstance(TestCreate.expenses, dict))


class TestGetById:
    expenses = timechimp.api.expenses.get_by_id(
        expense_id=TestCreate.expenses["id"] or 1,
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.expenses.get_by_id(1)

    def test_is_dict(self):
        assert(isinstance(TestGetById.expenses, dict))

    def test_is_same_id(self):
        assert(TestCreate.expenses["id"] == TestGetById.expenses["id"])


class TestGetByProject:

    expenses = timechimp.api.expenses.get_by_project(project_id=TestGetById.expenses["projectId"] or 1,
                                                     to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetByProject.expenses, list))

    def test_is_same_id(self):
        assert(all(project["projectId"] == TestCreate.expenses["projectId"]
                   for project in TestGetByProject.expenses))


class TestSubmitForApprovalInternal:
    registrations = timechimp.api.expenses.submit_for_approval_internal(
        registration_ids=[TestCreate.expenses["id"]],
        message="test",
        to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetByProject.expenses, list))

    def test_is_same_id(self):
        assert(all(registration["id"] == TestCreate.expenses["id"]
                   for registration in TestSubmitForApprovalInternal.registrations))


class TestSubmitForApprovalExternal:
    registrations = timechimp.api.expenses.submit_for_approval_external(
        registration_ids=[TestCreate.expenses["id"]],
        contact_person_emails=["test@gmail.com"],
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.expenses.submit_for_approval_external(
                registration_ids=[],
                contact_person_emails=["test@gmail.com"],
                message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.expenses, list))

    def test_is_same_id(self):
        assert(all(registration == TestCreate.expenses["id"]
                   for registration in TestSubmitForApprovalExternal.registrations))


class TestChangeStatusInternal:
    registrations = timechimp.api.expenses.change_status_internal(
        registration_ids=[TestCreate.expenses["id"]],
        approval_status=timechimp.enum.ApprovalStatus.REJECTED,
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.expenses.change_status_internal(
                registration_ids=[],
                approval_status=timechimp.enum.ApprovalStatus.REJECTED,
                message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.expenses, list))

    def test_is_same_id(self):
        assert(all(registration == TestCreate.expenses["id"]
                   for registration in TestChangeStatusInternal.registrations))


class TestChangeStatusExternal:
    registrations = timechimp.api.expenses.change_status_external(
        registration_ids=[TestCreate.expenses["id"]],
        approval_status=timechimp.enum.ApprovalStatus.REJECTED,
        name="test",
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.expenses.change_status_external(
                registration_ids=[],
                approval_status=timechimp.enum.ApprovalStatus.REJECTED,
                name="test",
                message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.expenses, list))

    def test_is_same_id(self):
        assert(all(registration == TestCreate.expenses["id"]
                   for registration in TestChangeStatusExternal.registrations))


class TestUpdate:
    expenses = timechimp.api.expenses.update(expense=TestCreate.expenses, to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.expenses.update({})

    def test_is_dict(self):
        assert(isinstance(TestUpdate.expenses, dict))

    def test_is_same_id(self):
        assert(TestCreate.expenses["id"] == TestUpdate.expenses["id"])


class TestDelete:
    response = timechimp.api.expenses.delete(expense_id=TestCreate.expenses["id"])

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.expenses.delete(expense_id=1)

    def test_ok_delete(self):
        assert(TestDelete.response.status_code == 200)

    def test_is_json_decode_error(self):
        with pytest.raises(json.decoder.JSONDecodeError):
            timechimp._response.to_json(TestDelete.response)


class TestGetByTimeRange:
    expenses = timechimp.api.expenses.get_by_date_range(
            date_from=datetime.now().strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"),
            to_json=True)

    response = timechimp.api.expenses.get_by_date_range(
            date_from=datetime.now().strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"))

    def test_is_list(self):
        assert(isinstance(TestGetByTimeRange.expenses, list))

    def test_is_request_response_instance(self):
        assert (isinstance(TestGetByTimeRange.response, requests.models.Response))

    def test_is_date_range_exception(self):
        with pytest.raises(ValueError):
            timechimp.api.expenses.get_by_date_range(
                date_from=datetime.now().strftime("%Y-%m-%d"),
                date_to=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))


class TestGetAll:
    expenses = timechimp.api.expenses.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.expenses, list))
