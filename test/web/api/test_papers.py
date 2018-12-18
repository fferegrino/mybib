import unittest
from unittest.mock import patch, Mock
from mybib.web import app


validate_indexes = Mock()


@patch('mybib.neo4j.validate_indexes', new=validate_indexes)
class PapersApiTestCase(unittest.TestCase):

    def setUp(self):
        print(validate_indexes)

    def test_something(self):
        return True