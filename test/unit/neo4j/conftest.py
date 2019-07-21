from pathlib import Path
from urllib.parse import urlparse

import pytest
import requests

from .json_fixtures import *


def execute(docker_services, service, *cmd):
    command = ["exec", "-T", service, " ".join(*cmd)]
    to_execute = " ".join(command)
    docker_services._docker_compose.execute(to_execute)


@pytest.fixture
def docker_neo4j(docker_ip, docker_services):
    port = docker_services.port_for("neo4j", 7687)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


def is_responsive(url):
    """Check if something responds to ``url``."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False


@pytest.fixture(params=[""])
def populate_scripts(request):
    if not request.param:
        raise NotImplementedError("override this in your test")
    return request.param


@pytest.fixture
def neo4j(pytestconfig, docker_neo4j, populate_scripts, docker_services):
    for script in populate_scripts:
        file = Path(pytestconfig.rootdir, "test", "cypher_scripts", f"{script}.cypher")
        with open(file) as r:
            cypher_command = " ".join(r.read().split("\n")).replace('"', '\\"')
            execute(docker_services, "neo4j", ["cypher-shell", f'"{cypher_command}"'])
    url = urlparse(docker_neo4j)
    return url
