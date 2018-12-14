from neo4j import GraphDatabase
from time import time
import os

URI = os.getenv('NEO4J_URL')
USER = os.getenv('NEO4J_USER')
PASS = os.getenv('NEO4J_PASS')
DRIVER = GraphDatabase.driver(URI, auth=(USER, PASS))


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