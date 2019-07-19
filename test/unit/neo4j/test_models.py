import os
from pathlib import Path

import pytest

from mybib.neo4j.models import Paper

from .json_fixtures import all_papers


def clean_none(kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


@pytest.fixture(scope="session")
def docker_compose_files(pytestconfig):
    return [Path(pytestconfig.rootdir, "docker", "docker-compose.neo4j.yml")]


def test_a(populate_neo4j, all_papers):
    url = populate_neo4j(["insert_papers"])
    host, port = url.split(":")
    os.environ["NEO4J_URL"] = host
    os.environ["NEO4J_PORT"] = port
    os.environ["NEO4J_USER"] = "neo4j"
    os.environ["NEO4J_PASS"] = "neo4j_generic"

    r = Paper().all()
    actual = sorted(
        [clean_none(record.asdict()) for record in r], key=lambda record: record["ID"]
    )

    assert actual == sorted(all_papers, key=lambda record: record["ID"])
