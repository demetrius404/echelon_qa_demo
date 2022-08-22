## Тестовое задание (QA Engineer) в компанию [АО "НПО Эшелон"](https://npo-echelon.ru)

Исходное тестовое задание в [файле](./TECH.md)   
Предварительно необходимо [скачать](https://chromedriver.chromium.org/downloads) WebDriver для Chrome
- [Файл](src/config/main.json) конфигурации
- Директория для драйвера `src/bin`

```text
$ git clone <REPO_URL>
$ cd ./<LOCAL_DIR>

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ pytest -v src/test_00_docker.py
$ pytest -v src/test_01_page_xpath.py 
$ pytest -v src/test_02_selenium_action.py
```

### Логотип в стиле ASCII art 
```text
0010001001001000100100101
00                   0110
01   10101010101000    10
011           001110   01
001001010110   0001010101
101                   010
100101010001   0010    10
010           101010   00
01   00101001000100    10
10                   0100
0100100101101100000100100
```

### Наборы тестов
- `src/test_00_docker.py` - тесты запуска `Docker` контейнера `Gitea`
- `src/test_01_page_xpath.py` - тестирование и поиск элементов с помощью `XPath` на странице
- `src/test_02_selenium_action.py` - целевые действия в `Gitea` и их проверка с помощью `Selenium`

### Fixture (pytest)
Общие `fixture` в файле `src/conftest.py` (имя зарезервировано `pytest`)

- `config` - конфигурация тестов (общие переменные)
- `docker_container` - запуск / остановка контейнера с `Gitea` 
- `chrome_worker` - управление `ChromeBrowser` на базе `Selenium`  

### Запуск тестов
```text
$ pytest
=== test session starts ===
platform darwin -- Python 3.9.6, pytest-7.1.2, pluggy-1.0.0
rootdir: ...
collected 20 items

0010001001001000100100101
00                   0110
01   10101010101000    10
011           001110   01
001001010110   0001010101
101                   010
100101010001   0010    10
010           101010   00
01   00101001000100    10
10                   0100
0100100101101100000100100

src/test_00_docker.py ...                   [ 15%]
src/test_01_page_xpath.py ............      [ 75%]
src/test_02_selenium_action.py .....        [100%]
```

```text
$ pytest -v src/test_00_docker.py
====== test session starts ======
platform darwin -- Python 3.9.6, pytest-7.1.2, pluggy-1.0.0
rootdir: ...
collected 3 items

src/test_00_docker.py::test_0000_docker_image_gitea_exist         PASSED    [ 33%]
src/test_00_docker.py::test_0001_docker_container_gitea_exist     PASSED    [ 66%]
src/test_00_docker.py::test_0002_docker_container_gitea_status    PASSED    [100%]

====== 3 passed ======
```

```text
$ pytest -v src/test_01_page_xpath.py 
====== test session starts ======
platform darwin -- Python 3.9.6, pytest-7.1.2, pluggy-1.0.0
rootdir: ...
collected 12 items

src/test_01_page_xpath.py::test_0100_gitea_init                                PASSED    [  8%]
src/test_01_page_xpath.py::test_0101_gitea_main_page_status_code               PASSED    [ 16%]
src/test_01_page_xpath.py::test_0102_gitea_main_page_element_count[<XPATH>]    PASSED    [ 25%]
src/test_01_page_xpath.py::test_0102_gitea_main_page_element_count[<XPATH>]    PASSED    [ 33%]
src/test_01_page_xpath.py::test_0102_gitea_main_page_element_count[<XPATH>]    PASSED    [ 41%]
src/test_01_page_xpath.py::test_0102_gitea_main_page_element_count[<XPATH>]    PASSED    [ 50%]
src/test_01_page_xpath.py::test_0102_gitea_main_page_element_count[<XPATH>]    PASSED    [ 58%]
src/test_01_page_xpath.py::test_0102_gitea_main_page_element_count[<XPATH>]    PASSED    [ 66%]
src/test_01_page_xpath.py::test_0103_gitea_main_page_element_text[<XPATH>]     PASSED    [ 75%]
src/test_01_page_xpath.py::test_0103_gitea_main_page_element_text[<XPATH>]     PASSED    [ 83%]
src/test_01_page_xpath.py::test_0103_gitea_main_page_element_text[<XPATH>]     PASSED    [ 91%]
src/test_01_page_xpath.py::test_0103_gitea_main_page_element_text[<XPATH>]     PASSED    [100%]

====== 12 passed ======
```

```text
$ pytest -v src/test_02_selenium_action.py
====== test session starts ======
platform darwin -- Python 3.9.6, pytest-7.1.2, pluggy-1.0.0
rootdir: ...
collected 5 items

src/test_02_selenium_action.py::test_0200_gitea_init                  PASSED    [ 20%]
src/test_02_selenium_action.py::test_0201_gitea_user_create           PASSED    [ 40%]
src/test_02_selenium_action.py::test_0202_gitea_repo_create           PASSED    [ 60%]
src/test_02_selenium_action.py::test_0203_gitea_commit_upload_file    PASSED    [ 80%]
src/test_02_selenium_action.py::test_0204_gitea_content_compare       PASSED    [100%]

====== 5 passed ======
```

### Запуск временного контейнера
```text
docker run \
--rm \
--name gitea \
--publish 8080:3000 \
gitea/gitea:1.16.9
```
