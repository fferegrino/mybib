import base64
from unittest.mock import patch

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


@pytest.fixture
def authenticated_post(client, auth_header):
    def post(*args, **kwargs):
        kwargs["headers"] = auth_header
        return client.post(*args, **kwargs)

    with patch("mybib.web.authentication.check_auth") as check_auth:
        check_auth.return_value = True
        yield post
