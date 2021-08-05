from datetime import datetime, timedelta

import logging
import json

import pytest
import requests.models

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    mileage = timechimp.api.mileage.create({}, to_json=True)

    def test_is_dict(self):
        assert (isinstance(TestCreate.mileage, dict))


class TestGetById:
    mileage = timechimp.api.mileage.get_by_id(
        mileage_id=TestCreate.mileage["id"] or 1,
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.mileage.get_by_id(1)

    def test_is_dict(self):
        assert(isinstance(TestGetById.mileage, dict))

    def test_is_same_id(self):
        assert(TestCreate.mileage["id"] == TestGetById.mileage["id"])


class TestGetByProject:

    mileages = timechimp.api.mileage.get_by_project(project_id=TestGetById.mileage["projectId"] or 1,
                                                    to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetByProject.mileages, list))

    @pytest.mark.skip(reason="Not associated to a project by default")
    def test_is_same_id(self):
        assert(all(project["projectId"] == TestCreate.mileage["projectId"]
                   for project in TestGetByProject.mileages))


class TestSubmitForApprovalInternal:
    registrations = timechimp.api.mileage.submit_for_approval_internal(
        registration_ids=[TestCreate.mileage["id"]],
        message="test",
        to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetByProject.mileages, list))

    def test_is_same_id(self):
        assert(all(registration["id"] == TestCreate.mileage["id"]
                   for registration in TestSubmitForApprovalInternal.registrations))


class TestSubmitForApprovalExternal:
    registrations = timechimp.api.mileage.submit_for_approval_external(
        registration_ids=[TestCreate.mileage["id"]],
        contact_person_emails=["test@gmail.com"],
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.mileage.submit_for_approval_external(
                registration_ids=[],
                contact_person_emails=["test@gmail.com"],
                message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.mileages, list))

    def test_is_same_id(self):
        assert(all(registration == TestCreate.mileage["id"]
                   for registration in TestSubmitForApprovalExternal.registrations))


class TestChangeStatusInternal:
    registrations = timechimp.api.mileage.change_status_internal(
        registration_ids=[TestCreate.mileage["id"]],
        approval_status=timechimp.enum.ApprovalStatus.REJECTED,
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.mileage.change_status_internal(
                registration_ids=[],
                approval_status=timechimp.enum.ApprovalStatus.REJECTED,
                message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.mileages, list))

    def test_is_same_id(self):
        assert(all(registration == TestCreate.mileage["id"]
                   for registration in TestChangeStatusInternal.registrations))


class TestChangeStatusExternal:
    """ does not seem to work
    registrations = timechimp.api.mileage.change_status_external(
        registration_ids=[TestCreate.mileage["id"]],
        approval_status=timechimp.enum.ApprovalStatus.REJECTED,
        name="test",
        message="test",
        to_json=True)
    """
    registrations = {}

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.mileage.change_status_external(
                registration_ids=[],
                approval_status=timechimp.enum.ApprovalStatus.REJECTED,
                name="test",
                message="test")

    @pytest.mark.skip(reason="Not able to change status external")
    def test_is_list(self):
        assert(isinstance(TestGetByProject.mileages, list))

    @pytest.mark.skip(reason="Not able to change status external")
    def test_is_same_id(self):
        assert(all(registration == TestCreate.mileage["id"]
                   for registration in TestChangeStatusExternal.registrations))


class TestUpdate:
    mileage = timechimp.api.mileage.update(mileage=TestCreate.mileage, to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.mileage.update({})

    def test_is_dict(self):
        assert(isinstance(TestUpdate.mileage, dict))

    def test_is_same_id(self):
        assert(TestCreate.mileage["id"] == TestUpdate.mileage["id"])


class TestDelete:
    response = timechimp.api.mileage.delete(mileage_id=TestCreate.mileage["id"])

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.mileage.delete(mileage_id=1)

    def test_ok_delete(self):
        assert(TestDelete.response.status_code == 200)

    def test_is_json_decode_error(self):
        with pytest.raises(json.decoder.JSONDecodeError):
            timechimp._response.to_json(TestDelete.response)


class TestGetByTimeRange:
    mileages = timechimp.api.mileage.get_by_date_range(
            date_from=datetime.now().strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"),
            to_json=True)

    response = timechimp.api.mileage.get_by_date_range(
            date_from=datetime.now().strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"))

    def test_is_list(self):
        assert(isinstance(TestGetByTimeRange.mileages, list))

    def test_is_request_response_instance(self):
        assert (isinstance(TestGetByTimeRange.response, requests.models.Response))

    def test_is_date_range_exception(self):
        with pytest.raises(ValueError):
            timechimp.api.mileage.get_by_date_range(
                date_from=datetime.now().strftime("%Y-%m-%d"),
                date_to=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))


class TestGetAll:
    mileages = timechimp.api.mileage.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.mileages, list))
