from datetime import datetime, timedelta
import logging

import pytest
import requests.models

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    time = timechimp.api.time.create({}, to_json=True)

    def test_is_dict(self):
        assert (isinstance(TestCreate.time, dict))


class TestGetById:
    time = timechimp.api.time.get_by_id(
        time_id=TestCreate.time["id"],
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.get_by_id({})

    def test_is_dict(self):
        assert(isinstance(TestGetById.time, dict))

    def test_is_same_id(self):
        assert(TestCreate.time["id"] == TestGetById.time["id"])


class TestGetByProject:
    times = timechimp.api.time.get_by_project(
        project_id=TestCreate.time["projectId"],
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.get_by_project(project_id=1)

    def test_is_list(self):
        assert(isinstance(TestGetByProject.times, list))

    def test_is_same_id(self):
        assert(all(project["projectId"] == TestCreate.time["projectId"]
                   for project in TestGetByProject.times))


class TestGetByProjectByTimeRange:
    times = timechimp.api.time.get_by_project_by_timerange(
        project_id=TestCreate.time["projectId"],
        date_from=datetime.now().strftime("%Y-%m-%d"),
        date_to=datetime.now().strftime("%Y-%m-%d"),
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.get_by_project_by_timerange(
                project_id=1,
                date_from=datetime.now().strftime("%Y-%m-%d"),
                date_to=datetime.now().strftime("%Y-%m-%d"))

    def test_is_list(self):
        assert(isinstance(TestGetByProjectByTimeRange.times, list))

    def test_is_same_id(self):
        assert(all(project["projectId"] == TestCreate.time["projectId"]
                   for project in TestGetByProjectByTimeRange.times))


class TestSubmitForApprovalInternal:
    registrations = timechimp.api.time.submit_for_approval_internal(
        registration_ids=[TestCreate.time["id"]],
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.submit_for_approval_internal(registration_ids=[], message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.times, list))

    def test_is_same_id(self):
        assert(all(registration["id"] == TestCreate.time["id"]
                   for registration in TestSubmitForApprovalInternal.registrations))


class TestSubmitForApprovalExternal:
    registrations = timechimp.api.time.submit_for_approval_external(
        registration_ids=[TestCreate.time["id"]],
        contact_person_emails=["test@gmail.com"],
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.submit_for_approval_external(
                registration_ids=[],
                contact_person_emails=["test@gmail.com"],
                message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.times, list))

    def test_is_same_id(self):
        assert(all(registration == TestCreate.time["id"]
                   for registration in TestSubmitForApprovalExternal.registrations))


class TestChangeStatusInternal:
    registrations = timechimp.api.time.change_status_internal(
        registration_ids=[TestCreate.time["id"]],
        approval_status=timechimp.enum.ApprovalStatus.REJECTED,
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.change_status_internal(
                registration_ids=[],
                approval_status=timechimp.enum.ApprovalStatus.REJECTED,
                message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.times, list))

    def test_is_same_id(self):
        assert(all(registration == TestCreate.time["id"]
                   for registration in TestChangeStatusInternal.registrations))


class TestChangeStatusExternal:
    registrations = timechimp.api.time.change_status_external(
        registration_ids=[TestCreate.time["id"]],
        approval_status=timechimp.enum.ApprovalStatus.REJECTED,
        name="test",
        message="test",
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.change_status_external(
                registration_ids=[],
                approval_status=timechimp.enum.ApprovalStatus.REJECTED,
                name="test",
                message="test")

    def test_is_list(self):
        assert(isinstance(TestGetByProject.times, list))

    def test_is_same_id(self):
        assert(all(registration == TestCreate.time["id"]
                   for registration in TestChangeStatusExternal.registrations))


class TestGetStatusHistory:
    status = timechimp.api.time.get_status_history(
        time_id=TestCreate.time["id"],
        to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetStatusHistory.status, list))

    def test_is_same_id(self):
        assert(all(status["timeId"] == TestCreate.time["id"]
                   for status in TestGetStatusHistory.status))


class TestUpdate:
    time = timechimp.api.time.update(time=TestCreate.time, to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.update({})

    def test_is_dict(self):
        assert(isinstance(TestUpdate.time, dict))

    def test_is_same_id(self):
        assert(TestCreate.time["id"] == TestUpdate.time["id"])


class TestDelete:
    response = timechimp.api.time.delete(time_id=TestCreate.time["id"])

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.time.delete(time_id=1)

    def test_ok_delete(self):
        assert(TestDelete.response.status_code == 200)

    def test_is_json_decode_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpJSONDecodeError):
            timechimp._response.to_json(TestDelete.response)


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


