"""
Настройка окружения, первый тест
(*)
1. Установить OpenCart по инструкции
2. Настроить selenium для запуска тестов

1. Написать фикстуру для запуска трех разных браузеров (ie, firefox, chrome) в полноэкранном режиме с опцией headless.
Выбор браузера должен осуществляться путем передачи аргумента командной строки pytest.
По завершению работы тестов должно осуществляться закрытие браузера.

2. Добавить опцию командной строки, которая указывает базовый URL opencart.

3. Написать тест, который открывает основную страницу opencart (http://<ip_or_fqdn>/opencart/) и проверяет,
что мы находимся именно на странице приложения opencart.

Критерии оценки:
(*) Скриншот работающего opencart
(**) В качестве решения прислать ссылку на коммит и скриншот с успешным запуском тестов.

"""


def test_opencart_title(browser):
    browser.get("http://127.0.0.1/")
    assert browser.title == 'Your Store'

