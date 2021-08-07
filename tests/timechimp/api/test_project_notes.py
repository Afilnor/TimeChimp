import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    project_note = timechimp.api.project_notes.create({}, to_json=True)

    def test_is_dict(self):
        assert(isinstance(TestCreate.project_note, dict))


class TestGetAll:
    project_notes = timechimp.api.project_notes.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.project_notes, list))


class TestGetById:
    project_note = timechimp.api.project_notes.get_by_id(
        project_note_id=TestGetAll.project_notes[0]["id"],
        to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_notes.get_by_id(1)

    def test_is_dict(self):
        assert(isinstance(TestGetAll.project_notes[0], dict))

    def test_is_same_id(self):
        assert(TestGetAll.project_notes[0]["id"] == TestGetById.project_note["id"])


class TestGetByProject:
    project_note = timechimp.api.project_notes.get_by_project(project_id=TestGetById.project_note["projectId"],
                                                              to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetByProject.project_note, list))

    def test_is_same_id(self):
        assert(all(project_note["projectId"] == TestGetById.project_note["projectId"]
                   for project_note in TestGetByProject.project_note))


class TestUpdate:
    project_note = timechimp.api.project_notes.update(project_note=TestGetById.project_note, to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_notes.update({})

    def test_is_dict(self):
        assert(isinstance(TestUpdate.project_note, dict))

    def test_is_same_id(self):
        assert(TestGetById.project_note["id"] == TestUpdate.project_note["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.project_notes.delete(project_note_id=1)
