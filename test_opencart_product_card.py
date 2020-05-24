# 1. Написать тесты проверяющие наличие элементов на разных страницах приложения opencart.
# 2. Реализовать минимум пять тестов (одни тест = одна страница приложения)
# 3. Какие элементы проверять определить самостоятельно, но не меньше 5 для каждой страницы.
# http://localhost/index.php?route=product/product&path=57&product_id=49
from selenium.webdriver.common.by import By

import pytest
import re
from page import Page


class ProductPage(Page):
    def __init__(self, driver):
        page = Page(driver)
        self.url = page.url + "/index.php?route=product/product&path=57&product_id=49"
        self.driver = page.driver

    def get_page_title(self):
        prod_page = ProductPage(self.driver)
        prod_page.driver.get(prod_page.url)
        title = prod_page.driver.title
        assert title == 'Samsung Galaxy Tab 10.1'
        return title


def test_product_page_title(driver_factory):
    prod_page = ProductPage(driver_factory)
    prod_page.driver.get(prod_page.url)
    assert prod_page.driver.title == prod_page.get_page_title()


list_items = ['Product Code', 'Reward Points', 'Availability']
@pytest.mark.parametrize("item_name", [list_items])
def test_product_attributes(driver_factory, item_name):
    prod_page = ProductPage(driver_factory)
    prod_page.driver.get(prod_page.url)
    for i in range(len(list_items)):
        el = prod_page.driver.find_elements(By.XPATH, "//div[@id='content']//"
                                                      "div[@class='col-sm-4']//ul[@class='list-unstyled']/li")[i].text
        attr = re.split(':', el)
        assert attr[0] == item_name[i]


def test_product_attributes_price(driver_factory):
    prod_page = ProductPage(driver_factory)
    prod_page.driver.get(prod_page.url)
    price_txt = prod_page.driver.find_elements(By.XPATH, "//div[@id='content']//"
                                               "div[@class='col-sm-4']//ul[@class='list-unstyled']")[1].text
    assert re.search('Ex Tax', price_txt)
    assert re.match(r'\$\d*', price_txt)


def test_product_add_to_cart_btn_exist(driver_factory):
    prod_page = ProductPage(driver_factory)
    prod_page.driver.get(prod_page.url)
    btn_txt = prod_page.driver.find_element(By.XPATH, "//div[@id='content']//"
                                            "div[@class='col-sm-4']/div[@id='product']//button[@type='button']").text
    assert btn_txt == 'Add to Cart'


def test_product_tab_description_exist(driver_factory):
    tab_list = ['Description', 'Reviews']
    prod_page = ProductPage(driver_factory)
    prod_page.driver.get(prod_page.url)
    tab_description = prod_page.driver.find_elements(By.XPATH, "//div[@id='content']//ul[@class='nav nav-tabs']/li")
    for i in range((len(tab_description))):
        assert re.search(tab_list[i], tab_description[i].text)


def test_product_tab_description_text(driver_factory):
    prod_page = ProductPage(driver_factory)
    prod_page.driver.get(prod_page.url)
    tab_description = prod_page.driver.find_element(By.XPATH, "//div[@id='content']//"
                                                              "div[@class='tab-content']/div[@id='tab-description']")
    tab_txt = tab_description.text
    title = prod_page.get_page_title()
    assert re.findall(title, tab_txt)


