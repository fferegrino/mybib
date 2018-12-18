import base64
import json
from copy import deepcopy
from unittest.mock import patch, Mock

import pytest

from mybib.web.app import app

validate_indexes = Mock()


@pytest.fixture
def sample_bibtex():
    return """@inproceedings{Petrovski:2017:EAP:3106426.3106449,
 author = {Petrovski, Petar and Bizer, Christian},
 title = {Extracting Attribute-value Pairs from Product Specifications on the Web},
 booktitle = {Proceedings of the International Conference on Web Intelligence},
 series = {WI '17},
 year = {2017},
 isbn = {978-1-4503-4951-2},
 location = {Leipzig, Germany},
 pages = {558--565},
 numpages = {8},
 url = {http://doi.acm.org/10.1145/3106426.3106449},
 doi = {10.1145/3106426.3106449},
 acmid = {3106449},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {feature extraction, product data, schema matching, web tables},
}"""


@pytest.fixture
def sample_json():
    return [
        {
            "keywords": [
                "feature extraction",
                "product data",
                "schema matching",
                "web tables"
            ],
            "address": "New York, NY, USA",
            "publisher": "ACM",
            "acmid": "3106449",
            "doi": "10.1145/3106426.3106449",
            "url": "http://doi.acm.org/10.1145/3106426.3106449",
            "numpages": "8",
            "pages": "558--565",
            "location": "Leipzig, Germany",
            "isbn": "978-1-4503-4951-2",
            "year": "2017",
            "series": "WI '17",
            "booktitle": "Proceedings of the International Conference on Web Intelligence",
            "title": "Extracting Attribute-value Pairs from Product Specifications on the Web",
            "author": [
                "Petrovski, Petar",
                "Bizer, Christian"
            ],
            "ENTRYTYPE": "inproceedings",
            "ID": "Petrovski:2017:EAP:3106426.3106449",
            "link": [
                {
                    "url": "http://dx.doi.org/10.1145/3106426.3106449",
                    "anchor": "doi"
                }
            ]
        }
    ]


@pytest.fixture
def client():
    with patch('mybib.neo4j.validate_indexes'):
        return app.test_client()


def test_get_two_identifiers(client):
    id1 = 'id1'
    id2 = 'id2'
    expected = {'a':'reference'}
    with patch('mybib.web.api.references.get_reference_neo4j', return_value={'a': 'reference'}) as get_reference:
        response = client.get(f'/api/references/{id1}/{id2}')
        actual = json.loads(response.get_data(as_text=True))
        get_reference.assert_called_with(id1, id2)
    assert expected == actual


@patch('mybib.web.api.references.insert_reference')
def test_post(insert_reference_mock, client):
    id1 = 'id1'
    id2 = 'id2'
    expected = {'a':'reference'}
    with patch('mybib.web.authentication.check_auth') as check_auth:
        check_auth.return_value = True

        valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
        response = client.post(f'/api/references/{id1}/{id2}', data=json.dumps(expected),
                               headers={'Authorization': 'Basic ' + valid_credentials},
                               content_type='application/json')

        assert response.status_code == 201
        insert_reference_mock.assert_called_with(id1, id2, expected)
