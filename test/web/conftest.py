import base64
from unittest.mock import patch

import pytest

from mybib.web.app import app


@pytest.fixture(scope="session", autouse=True)
def patch_py2neo(request):
    init_driver = patch('mybib.web.app.init_graph')
    init_driver.__enter__()

    def unpatch():
        init_driver.__exit__()

    request.addfinalizer(unpatch)


@pytest.fixture(scope="session", autouse=True)
def patch_neo4j(request):
    def unpatch():
        pass

    request.addfinalizer(unpatch)


@pytest.fixture
def auth_header():
    valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
    return {'Authorization': 'Basic ' + valid_credentials}


@pytest.fixture
def client():
    return app.test_client()
