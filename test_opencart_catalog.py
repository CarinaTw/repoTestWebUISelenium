# 1. Написать тесты проверяющие наличие элементов на разных страницах приложения opencart.
# 2. Реализовать минимум пять тестов (одни тест = одна страница приложения)
# 3. Какие элементы проверять определить самостоятельно, но не меньше 5 для каждой страницы.
#http://localhost/index.php?route=product/category&path=20
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from page import Page
from time import sleep
import re


class CatalogPage(Page):
    def __init__(self, driver):
        page = Page(driver)
        self.url = page.url + "/index.php?route=product/category&path=20"
        self.driver = driver


@pytest.mark.parametrize("menu_item", [('Desktops', 'Laptops & Notebooks', 'Components', 'MP3 Players')])
def test_catalog_page_nav_bar_dropdown_item_show_all(driver_factory, menu_item):
    cat_page = CatalogPage(driver_factory)
    cat_page.driver.get(cat_page.url)
    wait = WebDriverWait(driver_factory, 3)
    for i in range(4):
        menu_item = cat_page.driver.find_elements(By.XPATH, "//ul[@class='nav navbar-nav']/li[@class='dropdown']")[i]
        ActionChains(cat_page.driver).move_to_element(menu_item).pause(2).perform()
        btn = cat_page.driver.find_elements(By.XPATH, "//div[@class='dropdown-menu']/a[@class='see-all']")[i]
        btn.click()
        link_txt = cat_page.driver.find_elements(By.XPATH, "//ul[@class='nav navbar-nav']/li[@class='dropdown']")[i].text
        page_txt = cat_page.driver.find_element(By.XPATH, "//div[@id='content']/h2").text
        assert wait.until(EC.url_matches(r'http:\/\/localhost\/index\.php\?route=product\/category\&path\=\d*'))
        assert link_txt == page_txt


def test_catalog_page_button_wish_list_check(driver_factory):
    cat_page = CatalogPage(driver_factory)
    cat_page.driver.get(cat_page.url)
    product_grid = cat_page.driver.find_element(By.XPATH, "//div[@id='content']/div[@class='row'][4]")
    grid_item = product_grid.find_elements_by_css_selector(
        ".product-layout.product-grid.col-lg-4.col-md-4.col-sm-6.col-xs-12")[1]
    button_heart = grid_item.find_element(By.XPATH, "//button[@data-original-title='Add to Wish List']")
    button_heart.click()
    wait = WebDriverWait(driver_factory, 3)
    alert_item = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                          "//div[@class='alert alert-success alert-dismissible']")))
    ActionChains(cat_page.driver).move_to_element(alert_item).perform()
    assert re.search("You must login or create an account to save", alert_item.text)


@pytest.mark.xfail
def test_catalog_page_button_add_to_cart_check(driver_factory):
    cat_page = CatalogPage(driver_factory)
    cat_page.driver.get(cat_page.url)
    wait = WebDriverWait(driver_factory, 3)

    product_grid = cat_page.driver.find_element(By.XPATH, "//div[@id='content']/div[@class='row'][4]")
    grid_item = product_grid.find_elements_by_css_selector(
        ".product-layout.product-grid.col-lg-4.col-md-4.col-sm-6.col-xs-12")[1]
    button_cart = grid_item.find_elements(By.XPATH, "//i[@class='fa fa-shopping-cart']")
    sleep(3)
    button_cart[2].click()
    alert_item = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                          "//div[@class='alert alert-success alert-dismissible']")))
    ActionChains(cat_page.driver).move_to_element(alert_item).perform()
    assert re.search("Success: You have added", alert_item.text)
