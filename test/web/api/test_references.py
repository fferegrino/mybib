import base64
import json
from unittest.mock import patch, Mock

import pytest

from mybib.web.app import app

validate_indexes = Mock()


def test_get_two_identifiers(client):
    id1 = 'id1'
    id2 = 'id2'
    expected = {'a': 'reference'}
    with patch('mybib.web.api.references.get_reference_neo4j', return_value={'a': 'reference'}) as get_reference:
        response = client.get(f'/api/references/{id1}/{id2}')
        actual = json.loads(response.get_data(as_text=True))
        get_reference.assert_called_with(id1, id2)
    assert expected == actual


@patch('mybib.web.api.references.insert_reference')
def test_post(insert_reference_mock, client):
    id1 = 'id1'
    id2 = 'id2'
    expected = {'a': 'reference'}
    with patch('mybib.web.authentication.check_auth') as check_auth:
        check_auth.return_value = True

        valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
        response = client.post(f'/api/references/{id1}/{id2}', data=json.dumps(expected),
                               headers={'Authorization': 'Basic ' + valid_credentials},
                               content_type='application/json')

        assert response.status_code == 201
        insert_reference_mock.assert_called_with(id1, id2, expected)
