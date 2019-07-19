from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def docker_compose_files(pytestconfig):
    """Get the docker-compose.yml absolute path.
    Override this fixture in your tests if you need a custom location.
    """
    return [Path(pytestconfig.rootdir, "docker", "docker-compose.neo4j.yml")]


def test_a(docker_neo4j):
    assert 1 == 1
