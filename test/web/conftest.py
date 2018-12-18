from unittest.mock import patch

import pytest

from mybib.web.app import app


@pytest.fixture
def client():
    with patch('mybib.neo4j.validate_indexes'):
        return app.test_client()
