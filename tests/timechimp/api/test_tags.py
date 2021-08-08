import logging

import pytest

import timechimp

logger = logging.getLogger(__name__)


class TestCreate:
    with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
        timechimp.api.tags.create({}, to_json=True)


class TestGetAll:
    tags = timechimp.api.tags.get_all(to_json=True)

    def test_is_list(self):
        assert(isinstance(TestGetAll.tags, list))


class TestGetById:
    tag = {}
    if TestGetAll.tags:
        tag = timechimp.api.tags.get_by_id(
            tag_id=TestGetAll.tags[0]["id"],
            to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.tags.get_by_id(1)

    @pytest.mark.skipif(not TestGetAll.tags, reason="no tags found")
    def test_is_dict(self):
        assert(isinstance(TestGetAll.tags[0], dict))

    @pytest.mark.skipif(not TestGetAll.tags, reason="no tags found")
    def test_is_same_id(self):
        assert(TestGetAll.tags[0]["id"] == TestGetById.tag["id"])


class TestUpdate:
    tag = {}
    if TestGetById.tag:
        tag = timechimp.api.tags.update(tag=TestGetById.tag, to_json=True)

    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.tags.update({})

    @pytest.mark.skipif(not TestGetAll.tags, reason="no tags found")
    def test_is_dict(self):
        assert(isinstance(TestUpdate.tag, dict))

    @pytest.mark.skipif(not TestGetAll.tags, reason="no tags found")
    def test_is_same_id(self):
        assert(TestGetById.tag["id"] == TestUpdate.tag["id"])


class TestDelete:
    def test_is_api_error(self):
        with pytest.raises(timechimp.exceptions.TimeChimpAPIError):
            timechimp.api.tags.delete(tag_id=1)
