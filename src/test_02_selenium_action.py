from lib.chrome_worker import GiteaChromeAction


def test_0200_gitea_init(config, docker_container, chrome_worker):
    gitea_worker = GiteaChromeAction(chrome_worker, config.get("gitea_base_url"))
    is_success = gitea_worker.gitea_init()
    assert is_success


def test_0201_gitea_user_create(config, docker_container, chrome_worker):
    gitea_worker = GiteaChromeAction(chrome_worker, config.get("gitea_base_url"))
    is_success = gitea_worker.user_create(config.get("test_case"))
    assert is_success


def test_0202_gitea_repo_create(config, docker_container, chrome_worker):
    # user already login on previous step
    gitea_worker = GiteaChromeAction(chrome_worker, config.get("gitea_base_url"))
    is_success = gitea_worker.repo_create(config.get("test_case"))
    assert is_success


def test_0203_gitea_commit_upload_file(config, docker_container, chrome_worker):
    gitea_worker = GiteaChromeAction(chrome_worker, config.get("gitea_base_url"))
    is_success = gitea_worker.commit_upload_file(config.get("test_case"))
    assert is_success


def test_0204_gitea_content_compare(config, docker_container, chrome_worker):
    gitea_worker = GiteaChromeAction(chrome_worker, config.get("gitea_base_url"))
    gitea_content = gitea_worker.content_raw_file(config.get("test_case"))
    is_equal = GiteaChromeAction.is_content_equal(gitea_content, config.get("test_case"))
    assert is_equal
