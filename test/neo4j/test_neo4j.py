from copy import deepcopy
from unittest.mock import patch, MagicMock

from mybib.neo4j import validate_indexes, EXPECTED_INDEXES, insert_reference, insert_paper, insert_keyword, \
    insert_author


def mock_run(mock_driver):
    run_mock = MagicMock()
    enter_mock = MagicMock()
    enter_mock.run = MagicMock(return_value=run_mock)
    context_mgr_mock = MagicMock()

    context_mgr_mock.__enter__.return_value = enter_mock
    session_mock = MagicMock(return_value=context_mgr_mock)

    mock_driver.session = session_mock

    return run_mock, enter_mock, context_mgr_mock, session_mock


@patch('mybib.neo4j.DRIVER')
def test_validate_indexes(mock_driver):
    run_mock, enter_mock, context_mgr_mock, session_mock = mock_run(mock_driver)
    validate_indexes()

    calls = enter_mock.mock_calls

    for index, call in zip(EXPECTED_INDEXES, calls):
        assert call[0] == 'run'
        assert call[1][0] == f'CREATE INDEX ON :{index.node}({index.field})'


@patch('mybib.neo4j.DRIVER')
def test_insert_reference(mock_driver):
    run_mock, enter_mock, context_mgr_mock, session_mock = mock_run(mock_driver)

    expected_insertion_return = {'return': 'value'}
    run_mock.single.return_value = {'r': expected_insertion_return}

    identifier1 = 'A1'
    identifier2 = 'A2'
    attr_dict = {'k1': 'k2'}

    attributes = ', '.join([f'{k}:"{attr_dict[k]}"' for k in attr_dict])

    actual_insertion_return = insert_reference(identifier1, identifier2, attr_dict)
    [match_call] = enter_mock.mock_calls

    assert match_call[0] == 'run'
    assert match_call[1][0] == f'MATCH (referee:Paper{{ID:"{identifier1}"}}), ' \
                               f'(referenced:Paper{{ID:"{identifier2}"}}) ' \
                               f'CREATE (referee)-[r:REFERENCES {{{attributes}}}]->(referenced) ' \
                               'RETURN r'
    assert actual_insertion_return == expected_insertion_return


@patch('mybib.neo4j.DRIVER')
@patch('mybib.neo4j.time', return_value=1545334834)
def test_insert_paper(mock_time, mock_driver):
    run_mock, enter_mock, context_mgr_mock, session_mock = mock_run(mock_driver)

    expected_insertion_return = {'return': 'value'}
    run_mock.single.return_value = {'r': expected_insertion_return}

    input_dict = {'k1': 'k2', 'k3': 'v2'}
    transformed_dict = deepcopy(input_dict)
    transformed_dict['_time'] = 1545334834

    attributes = ', '.join([f'{k}:"{transformed_dict[k]}"' for k in transformed_dict])

    insert_paper(input_dict)
    [match_call] = enter_mock.mock_calls

    assert match_call[0] == 'run'
    assert match_call[1][0] == 'CREATE (x:Paper {' + attributes + '})'


@patch('mybib.neo4j.DRIVER')
@patch('mybib.neo4j.time', return_value=1545334834)
def test_insert_keyword(mock_time, mock_driver):
    run_mock, enter_mock, context_mgr_mock, session_mock = mock_run(mock_driver)

    keyword = 'neo4j'

    insert_keyword(keyword)
    [match_call] = enter_mock.mock_calls

    assert match_call[0] == 'run'
    assert match_call[1][0] == 'CREATE (x:Keyword {value:"neo4j", _time:"1545334834"})'


@patch('mybib.neo4j.DRIVER')
@patch('mybib.neo4j.time', return_value=1545334834)
def test_insert_author(mock_time, mock_driver):
    run_mock, enter_mock, context_mgr_mock, session_mock = mock_run(mock_driver)

    author = 'Cosme Fulanito'

    insert_author(author)
    [match_call] = enter_mock.mock_calls

    assert match_call[0] == 'run'
    assert match_call[1][0] == 'CREATE (x:Author {name:"Cosme Fulanito", _time:"1545334834"})'
