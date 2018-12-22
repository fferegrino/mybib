import json
from unittest.mock import patch, Mock

validate_indexes = Mock()


def test_get_two_identifiers(client):
    id1 = 'id1'
    id2 = 'id2'
    expected = {'a': 'reference'}


def test_post( client, auth_header):
    id1 = 'id1'
    id2 = 'id2'
    expected = {'a': 'reference'}
    with patch('mybib.web.authentication.check_auth') as check_auth:
        check_auth.return_value = True

        response = client.post(f'/api/references/{id1}/{id2}', data=json.dumps(expected),
                               headers=auth_header,
                               content_type='application/json')

        assert response.status_code == 201
