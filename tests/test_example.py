import time


def test_yandex_0(browser):
    browser.get("https://ya.ru")
    browser.find_element_by_id("text")
    browser.find_element_by_css_selector("a[title='Яндекс']")
    assert browser.title == "Яндекс"
    time.sleep(2)


def test_avito_0(browser):
    browser.get("https://avito.ru")
    browser.find_element_by_id("category")
    browser.find_element_by_id("search")
    assert "Авито" in browser.title
    time.sleep(2)


def test_yandex_1(browser):
    browser.get("https://ya.ru")
    browser.find_element_by_id("text")
    browser.find_element_by_css_selector("a[title='Яндекс']")
    assert browser.title == "Яндекс"
    time.sleep(2)


def test_avito_1(browser):
    browser.get("https://avito.ru")
    browser.find_element_by_id("category")
    browser.find_element_by_id("search")
    assert "Авито" in browser.title
    time.sleep(2)


def test_yandex_2(browser):
    browser.get("https://ya.ru")
    browser.find_element_by_id("text")
    browser.find_element_by_css_selector("a[title='Яндекс']")
    assert browser.title == "Яндекс"
    time.sleep(2)


def test_avito_2(browser):
    browser.get("https://avito.ru")
    browser.find_element_by_id("category")
    browser.find_element_by_id("search")
    assert "Авито" in browser.title
    time.sleep(2)