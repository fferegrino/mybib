import os
from pathlib import Path
from urllib.parse import urlparse

import pytest

from mybib.neo4j.models import Paper


def clean_none(kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return [Path(pytestconfig.rootdir, "docker", "docker-compose.neo4j.yml")]


@pytest.mark.parametrize("populate_scripts", [["insert_papers"]], indirect=True)
def test_get_all_papers(neo4j, all_papers):
    os.environ["NEO4J_HOST"] = neo4j.hostname
    os.environ["NEO4J_PORT"] = str(neo4j.port)
    os.environ["NEO4J_USER"] = "neo4j"
    os.environ["NEO4J_PASS"] = "neo4j_generic"

    r = Paper().all()
    actual = sorted(
        [clean_none(record.asdict()) for record in r], key=lambda record: record["ID"]
    )

    assert actual == sorted(all_papers, key=lambda record: record["ID"])
