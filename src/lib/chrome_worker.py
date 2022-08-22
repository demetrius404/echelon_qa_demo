import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from typing import Tuple
from typing import Dict
from typing import Union
from typing_extensions import TypeAlias
from lxml import etree


Int: TypeAlias = int
Float: TypeAlias = float
Str: TypeAlias = str
Bool: TypeAlias = bool


class ChromeWorker:

    def __init__(self, driver_path: Path, window_size: Tuple[Int] = (1024, 768), implicitly_wait: Int = 20):

        self.driver_path = driver_path
        self.service = Service(str(self.driver_path))
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(*window_size)
        self.driver.implicitly_wait(implicitly_wait)

    def element_by_xpath(self, xpath_query: Str):
        return self.driver.find_element(By.XPATH, xpath_query)

    @staticmethod
    def sleep(value: Int):
        time.sleep(value)

    def quit(self):
        self.driver.quit()


class GiteaChromeAction:

    def __init__(self, worker: ChromeWorker, base_url: Str):
        self.worker = worker
        self.base_url = base_url

    def gitea_init(self, wait: Union[Int, Float] = 10) -> Bool:
        self.worker.driver.get(self.base_url)
        self.worker.sleep(wait)

        h3 = self.worker.element_by_xpath("//h3[1]")
        if h3.text != "Initial Configuration":
            return False

        button = self.worker.element_by_xpath("//button[@class='ui primary button']")
        if button.text == "Install Gitea":
            button.click()
        self.worker.sleep(wait)

        redirect_url = "http://localhost:3000/user/login"
        if self.worker.driver.current_url == redirect_url:
            return True
        else:
            return False

    def user_create(self, property_dict: Dict, wait: Union[Int, Float] = 2) -> Bool:

        required_keys = ["user_name", "email", "password"]
        for k in required_keys:
            if k not in property_dict:
                raise ValueError(f"required_key: {k}")

        self.worker.driver.get(f"{self.base_url}/user/sign_up")
        self.worker.sleep(wait * 5)

        element = self.worker.element_by_xpath("//input[@id='user_name']")
        element.send_keys(property_dict["user_name"])
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//input[@id='email']")
        element.send_keys(property_dict["email"])
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//input[@id='password']")
        element.send_keys(property_dict["password"])
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//input[@id='retype']")
        element.send_keys(property_dict["password"])
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//button[@class='ui green button']")
        element.click()

        self.worker.sleep(wait * 5)

        element = self.worker.element_by_xpath("//div[@class='ui positive message flash-success']")
        if element:
            return True
        else:
            return False

    def repo_create(self, property_dict: Dict, wait: Union[Int, Float] = 2) -> Bool:
        required_keys = ["repo_name"]
        for k in required_keys:
            if k not in property_dict:
                raise ValueError(f"required_key: {k}")

        self.worker.driver.get(f"{self.base_url}/repo/create")
        self.worker.sleep(wait * 5)

        element = self.worker.element_by_xpath("//input[@id='repo_name']")
        element.send_keys(property_dict["repo_name"])
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//input[@name='auto_init']")
        ActionChains(self.worker.driver).move_to_element(element).click().perform()
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//button[@class='ui green button']")
        element.click()

        self.worker.sleep(wait * 5)

        if self.worker.driver.current_url == "{0}/gitea/{1}".format(self.base_url, property_dict["repo_name"]):
            return True
        else:
            return False

    def logout(self, wait: Union[Int, Float] = 2):
        self.worker.driver.get(f"{self.base_url}/user/logout")
        self.worker.sleep(wait * 5)

    def login(self, property_dict: Dict, wait: Union[Int, Float] = 2) -> Bool:

        required_keys = ["user_name", "password"]
        for k in required_keys:
            if k not in property_dict:
                raise ValueError(f"required_key: {k}")

        self.worker.driver.get(f"{self.base_url}/user/login")
        self.worker.sleep(wait * 5)

        element = self.worker.element_by_xpath("//input[@id='user_name']")
        element.send_keys(property_dict["user_name"])
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//input[@id='password']")
        element.send_keys(property_dict["password"])
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//button[@class='ui green button']")
        element.click()

        self.worker.sleep(wait * 5)

        # logout href exist
        element = self.worker.element_by_xpath("//a[@data-url='/user/logout']")
        current_url = self.worker.driver.current_url.strip("/")
        if current_url == self.base_url and element.get_attribute("data-url") == "/user/logout":
            return True
        else:
            return False

    def commit_upload_file(self, property_dict: Dict, wait: Union[Int, Float] = 2) -> Bool:

        required_keys = ["repo_name", "upload_dir", "upload_file"]
        for k in required_keys:
            if k not in property_dict:
                raise ValueError(f"required_key: {k}")

        repo_name = property_dict["repo_name"]
        self.worker.driver.get(f"{self.base_url}/gitea/{repo_name}/_upload/master")
        self.worker.sleep(wait * 5)

        element = self.worker.element_by_xpath("//input[@name='commit_summary']")
        element.send_keys("upload_file: {0}".format(property_dict["upload_file"]))
        self.worker.sleep(wait)

        element = self.worker.element_by_xpath("//input[@class='dz-hidden-input']")

        upload_path = Path(property_dict["upload_dir"]).joinpath(property_dict["upload_file"])
        element.send_keys(str(upload_path))

        element = self.worker.element_by_xpath("//button[@class='ui green button']")
        element.click()

        self.worker.sleep(wait * 5)

        return True

    def content_raw_file(self, property_dict: Dict, wait: Union[Int, Float] = 2) -> Str:

        required_keys = ["repo_name", "upload_dir", "upload_file"]
        for k in required_keys:
            if k not in property_dict:
                raise ValueError(f"required_key: {k}")

        repo_name = property_dict["repo_name"]
        upload_file = property_dict["upload_file"]

        self.worker.driver.get(f"{self.base_url}/gitea/{repo_name}/raw/branch/master/{upload_file}")
        self.worker.sleep(wait * 5)

        html_parser = etree.HTMLParser()
        page_tree = etree.fromstring(self.worker.driver.page_source, html_parser)
        return page_tree.xpath("//pre[1]/text()")[0]

    @staticmethod
    def is_content_equal(remote_content: Str, property_dict: Dict) -> Bool:

        required_keys = ["upload_dir", "upload_file"]
        for k in required_keys:
            if k not in property_dict:
                raise ValueError(f"required_key: {k}")

        local_path = Path(property_dict["upload_dir"]).joinpath(property_dict["upload_file"])
        with open(local_path, "r", encoding="utf-8") as file:
            local_content = file.read()

        if remote_content == local_content:
            return True
        else:
            return False


if __name__ == "__main__":

    test_driver_path = Path(__file__).parent.parent.parent.joinpath("src/bin/chromedriver_v104.bin")
    test_base_url = "http://127.0.0.1:8080"

    chrome_worker = ChromeWorker(test_driver_path)
    gitea_worker = GiteaChromeAction(chrome_worker, test_base_url)

    gitea_property_dict = {
        "user_name": "gitea",
        "email": "gitea@local",
        "password": "QXpMvkPFmS",
        "repo_name": "test",
        "upload_dir": "/Users/User/PyCharmProjects/echelon_qa_demo",
        "upload_file": "TECH.md"
    }

    # print("gitea_sing_up:", gitea_sign_up(_worker, _url, _dict))

    print("gitea_login:", gitea_worker.login(gitea_property_dict))
    # print("gitea_repo_create:", gitea_worker.repo_create(gitea_property_dict))
    # print("gitea_commit_upload_file:", gitea_worker.commit_upload_file(gitea_property_dict))
    print("gitea_content ...")
    gitea_content = gitea_worker.content_raw_file(gitea_property_dict)
    is_equal = GiteaChromeAction.is_content_equal(gitea_content, gitea_property_dict)
    print("gitea_content:", is_equal)

    chrome_worker.sleep(10)
    chrome_worker.quit()


