import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_tasks.create({}, to_json=True)


class TestGetAll:
    project_tasks = timechimp.api.project_tasks.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.project_tasks, list))


class TestGetById:
    project_task = []
    if TestGetAll.project_tasks:
        project_task = timechimp.api.project_tasks.get_by_id(
            project_task_id=TestGetAll.project_tasks[0]["id"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_tasks.get_by_id(1)

    @pytest.mark.skipif(not TestGetAll.project_tasks, reason="no project tasks found")
    def test_is_dict(self):
        assert(isinstance(TestGetAll.project_tasks[0], dict))

    @pytest.mark.skipif(not TestGetAll.project_tasks, reason="no project tasks found")
    def test_is_same_id(self):
        assert(TestGetAll.project_tasks[0]["id"] == TestGetById.project_task["id"])


class TestGetByProject:
    project_task = []
    if TestGetById.project_task:
        project_task = timechimp.api.project_tasks.get_by_project(project_id=TestGetById.project_task["projectId"],
                                                                  to_json=True)

    @pytest.mark.skipif(not TestGetById.project_task, reason="no project tasks found")
    def test_is_list(self):
        assert(isinstance(TestGetByProject.project_task, list))

    @pytest.mark.skipif(not TestGetById.project_task, reason="no project tasks found")
    def test_is_same_id(self):
        assert(all(project_task["projectId"] == TestGetById.project_task["projectId"]
                   for project_task in TestGetByProject.project_task))


class TestGetByTask:
    project_task = []
    if TestGetById.project_task:
        project_task = timechimp.api.project_tasks.get_by_task(task_id=TestGetById.project_task["taskId"],
                                                               to_json=True)

    @pytest.mark.skipif(not TestGetById.project_task, reason="no project tasks found")
    def test_is_list(self):
        assert(isinstance(TestGetByProject.project_task, list))

    @pytest.mark.skipif(not TestGetById.project_task, reason="no project tasks found")
    def test_is_same_id(self):
        assert(all(project_task["projectId"] == TestGetById.project_task["projectId"]
                   for project_task in TestGetByProject.project_task))


class TestUpdate:
    project_task = []
    if TestGetById.project_task:
        project_task = timechimp.api.project_tasks.update(project_task=TestGetById.project_task,
                                                          to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_tasks.update({})

    @pytest.mark.skipif(not TestGetById.project_task, reason="no project tasks found")
    def test_is_dict(self):
        assert(isinstance(TestUpdate.project_task, dict))

    @pytest.mark.skipif(not TestGetById.project_task, reason="no project tasks found")
    def test_is_same_id(self):
        assert(TestGetById.project_task["id"] == TestUpdate.project_task["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_tasks.delete(project_task_id=1)
