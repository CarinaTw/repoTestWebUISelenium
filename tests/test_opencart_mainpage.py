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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class MainPage(Page):
    def __init__(self, driver):
        page = Page(driver)
        self.url = page.url
        self.driver = page.driver


def test_main_page_title(driver_factory):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    main_page.driver.implicitly_wait(1)  # неявное ожидание
    wait = WebDriverWait(driver_factory, 3)
    wait.until(EC.title_is('Your Store'))


@pytest.mark.parametrize("searched", ['ipone', 'sumsung'])
def test_main_page_search_field_exist(driver_factory, searched):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    elem = main_page.driver.find_element(By.XPATH, "//input[@name='search']")
    elem.click()
    elem.send_keys(searched)
    elem.send_keys(Keys.ENTER)
    wait = WebDriverWait(driver_factory, 2)
    wait.until(EC.title_is('Search - {}'.format(searched)))
    assert main_page.driver.current_url == 'http://localhost/index.php?route=product/search&search={}'.format(searched)


def test_main_page_search_button_exist(driver_factory):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    elem = main_page.driver.find_element(By.XPATH, "//div[@id='search']//button[@type='button']")
    elem.click()
    wait = WebDriverWait(driver_factory, 2)
    el_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='content']//p[2]")))
    assert el_text.text == 'There is no product that matches the search criteria.'


def test_main_page_slideshow_exist(driver_factory):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    try:
        wait = WebDriverWait(driver_factory, 3)
        assert wait.until(EC.visibility_of_element_located((By.ID, "slideshow0")))
    except NoSuchElementException:
        raise NoSuchElementException('Слайдшоу не было отображено на странице')


def test_main_page_catalog_page_opened(driver_factory):
    main_page = MainPage(driver_factory)
    main_page.driver.get(main_page.url)
    wait = WebDriverWait(driver_factory, 3)
    try:
        el = main_page.driver.find_element_by_link_text("Desktops")
        ActionChains(main_page.driver).move_to_element(el).perform()
        main_page.driver.find_element_by_link_text("Show All Desktops").click()
        assert wait.until(EC.url_matches(r'http:\/\/localhost\/index\.php\?route=product\/category\&path\=\d*'))
    except NoSuchElementException:
        raise NoSuchElementException('Страница с каталогом товаров не была загружена')
