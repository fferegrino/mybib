import json
from unittest.mock import patch, Mock, MagicMock

validate_indexes = Mock()


def test_get_two_identifiers(client):
    id1 = 'id1'
    id2 = 'id2'
    expected = {'a': 'reference'}


@patch('mybib.web.api.references.Paper.fetch', autospec=True)
@patch('mybib.web.api.references.are_related', autospec=True, return_value=False)
def test_post_inserts(are_related_mock, fetch_mock, client, auth_header):
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
        are_related_mock.assert_called_once_with(id1, id2)
        referee_mock.references.add.assert_called_once_with(referenced_mock, expected)
        assert response.status_code == 201


@patch('mybib.web.api.references.Paper.fetch', autospec=True)
@patch('mybib.web.api.references.are_related', autospec=True, return_value=True)
def test_post_already_exists(are_related_mock, fetch_mock, client, auth_header):
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
        are_related_mock.assert_called_once_with(id1, id2)
        assert not referee_mock.references.add.called
        assert response.status_code == 409
