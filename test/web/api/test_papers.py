from copy import deepcopy
from unittest.mock import patch, Mock, MagicMock

validate_indexes = Mock()


def test_get_identifier(client):
    pass


def test_get_search(client, json_multiple_authors):
    pass


@patch('mybib.web.api.papers.Paper', autospec=True)
@patch('mybib.web.api.papers.Author', autospec=True)
@patch('mybib.web.api.papers.Keyword', autospec=True)
def test_post(keyword_mock, author_mock, paper_mock, client, bibtex_multiple_authors, json_multiple_authors,
              auth_header):
    fake_paper = MagicMock()
    paper_mock.return_value = fake_paper

    fake_author = MagicMock()
    author_mock.return_value = fake_author

    fake_keyword = MagicMock()
    keyword_mock.return_value = fake_keyword

    with patch('mybib.web.authentication.check_auth') as check_auth:
        check_auth.return_value = True
        entries = deepcopy(json_multiple_authors)

        inserted_paper = entries[0]
        inserted_paper['_bibtex'] = bibtex_multiple_authors

        keywords = inserted_paper.pop('keywords')
        authors = inserted_paper.pop('authors')

        response = client.post('/api/papers', data=bibtex_multiple_authors, headers=auth_header)

        assert len(keyword_mock.mock_calls) == len(keywords) * 2
        assert len(author_mock.mock_calls) == len(authors) * 2
        paper_mock.assert_called_once_with(**inserted_paper)
        fake_paper.save.assert_called()
        assert response.status_code == 201
