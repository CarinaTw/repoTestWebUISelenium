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


class CatalogPage(Page):
    def __init__(self, driver):
        page = Page(driver)
        self.url = page.url + "/index.php?route=product/category&path=20"
        self.driver = driver


def test_catalog_page_title(driver_factory):
    cat_page = CatalogPage(driver_factory)
    cat_page.driver.get(cat_page.url)
    assert cat_page.driver.title == 'Desktops'


@pytest.mark.parametrize("menu_item", ['Desktops', 'Laptops & Notebooks', 'Components', 'MP3 Players'])
def test_catalog_page_nav_bar_dropdown_items(driver_factory, menu_item):
    links_list = ['Desktops', 'Laptops & Notebooks', 'Components', 'MP3 Players']
    cat_page = CatalogPage(driver_factory)
    cat_page.driver.get(cat_page.url)
    for i in range(len(links_list)):
        menu_item = cat_page.driver.find_elements(By.XPATH, "//ul[@class='nav navbar-nav']/li[@class='dropdown']")[i]
        ActionChains(cat_page.driver).move_to_element(menu_item).pause(2).perform()
        cat_page.driver.find_elements(By.XPATH, "//div[@class='dropdown-menu']/a[@class='see-all']")[i].click()
        link_txt = cat_page.driver.find_elements(By.XPATH, "//ul[@class='nav navbar-nav']/li[@class='dropdown']")[i].text
        page_txt = cat_page.driver.find_element(By.XPATH, "//div[@id='content']/h2").text
        assert link_txt == page_txt


def test_catalog_page_nav_bar_item_pc(driver_factory):
    cat_page = CatalogPage(driver_factory)
    cat_page.driver.get(cat_page.url)
    elem = cat_page.driver.find_element(By.XPATH,
                                        "//ul[@class='nav navbar-nav']/li[@class='dropdown']/"
                                        "a[@class='dropdown-toggle']")
    elem.click()
    ActionChains(cat_page.driver).move_to_element(elem).pause(2).perform()
    cat_page.driver.find_element(By.XPATH, "//ul[@class='list-unstyled']/li[1]").click()
    cat_page.driver.find_element_by_partial_link_text('PC')
    text = cat_page.driver.find_element(By.XPATH, "//div[@id='content']//p")
    assert text.text == 'There are no products to list in this category.'


def test_catalog_page_button_wish_list(driver_factory):
    cat_page = CatalogPage(driver_factory)
    cat_page.driver.get(cat_page.url)
    product_grid = cat_page.driver.find_element(By.XPATH, "//div[@id='content']/div[@class='row'][4]")
    grid_item = product_grid.find_elements_by_css_selector(
        ".product-layout.product-grid.col-lg-4.col-md-4.col-sm-6.col-xs-12")[1]
    button_heart = grid_item.find_element(By.XPATH, "//button[@data-original-title='Add to Wish List']")
    button_heart.click()
    alert_item = WebDriverWait(cat_page.driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                          "//div[@class='alert alert-success alert-dismissible']")))
    ActionChains(cat_page.driver).move_to_element(alert_item).perform()
    assert alert_item.find_element_by_partial_link_text('login').text == 'login'
    assert alert_item.find_element_by_partial_link_text('create an account').text == 'create an account'
    assert alert_item.find_element_by_partial_link_text('wish list').text == 'wish list'


