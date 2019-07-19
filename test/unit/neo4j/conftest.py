from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def docker_neo4j(docker_services):
    docker_services.start("neo4j")
    # Make neo4j read files from anywhere
    docker_services.execute(
        "neo4j",
        "sed",
        "-ie",
        "s/dbms\.directories\.import\=import/dbms\.directories\.import\=/g",
        "conf/neo4j.conf",
    )
    public_port = docker_services.wait_for_service("neo4j", 7687)
    dsn = "{docker_services.docker_ip}:{public_port}".format(**locals())

    return dsn


@pytest.fixture(scope="session")
def populate_neo4j(pytestconfig, docker_neo4j, docker_services):
    def f(cyphers):
        for script in cyphers:
            file = Path(
                pytestconfig.rootdir, "test", "cypher_scripts", f"{script}.cypher"
            )
            with open(file) as r:
                command = " ".join(r.read().split("\n"))
                docker_services.execute("neo4j", "cypher-shell", f"{command}")
        return docker_neo4j

    return f
