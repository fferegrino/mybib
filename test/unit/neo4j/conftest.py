from pathlib import Path
from urllib.parse import urlparse

import pytest
import requests

from .json_fixtures import *


def execute(docker_services, service, *cmd):
    command = ["exec", "-T", service, " ".join(*cmd)]
    to_execute = " ".join(command)
    docker_services._docker_compose.execute(to_execute)


@pytest.fixture(scope="session")
def docker_neo4j(docker_ip, docker_services):
    port_browser = docker_services.port_for("neo4j", 7474)
    port_bolt = docker_services.port_for("neo4j", 7687)
    url = f"http://{docker_ip}:{port_browser}"
    docker_services.wait_until_responsive(
        timeout=180.0, pause=0.1, check=lambda: is_responsive(url)
    )
    # Service is alive... let's kill it!
    execute(docker_services, 'neo4j', ['neo4j', 'stop'])
    docker_services.wait_until_responsive(
        timeout=180.0, pause=0.1, check=lambda: is_responsive_reverse(url)
    )
    bolt_url = f"http://{docker_ip}:{port_bolt}"
    browser_url = f"http://{docker_ip}:{port_browser}"
    return bolt_url, browser_url


def is_responsive(url):
    """Check if something responds to ``url``."""
    try:
        response = requests.get(url)
        print(f'Cheching at {url}')
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False


def is_responsive_reverse(url):
    """Check if something responds to ``url``."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return False
    except requests.exceptions.ConnectionError:
        return True


@pytest.fixture(params=[""])
def populate_scripts(request):
    return request.param


@pytest.fixture
def neo4j(pytestconfig, docker_neo4j, populate_scripts, docker_services):
    bolt_url, browser_url = docker_neo4j
    execute(docker_services, 'neo4j', ['neo4j', 'start'])
    docker_services.wait_until_responsive(
        timeout=180.0, pause=0.1, check=lambda: is_responsive(browser_url)
    )
    for script in populate_scripts:
        file = Path(pytestconfig.rootdir, "test", "cypher_scripts", f"{script}.cypher")
        with open(file) as r:
            print(f"Executing {file}")
            cypher_command = " ".join(r.read().split("\n")).replace('"', '\\"')
            execute(docker_services, "neo4j", ["cypher-shell", f'"{cypher_command}"'])
    bolt_parsed_url = urlparse(bolt_url)
    yield bolt_parsed_url
    execute(docker_services, 'neo4j', ['neo4j', 'stop'])
    docker_services.wait_until_responsive(
        timeout=180.0, pause=0.1, check=lambda: is_responsive_reverse(browser_url)
    )
