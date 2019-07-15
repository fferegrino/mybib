from copy import deepcopy
from unittest.mock import MagicMock, Mock, patch

from mybib.neo4j.models import Paper

validate_indexes = Mock()


@patch("mybib.web.api.papers.Paper", autospec=True)
@patch("mybib.web.api.papers.Author", autospec=True)
@patch("mybib.web.api.papers.Keyword", autospec=True)
def test_post_inserts(
    keyword_mock,
    author_mock,
    paper_mock,
    authenticated_post,
    bibtex_multiple_authors,
    json_multiple_authors,
):
    fake_paper = MagicMock()
    fake_paper.fetch = MagicMock(return_value=None)
    paper_mock.return_value = fake_paper

    fake_author = MagicMock()
    author_mock.return_value = fake_author

    fake_keyword = MagicMock()
    keyword_mock.return_value = fake_keyword

    entries = deepcopy(json_multiple_authors)

    inserted_paper = entries[0]
    inserted_paper["_bibtex"] = bibtex_multiple_authors

    keywords = inserted_paper.pop("keywords")
    authors = inserted_paper.pop("authors")

    response = authenticated_post("/api/papers", data=bibtex_multiple_authors)

    assert len(keyword_mock.mock_calls) == len(keywords) * 3
    assert len(author_mock.mock_calls) == len(authors) * 3
    paper_mock.assert_called_once_with(**inserted_paper)
    fake_paper.save.assert_called()
    assert response.status_code == 201


@patch("mybib.web.api.papers.Paper", autospec=True)
@patch("mybib.web.api.papers.Author", autospec=True)
@patch("mybib.web.api.papers.Keyword", autospec=True)
def test_post_does_not_insert(
    keyword_mock,
    author_mock,
    paper_mock,
    authenticated_post,
    bibtex_multiple_authors,
    json_multiple_authors,
):
    fake_paper = MagicMock()
    fake_paper.fetch = MagicMock(return_value=Paper(ID="ID1"))

    fake_author = MagicMock()
    author_mock.return_value = fake_author

    fake_keyword = MagicMock()
    keyword_mock.return_value = fake_keyword

    entries = deepcopy(json_multiple_authors)

    inserted_paper = entries[0]
    inserted_paper["_bibtex"] = bibtex_multiple_authors

    inserted_paper.pop("keywords")
    inserted_paper.pop("authors")

    response = authenticated_post("/api/papers", data=bibtex_multiple_authors)

    assert len(keyword_mock.mock_calls) == 0
    assert len(author_mock.mock_calls) == 0
    paper_mock.assert_called_once_with(**inserted_paper)
    assert not fake_paper.save.called
    assert response.status_code == 409
