import json
from unittest.mock import patch, Mock

validate_indexes = Mock()


def test_get_identifier(client):
    expected = {'nodes': [], 'references': []}
    return_value = ([], [])
    with patch('mybib.web.api.root.recent_papers_and_references',
               return_value=return_value) as recent_papers_and_references:
        response = client.get('/api/recent')
        actual = json.loads(response.get_data(as_text=True))
        recent_papers_and_references.assert_called_with()
    assert expected == actual
