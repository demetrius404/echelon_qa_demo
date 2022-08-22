import pytest
import docker


@pytest.fixture
def docker_client():
    return docker.from_env()


def test_0000_docker_image_gitea_exist(config, docker_container, docker_client):
    docker_image_list = docker_client.images.list(name=config.get("docker_image"))
    assert len(docker_image_list) == 1


def test_0001_docker_container_gitea_exist(config, docker_container, docker_client):
    container_strict_name = "^{0}$".format(config.get("docker_container"))
    container_list = docker_client.containers.list(filters={"name": container_strict_name}, all=True)
    assert len(container_list) == 1


def test_0002_docker_container_gitea_status(config, docker_container, docker_client):
    container_gitea = docker_client.containers.get(config.get("docker_container"))
    assert container_gitea.status == "running"
