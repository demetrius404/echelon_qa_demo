import docker
import pytest
from lib.docker_runtime_exception import DockerRuntimeError
from lib.chrome_worker import ChromeWorker
from pathlib import Path
import time
import json


@pytest.fixture(scope="module")
def config():

    base_dir = Path(__file__).parent.parent
    with open(base_dir.joinpath("src/config/main.json"), "r", encoding="utf-8") as file:
        main_config = json.load(file)

    main_config.update({"selenium_bin_path": str(base_dir.joinpath(main_config.get("selenium_bin_path")))})
    main_config.get("test_case").update({"upload_dir": str(base_dir)})

    return main_config


@pytest.fixture(scope="module")
def docker_container(config):
    # setup
    client = docker.from_env()
    property_dict = {
        "detach": True,
        "remove": True,
        "name": config.get("docker_container"),
        "ports": {"3000/tcp": 8080}
    }
    container = client.containers.run(config.get("docker_image"), **property_dict)
    if container.status != "running":
        container.start()

        time_elapsed = 0
        while container.status != "running" and time_elapsed <= config.get("time_wait_container_start"):
            # refresh docker container status
            container = client.containers.get(config.get("docker_container"))
            time.sleep(1)
            time_elapsed += 1

    # refresh docker container status
    container = client.containers.get(config.get("docker_container"))
    if container.status != "running":
        raise DockerRuntimeError("docker container still not running")

    # just in case
    time.sleep(config.get("time_wait_container_after_start"))

    yield

    # teardown
    container.stop()


@pytest.fixture(scope="module")
def chrome_worker(config):
    chrome_worker = ChromeWorker(config.get("selenium_bin_path"))
    yield chrome_worker
    chrome_worker.quit()
