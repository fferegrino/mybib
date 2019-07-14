import base64

import pytest

from mybib.web.app import app


@pytest.fixture(scope="session", autouse=True)
def patch_neo4j(request):
    def unpatch():
        pass

    request.addfinalizer(unpatch)


@pytest.fixture
def auth_header():
    valid_credentials = base64.b64encode(b"testuser:testpassword").decode("utf-8")
    return {"Authorization": "Basic " + valid_credentials}


@pytest.fixture
def client():
    return app.test_client()
