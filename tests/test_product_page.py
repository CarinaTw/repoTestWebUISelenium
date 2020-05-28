import pytest
from selenium.webdriver.common.by import By
import re

LIST_LOCATOR = (By.XPATH, "//div[@id='content']//div[@class='col-sm-4']//ul[@class='list-unstyled']")
BUTTON_ADD_TO_CART_LOCATOR = (By.XPATH, "//div[@id='content']//div[@class='col-sm-4']"
                                        "/div[@id='product']//button[@type='button']")
NAV_LOCATOR = (By.XPATH, "//div[@id='content']//ul[@class='nav nav-tabs']/li")
TAB_DESCRIPTION_LOCATOR = (By.XPATH, "//div[@id='content']//div[@class='tab-content']/div[@id='tab-description']")


def test_page_title(product_page):
    assert product_page.driver.title == 'iPod Classic'


def test_product_attributes_price(product_page):
    price_txt = product_page.find_elements(LIST_LOCATOR)[1].text
    assert re.search('Ex Tax', price_txt)
    assert re.match(r'\$\d*', price_txt)


def test_product_add_to_cart_btn_exist(product_page):
    btn_txt = product_page.find_element(BUTTON_ADD_TO_CART_LOCATOR).text
    assert btn_txt == 'Add to Cart'


def test_product_tab_description_exist(product_page):
    tab_list = ['Description', 'Reviews']
    tab_description = product_page.find_elements(NAV_LOCATOR)
    for i in range((len(tab_description))):
        assert re.search(tab_list[i], tab_description[i].text)


def test_product_tab_description_text(product_page):
    tab_description = product_page.find_element(TAB_DESCRIPTION_LOCATOR)
    assert len(tab_description.text) > 0
