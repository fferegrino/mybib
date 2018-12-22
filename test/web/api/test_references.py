import json
from unittest.mock import patch, Mock, MagicMock

validate_indexes = Mock()


def test_get_two_identifiers(client):
    id1 = 'id1'
    id2 = 'id2'
    expected = {'a': 'reference'}


@patch('mybib.web.api.references.Paper.fetch', autospec=True)
def test_post(fetch_mock, client, auth_header):
    referee_mock = MagicMock()
    referenced_mock = MagicMock()
    fetch_mock.side_effect = [referee_mock, referenced_mock]

    id1 = 'id1'
    id2 = 'id2'
    expected = {'a': 'reference'}
    with patch('mybib.web.authentication.check_auth') as check_auth:
        check_auth.return_value = True

        response = client.post(f'/api/references/{id1}/{id2}', data=json.dumps(expected),
                               headers=auth_header,
                               content_type='application/json')

        referee_mock.references.add.assert_called_once_with(referenced_mock, expected)
        assert response.status_code == 201
