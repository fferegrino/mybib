from copy import deepcopy
from unittest.mock import MagicMock, Mock, patch

from mybib.neo4j.models import Paper

validate_indexes = Mock()


@patch("mybib.web.api.papers.Paper", autospec=True)
@patch("mybib.web.api.papers.get_create_keyword", return_value=MagicMock())
@patch("mybib.web.api.papers.get_create_author", return_value=MagicMock())
def test_post_inserts(
    get_create_author_mock,
    get_create_keyword_mock,
    paper_mock,
    authenticated_post,
    bibtex_multiple_authors,
    json_multiple_authors,
):
    fake_paper = MagicMock()
    fake_paper.fetch = MagicMock(return_value=None)
    paper_mock.return_value = fake_paper

    entries = deepcopy(json_multiple_authors)

    inserted_paper = entries[0]
    inserted_paper["_bibtex"] = bibtex_multiple_authors

    keywords = inserted_paper.pop("keywords")
    authors = inserted_paper.pop("authors")

    response = authenticated_post("/api/papers", data=bibtex_multiple_authors)

    assert len(get_create_keyword_mock.mock_calls) == len(keywords)
    assert len(get_create_author_mock.mock_calls) == len(authors)
    paper_mock.assert_called_once_with(**inserted_paper)
    fake_paper.save.assert_called()
    assert response.status_code == 201


@patch("mybib.web.api.papers.Paper", autospec=True)
@patch("mybib.web.api.papers.get_create_keyword", return_value=MagicMock())
@patch("mybib.web.api.papers.get_create_author", return_value=MagicMock())
def test_post_does_not_insert(
    get_create_author_mock,
    get_create_keyword_mock,
    paper_mock,
    authenticated_post,
    bibtex_multiple_authors,
    json_multiple_authors,
):
    fake_paper = MagicMock()
    fake_paper.fetch.return_value = Paper(ID="ID1")

    entries = deepcopy(json_multiple_authors)

    inserted_paper = entries[0]
    inserted_paper["_bibtex"] = bibtex_multiple_authors

    inserted_paper.pop("keywords")
    inserted_paper.pop("authors")

    response = authenticated_post("/api/papers", data=bibtex_multiple_authors)

    get_create_author_mock.assert_not_called()
    get_create_keyword_mock.assert_not_called()
    paper_mock.assert_called_once_with(**inserted_paper)
    assert not fake_paper.save.called
    assert response.status_code == 409
