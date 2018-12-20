import os
from collections import namedtuple
from time import time

from neo4j import GraphDatabase

URI = os.getenv('GRAPHENEDB_BOLT_URL')
USER = os.getenv('GRAPHENEDB_BOLT_USER')
PASS = os.getenv('GRAPHENEDB_BOLT_PASSWORD')
DRIVER = None


def init_driver():
    global DRIVER
    DRIVER = GraphDatabase.driver(URI, auth=(USER, PASS))


Index = namedtuple('Index', ['node', 'field'])


EXPECTED_INDEXES = [
    Index('Keyword', 'value'),
    Index('Paper', 'ID'),
    Index('Author', 'name'),
    Index('Investigation', 'title'),
]


def validate_indexes():
    with DRIVER.session() as session:
        for index in EXPECTED_INDEXES:
            session.run(f'CREATE INDEX ON :{index.node}({index.field})')


def get_paper(identifier):
    return _get_node('Paper', identifier)


def _get_node(label, identifier):
    with DRIVER.session() as session:
        result = session.run(f'MATCH (x:{label}) '
                             f'WHERE x.ID="{identifier}" '
                             'RETURN x')
        single_result = result.single()
        return dict(single_result['x'])


def insert_paper(attr_dict):
    return _insert_node('Paper', attr_dict)


def _insert_node(label, attr_dict):
    with DRIVER.session() as session:
        query = f'CREATE (x:{label} {{'
        attr_dict['_time'] = int(time())
        query += ', '.join([f'{k}:"{attr_dict[k]}"' for k in attr_dict]) + '})'
        return session.run(query)


def insert_reference(referee_id, referenced_id, attr_dict):
    attributes = ', '.join([f'{k}:"{attr_dict[k]}"' for k in attr_dict])
    query = f'MATCH (referee:Paper{{ID:"{referee_id}"}}), ' \
            f'(referenced:Paper{{ID:"{referenced_id}"}}) ' \
            f'CREATE (referee)-[r:REFERENCES {{{attributes}}}]->(referenced) ' \
            'RETURN r'

    with DRIVER.session() as session:
        result = session.run(query)
        single_result = result.single()
        return dict(single_result['r'])


def get_reference(referee_id, referenced_id):
    query = f'MATCH (referee:Paper{{ID:"{referee_id}"}})' \
            f'-[r:REFERENCES]->' \
            f'(referenced:Paper{{ID:"{referenced_id}"}})' \
            'RETURN r'

    with DRIVER.session() as session:
        result = session.run(query)
        single_result = result.single()
        return dict(single_result['r'])


def search_papers(title):
    with DRIVER.session() as sess:
        results = sess.run(f'MATCH (p:Paper) WHERE p.title=~".*{title}.*" RETURN p')
        return [dict(record['p']) for record in results]


def recent_papers_and_references():
    nodes = {}
    references = []
    with DRIVER.session() as sess:
        results = sess.run('MATCH (referee:Paper) '
                           'OPTIONAL MATCH (referee)-[reference:REFERENCES]->(referenced:Paper) '
                           'RETURN referee,reference,referenced ORDER BY referee._time DESC LIMIT 25')
        for r00 in results:
            dictionary = dict(r00)
            referee = dict(dictionary['referee'])
            nodes[referee['ID']] = referee

            referenced = dictionary.get('referenced')
            if referenced:
                referenced = dict(referenced)
                nodes[referenced['ID']] = referenced

                reference = dict(dictionary['reference'])
                reference['to'] = referenced['ID']
                reference['from'] = referee['ID']
                references.append(reference)

        return list(nodes.values()), references
