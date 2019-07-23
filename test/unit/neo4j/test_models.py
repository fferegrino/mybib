import os
from pathlib import Path
from urllib.parse import urlparse

import pytest

from mybib.neo4j.models import Paper, refresh_graph, Author

RUNNING_IN_CIRCLECI = bool(os.getenv("CIRCLECI", False))


def clean_none(kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return [Path(pytestconfig.rootdir, "docker", "docker-compose.neo4j.yml")]

@pytest.fixture
def graph_refresher():
    yield True
    refresh_graph()

@pytest.mark.skipif(
    RUNNING_IN_CIRCLECI, reason="I have not set this up properly in Circle Ci"
)
class TestDbInteraction:


    @pytest.mark.parametrize("populate_scripts", [["insert_papers"]], indirect=True)
    def test_get_all_papers(self, neo4j, all_papers, graph_refresher):
        os.environ["NEO4J_HOST"] = neo4j.hostname
        os.environ["NEO4J_PORT"] = str(neo4j.port)
        os.environ["NEO4J_USER"] = "neo4j"
        os.environ["NEO4J_PASS"] = "neo4j_generic"

        r = Paper().all()
        actual = sorted(
            [clean_none(record.asdict()) for record in r],
            key=lambda record: record["ID"],
        )

        assert actual == sorted(all_papers, key=lambda record: record["ID"])

    def test_isolation(self, neo4j, graph_refresher):
        os.environ["NEO4J_HOST"] = neo4j.hostname
        os.environ["NEO4J_PORT"] = str(neo4j.port)
        os.environ["NEO4J_USER"] = "neo4j"
        os.environ["NEO4J_PASS"] = "neo4j_generic"

        r = Author().all()
        import pdb; pdb.set_trace()
        actual = sorted(
            [clean_none(record.asdict()) for record in r],
            key=lambda record: record["ID"],
        )

        assert len(actual) == 0
