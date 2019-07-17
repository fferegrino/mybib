import json
from unittest.mock import MagicMock, patch

import pytest

from mybib.graphql.access_layer import EntityAlreadyExistsError


@patch("mybib.web.api.references.insert_reference")
def test_post_inserts(insert_reference_mock, authenticated_post):
    id1 = "id1"
    id2 = "id2"
    expected = {"a": "reference"}

    response = authenticated_post(
        f"/api/references/{id1}/{id2}",
        data=json.dumps(expected),
        content_type="application/json",
    )
    insert_reference_mock.assert_called_once_with(id1, id2, expected)
    assert response.status_code == 201


@patch(
    "mybib.web.api.references.insert_reference", side_effect=EntityAlreadyExistsError()
)
def test_post_inserts_fails_already_exists(insert_reference_mock, authenticated_post):
    id1 = "id1"
    id2 = "id2"
    expected = {"a": "reference"}

    response = authenticated_post(
        f"/api/references/{id1}/{id2}",
        data=json.dumps(expected),
        content_type="application/json",
    )
    insert_reference_mock.assert_called_once_with(id1, id2, expected)
    assert response.status_code == 409


@patch("mybib.web.api.references.insert_reference", side_effect=AssertionError())
def test_post_inserts_fails_reference_does_not_exist(
    insert_reference_mock, authenticated_post
):
    id1 = "id1"
    id2 = "id2"
    expected = {"a": "reference"}

    response = authenticated_post(
        f"/api/references/{id1}/{id2}",
        data=json.dumps(expected),
        content_type="application/json",
    )
    insert_reference_mock.assert_called_once_with(id1, id2, expected)
    assert response.status_code == 400


@pytest.mark.skip
@patch("mybib.web.api.references.insert_reference.fetch", autospec=True)
@patch("mybib.web.api.references.are_related", autospec=True, return_value=False)
def test_post_inserts_(are_related_mock, fetch_mock, authenticated_post):
    referee_mock = MagicMock()
    referenced_mock = MagicMock()
    fetch_mock.side_effect = [referee_mock, referenced_mock]

    id1 = "id1"
    id2 = "id2"
    expected = {"a": "reference"}

    response = authenticated_post(
        f"/api/references/{id1}/{id2}",
        data=json.dumps(expected),
        content_type="application/json",
    )
    are_related_mock.assert_called_once_with(id1, id2)
    referee_mock.references.add.assert_called_once_with(referenced_mock, expected)
    assert response.status_code == 201


@pytest.mark.skip
@patch("mybib.web.api.references.Paper.fetch", autospec=True)
@patch("mybib.web.api.references.are_related", autospec=True, return_value=True)
def test_post_already_exists(are_related_mock, fetch_mock, authenticated_post):
    referee_mock = MagicMock()
    referenced_mock = MagicMock()
    fetch_mock.side_effect = [referee_mock, referenced_mock]

    id1 = "id1"
    id2 = "id2"
    expected = {"a": "reference"}

    response = authenticated_post(
        f"/api/references/{id1}/{id2}",
        data=json.dumps(expected),
        content_type="application/json",
    )
    are_related_mock.assert_called_once_with(id1, id2)
    assert not referee_mock.references.add.called
    assert response.status_code == 409
