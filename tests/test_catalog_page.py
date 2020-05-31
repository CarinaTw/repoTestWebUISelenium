import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re

DROPDOWN_LOCATOR = (By.XPATH, "//ul[@class='nav navbar-nav']/li[@class='dropdown']")
SEE_ALL_LOCATOR = (By.XPATH, "//div[@class='dropdown-menu']/a[@class='see-all']")
CONTENT_LOCATOR = (By.XPATH, "//div[@id='content']/h2")
PRODUCT_GRID_LOCATOR = (By.XPATH, "//div[@id='content']/div[@class='row'][4]")
ADD_TO_WISH_LIST_LOCATOR = (By.XPATH, "//button[@data-original-title='Add to Wish List']")
ADD_TO_CART_LOCATOR = (By.XPATH, "//i[@class='fa fa-shopping-cart']")
ALERT_LOCATOR = (By.XPATH, "//div[@class='alert alert-success alert-dismissible']")


def test_page_title(catalog_page):
    assert catalog_page.driver.title == 'Desktops'


@pytest.mark.parametrize("menu_item", [('Desktops', 'Laptops & Notebooks', 'Components', 'MP3 Players')])
def test_nav_bar_dropdown_item_show_all(catalog_page, menu_item):

    for i in range(4):
        menu_item = catalog_page.find_elements(DROPDOWN_LOCATOR)[i]
        ActionChains(catalog_page.driver).move_to_element(menu_item).pause(2).perform()
        catalog_page.find_elements(SEE_ALL_LOCATOR)[i].click()
        link_txt = catalog_page.find_elements(DROPDOWN_LOCATOR)[i].text
        page_txt = catalog_page.find_element(CONTENT_LOCATOR).text
        assert link_txt == page_txt
        assert catalog_page.catalog_url_matches()


def test_button_wish_list_check(catalog_page):
    catalog_page.find_elements(ADD_TO_WISH_LIST_LOCATOR)[1].click()

    alert_item = catalog_page.find_element(ALERT_LOCATOR)
    ActionChains(catalog_page.driver).move_to_element(alert_item).perform()
    assert re.search("You must login or create an account to save", alert_item.text)


@pytest.mark.xfail
def test_catalog_page_button_add_to_cart_check(catalog_page):
    catalog_page.find_elements(ADD_TO_CART_LOCATOR)[2].click()

    alert_item = catalog_page.find_element(ALERT_LOCATOR)
    ActionChains(catalog_page.driver).move_to_element(alert_item).perform()
    assert re.search("Success: You have added", alert_item.text)