import base64
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


def test_get_search(client, sample_json):
    with patch('mybib.web.api.papers.search_papers_neo4j') as search_papers:
        title = 'A title'
        search_papers.return_value = sample_json

        response = client.get(f'/api/papers/search?title={title}')

        actual = json.loads(response.get_data(as_text=True))
        search_papers.assert_called_with(title)
    assert sample_json == actual


@patch('mybib.web.api.papers.insert_paper_neo4j')
@patch('mybib.web.api.papers.load_from_string')
def test_post(load_from_string_mock, insert_paper_neo4j_mock, client, sample_bibtex, sample_json):
    load_from_string_mock.return_value = sample_json
    with patch('mybib.web.authentication.check_auth') as check_auth:
        check_auth.return_value = True
        entries = deepcopy(sample_json)
        inserted_paper = entries[0]
        inserted_paper['_bibtex'] = sample_bibtex

        valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
        response = client.post('/api/papers', data=sample_bibtex,
                               headers={'Authorization': 'Basic ' + valid_credentials})

        load_from_string_mock.assert_called_with(sample_bibtex)
        insert_paper_neo4j_mock.assert_called_with(inserted_paper)
        assert response.status_code == 201
