import pytest


@pytest.fixture(scope="session")
def docker_neo4j(docker_services):
    docker_services.start("neo4j")
    public_port = docker_services.wait_for_service("neo4j", 7687)
    dsn = "{docker_services.docker_ip}:{public_port}".format(**locals())
    things =docker_services.execute("neo4j", "ls", "/cypher")
    return dsn
