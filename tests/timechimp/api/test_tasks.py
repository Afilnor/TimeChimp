import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
        timechimp.api.tasks.create({}, to_json=True)


class TestGetAll:
    tasks = timechimp.api.tasks.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.tasks, list))


class TestGetById:
    task = {}
    if TestGetAll.tasks:
        task = timechimp.api.tasks.get_by_id(
            task_id=TestGetAll.tasks[0]["id"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.tasks.get_by_id(1)

    @pytest.mark.skipif(not TestGetAll.tasks, reason="no tasks found")
    def test_is_dict(self):
        assert(isinstance(TestGetAll.tasks[0], dict))

    @pytest.mark.skipif(not TestGetAll.tasks, reason="no tasks found")
    def test_is_same_id(self):
        assert(TestGetAll.tasks[0]["id"] == TestGetById.task["id"])


class TestUpdate:
    task = {}
    if TestGetById.task:
        task = timechimp.api.tasks.update(task=TestGetById.task, to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.tasks.update({})

    @pytest.mark.skipif(not TestGetAll.tasks, reason="no tasks found")
    def test_is_dict(self):
        assert(isinstance(TestUpdate.task, dict))

    @pytest.mark.skipif(not TestGetAll.tasks, reason="no tasks found")
    def test_is_same_id(self):
        assert(TestGetById.task["id"] == TestUpdate.task["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.tasks.delete(task_id=1)
