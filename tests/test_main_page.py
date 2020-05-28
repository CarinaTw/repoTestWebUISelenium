import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


SEARCH_BUTTON_LOCATOR = (By.XPATH, "//div[@id='search']//button[@type='button']")
TXT_NO_SEARCH_RESULT_LOCATOR = (By.XPATH, "//div[@id='content']//p[2]")
SLIDESHOW_LOCATOR = (By.ID, "slideshow0")
SEARCH_INPUT_LOCATOR = (By.XPATH, "//input[@name='search']")


def test_page_title(main_page):
    assert main_page.driver.title == 'Your Store'


def test_search_button_exist(main_page):
    main_page.find_element(SEARCH_BUTTON_LOCATOR).click()
    assert main_page.find_element(TXT_NO_SEARCH_RESULT_LOCATOR).text == \
           'There is no product that matches the search criteria.'


def test_slideshow_exist(main_page):
    try:
        assert main_page.find_element(SLIDESHOW_LOCATOR)
    except NoSuchElementException:
        raise NoSuchElementException('Слайдшоу не было отображено на странице')


@pytest.mark.parametrize("searched", ['ipone', 'sumsung'])
def test_main_page_search_field_exist(main_page, searched):
    field = main_page.find_element(SEARCH_INPUT_LOCATOR)
    field.click()
    field.send_keys(searched)
    field.send_keys(Keys.ENTER)
    assert main_page.driver.title == 'Search - {}'.format(searched)
    assert main_page.driver.current_url == 'http://localhost/index.php?route=product/search&search={}'.format(searched)


def test_main_page_catalog_page_opened(main_page):
    try:
        el = main_page.find_element_by_link_text("Desktops")
        ActionChains(main_page.driver).move_to_element(el).perform()

        main_page.find_element_by_link_text("Show All Desktops").click()
        assert main_page.catalog_url_matches()

    except NoSuchElementException:
        raise NoSuchElementException('Страница с каталогом товаров не была загружена')