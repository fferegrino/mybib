from copy import deepcopy
from unittest.mock import MagicMock, patch

import pytest

from mybib.graphql.access_layer import EntityAlreadyExistsError, insert_paper
from mybib.neo4j.models import Paper


@patch("mybib.graphql.access_layer.Paper", autospec=True)
@patch("mybib.graphql.access_layer.get_create_keyword", return_value=MagicMock())
@patch("mybib.graphql.access_layer.get_create_author", return_value=MagicMock())
def test_insert_paper(
    get_create_author_mock,
    get_create_keyword_mock,
    paper_mock,
    single_json_multiple_authors,
):
    fake_paper = MagicMock()
    fake_paper.fetch.return_value = None
    paper_mock.return_value = fake_paper

    expected_insertion = deepcopy(single_json_multiple_authors)
    keywords = expected_insertion.pop("keywords")
    authors = expected_insertion.pop("authors")

    insert_paper(single_json_multiple_authors)

    assert len(get_create_keyword_mock.mock_calls) == len(keywords)
    assert len(get_create_author_mock.mock_calls) == len(authors)
    assert expected_insertion == single_json_multiple_authors
    paper_mock.assert_called_once_with(**expected_insertion)
    fake_paper.save.assert_called()


@patch("mybib.graphql.access_layer.Paper", autospec=True)
@patch("mybib.graphql.access_layer.get_create_keyword", return_value=MagicMock())
@patch("mybib.graphql.access_layer.get_create_author", return_value=MagicMock())
def test_insert_paper_fails(
    get_create_author_mock,
    get_create_keyword_mock,
    paper_mock,
    single_json_multiple_authors,
):
    fake_paper = MagicMock()
    fake_paper.fetch.return_value = Paper(ID="ID1")
    paper_mock.return_value = fake_paper

    expected_insertion = deepcopy(single_json_multiple_authors)
    expected_insertion.pop("keywords")
    expected_insertion.pop("authors")

    with pytest.raises(EntityAlreadyExistsError):
        insert_paper(single_json_multiple_authors)

    get_create_author_mock.assert_not_called()
    get_create_keyword_mock.assert_not_called()
    paper_mock.assert_called_once_with(**expected_insertion)
    fake_paper.save.assert_not_called()
