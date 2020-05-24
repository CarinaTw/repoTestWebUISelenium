# 1. Написать тесты проверяющие наличие элементов на разных страницах приложения opencart.
# 2. Реализовать минимум пять тестов (одни тест = одна страница приложения)
# 3. Какие элементы проверять определить самостоятельно, но не меньше 5 для каждой страницы.
#http://localhost
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
import pytest
import re
from page import Page


class MainPage(Page):
    def __init__(self, driver):
        page = Page(driver)
        self.url = page.url
        self.driver = page.driver


def test_opencart_main_page_title(driver_factory):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    assert main_page.driver.title == 'Your Store'


@pytest.mark.parametrize("searched", ['ipone', 'sumsung'])
def test_opencart_main_page_search_field_exist(driver_factory, searched):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    elem = main_page.driver.find_element(By.XPATH, "//input[@name='search']")
    elem.click()
    elem.send_keys(searched)
    elem.send_keys(Keys.ENTER)
    assert main_page.driver.title == 'Search - {}'.format(searched)
    assert main_page.driver.current_url == 'http://localhost/index.php?route=product/search&search={}'.format(searched)


def test_opencart_main_page_search_button_exist(driver_factory):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    elem = main_page.driver.find_element(By.XPATH, "//div[@id='search']//button[@type='button']")
    elem.click()
    sleep(2)
    el_text = main_page.driver.find_element(By.XPATH, "//div[@id='content']//p[2]")
    assert el_text.text == 'There is no product that matches the search criteria.'


def test_opencart_main_page_slideshow_exist(driver_factory):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    elem = main_page.driver.find_element(By.ID, "slideshow0")
    elem.click()

    prod_url = main_page.driver.current_url
    str_prod = re.findall('product_id=\d*', prod_url)
    s = re.split(r'=', str_prod[0])[1]

    assert main_page.driver.find_element(By.XPATH, "//div[@id='product']//input[@name='product_id'][@value=%s]" % s), \
        'Product with id={} is not found'.format(s)
