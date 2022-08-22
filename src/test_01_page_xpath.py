import pytest
import requests
from lxml import etree
from lib.chrome_worker import GiteaChromeAction


def test_0100_gitea_init(config, docker_container, chrome_worker):
    gitea_worker = GiteaChromeAction(chrome_worker, config.get("gitea_base_url"))
    is_success = gitea_worker.gitea_init()
    assert is_success


def test_0101_gitea_main_page_status_code(config, docker_container):
    response = requests.get(config.get("gitea_base_url"))
    assert response.status_code == 200


gitea_main_page_element_count_parameter_list = [
    ("//img[@class='ui mini image']", 1),
    ("//img[@class='logo']", 1),
    ("//a[@href='/api/swagger']", 1),
    ("//div", 23),
    ("/html/body", 1),
    ("//h1[text()[contains(.,'Gitea')]]", 1),
]


@pytest.mark.parametrize("xpath_query, element_count", gitea_main_page_element_count_parameter_list)
def test_0102_gitea_main_page_element_count(config, docker_container, xpath_query, element_count):
    response = requests.get(config.get("gitea_base_url"))
    html_parser = etree.HTMLParser()
    page_tree = etree.fromstring(response.text, html_parser)
    element_list = page_tree.xpath(xpath_query)
    assert len(element_list) == element_count


gitea_main_page_element_text_parameter_list = [
    ("(//h1[@class='hero ui icon header'])[1]/text()[2]", "Easy to install"),
    ("(//h1[@class='hero ui icon header'])[2]/text()[2]", "Cross-platform"),
    ("(//h1[@class='hero ui icon header'])[3]/text()[2]", "Lightweight"),
    ("(//h1[@class='hero ui icon header'])[4]/text()[2]", "Open Source")
]


@pytest.mark.parametrize("xpath_query, element_text", gitea_main_page_element_text_parameter_list)
def test_0103_gitea_main_page_element_text(config, docker_container, xpath_query, element_text):
    response = requests.get(config.get("gitea_base_url"))
    html_parser = etree.HTMLParser()
    page_tree = etree.fromstring(response.text, html_parser)
    element_list = page_tree.xpath(xpath_query)
    assert element_list[0].strip() == element_text
