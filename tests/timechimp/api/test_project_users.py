import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_users.create({}, to_json=True)


class TestGetAll:
    project_users = timechimp.api.project_users.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.project_users, list))


class TestGetById:
    project_user = {}
    if TestGetAll.project_users:
        project_user = timechimp.api.project_users.get_by_id(
            project_user_id=TestGetAll.project_users[0]["id"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_users.get_by_id(1)

    @pytest.mark.skipif(not TestGetAll.project_users, reason="no project users found")
    def test_is_dict(self):
        assert(isinstance(TestGetAll.project_users[0], dict))

    @pytest.mark.skipif(not TestGetAll.project_users, reason="no project users found")
    def test_is_same_id(self):
        assert(TestGetAll.project_users[0]["id"] == TestGetById.project_user["id"])


class TestGetByProject:
    project_users = []
    if TestGetById.project_user:
        project_user = timechimp.api.project_users.get_by_project(project_id=TestGetById.project_user["projectId"],
                                                                  to_json=True)

    @pytest.mark.skipif(not TestGetAll.project_users, reason="no project users found")
    def test_is_list(self):
        assert(isinstance(TestGetByProject.project_user, list))

    @pytest.mark.skipif(not TestGetAll.project_users, reason="no project users found")
    def test_is_same_id(self):
        assert(all(project_user["projectId"] == TestGetById.project_user["projectId"]
                   for project_user in TestGetByProject.project_user))


class TestGetByUser:
    project_user = []
    if TestGetById.project_user:
        project_user = timechimp.api.project_users.get_by_user(user_id=TestGetById.project_user["userId"],
                                                               to_json=True)

    @pytest.mark.skipif(not TestGetById.project_user, reason="no project users found")
    def test_is_list(self):
        assert(isinstance(TestGetByUser.project_user, list))

    @pytest.mark.skipif(not TestGetById.project_user, reason="no project users found")
    def test_is_same_id(self):
        assert(all(int(project_user["userId"]) == int(TestGetById.project_user["userId"])
                   for project_user in TestGetByUser.project_user))


class TestUpdate:
    project_user = []
    if TestGetById.project_user:
        project_user = timechimp.api.project_users.update(project_user=TestGetById.project_user,
                                                          to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_users.update({})

    @pytest.mark.skipif(not TestGetById.project_user, reason="no project users found")
    def test_is_dict(self):
        assert(isinstance(TestUpdate.project_user, dict))

    @pytest.mark.skipif(not TestGetById.project_user, reason="no project users found")
    def test_is_same_id(self):
        assert(TestGetById.project_user["id"] == TestUpdate.project_user["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_users.delete(project_user_id=1)
