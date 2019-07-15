from unittest.mock import Mock

validate_indexes = Mock()


def test_get_identifier(client):
    expected = {"nodes": [], "references": []}
    return_value = ([], [])
