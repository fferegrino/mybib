import json
from copy import deepcopy
from unittest.mock import patch, Mock

validate_indexes = Mock()


def test_get_identifier(client):
    expected = {'my': 'bib'}
    with patch('mybib.web.api.papers.get_paper_neo4j', return_value=expected) as get_paper:
        response = client.get('/api/papers/paper1')
        actual = json.loads(response.get_data(as_text=True))
        get_paper.assert_called_with('paper1')
    assert expected == actual


def test_get_search(client, json_multiple_authors):
    with patch('mybib.web.api.papers.search_papers_neo4j') as search_papers:
        title = 'A title'
        search_papers.return_value = json_multiple_authors

        response = client.get(f'/api/papers/search?title={title}')

        actual = json.loads(response.get_data(as_text=True))
        search_papers.assert_called_with(title)
    assert json_multiple_authors == actual


@patch('mybib.web.api.papers.insert_paper_neo4j')
@patch('mybib.web.api.papers.load_from_string')
@patch('mybib.web.api.papers.insert_author_neo4j')
@patch('mybib.web.api.papers.insert_kw_neo4j')
@patch('mybib.web.api.papers.insert_author_paper_reference')
@patch('mybib.web.api.papers.insert_keyword_paper_reference')
def test_post(insert_keyword_paper_reference,
              insert_author_paper_reference,
              insert_kw_neo4j,
              insert_author_neo4j,
              load_from_string_mock,
              insert_paper_neo4j_mock,
              client, bibtex_multiple_authors, json_multiple_authors,
              auth_header):
    load_from_string_mock.return_value = json_multiple_authors
    with patch('mybib.web.authentication.check_auth') as check_auth:
        check_auth.return_value = True
        entries = deepcopy(json_multiple_authors)

        inserted_paper = entries[0]
        inserted_paper['_bibtex'] = bibtex_multiple_authors

        keywords = inserted_paper.pop('keywords')
        authors = inserted_paper.pop('authors')

        response = client.post('/api/papers', data=bibtex_multiple_authors, headers=auth_header)

        load_from_string_mock.assert_called_with(bibtex_multiple_authors)
        insert_paper_neo4j_mock.assert_called_with(inserted_paper)

        assert len(insert_kw_neo4j.mock_calls) == len(keywords)
        assert len(insert_author_neo4j.mock_calls) == len(authors)

        assert len(insert_keyword_paper_reference.mock_calls) == len(keywords)
        assert len(insert_author_paper_reference.mock_calls) == len(authors)
        assert response.status_code == 201
