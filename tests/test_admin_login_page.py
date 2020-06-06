import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

LOGO_LOCATOR = (By.XPATH, "//body//div[@id='header-logo']//img[@src='view/image/logo.png']")
FOOTER_TEXT_LOCATOR = (By.XPATH, "//footer[@id='footer']")
TITLE_TEXT_LOCATOR = (By.XPATH, "//div[@class='page-header']//h1")


def test_admin_login_success(admin_page):
    try:
        admin_page.login()
    except TimeoutException:
        raise TimeoutException('Cannot login')
    assert admin_page.driver.title == 'Dashboard'


def test_adimn_page_logo(admin_page):
    assert admin_page.find_element(locator=LOGO_LOCATOR)


def test_admin_page_footer_text(admin_page):
    assert admin_page.find_element(locator=FOOTER_TEXT_LOCATOR).text == "OpenCart © 2009-2020 All Rights Reserved."


@pytest.mark.parametrize("product_name, product_meta, product_model", [('Product_2020', 'Prod2020', 'Model XXX')])
def test_admin_login_product_add(admin_page, product_name, product_meta, product_model):
    try:
        admin_page.login()
    except TimeoutException:
        raise TimeoutException('Cannot login')

    try:
        admin_page.add_product(product_name=product_name, product_meta=product_meta, product_model=product_model)
    except TimeoutException:
        raise TimeoutException('Product not added')

    assert not admin_page.check_prod_exist_by_name(product_name) == []


@pytest.mark.parametrize("product_name", ['Product_2020'])
def test_admin_login_product_delete(admin_page, product_name):
    try:
        admin_page.login()
    except TimeoutException:
        raise TimeoutException('Cannot login')

    admin_page.go_to_products_table()

    if admin_page.check_prod_exist_by_name(product_name):
        try:
            admin_page.delete_product_by_name(product_name)
        except TimeoutException:
            raise TimeoutException('Cannot delete product')
    assert admin_page.check_prod_exist_by_name(product_name) == []


@pytest.mark.parametrize("product_name_1, product_name_2", [('Product 2020', 'Product 2020 NEW')])
def test_admin_login_product_edit(admin_page, product_name_1, product_name_2):
    admin_page.login()
    admin_page.add_product(product_name=product_name_1)
    if admin_page.check_prod_exist_by_name(product_name_1):
        admin_page.driver.implicitly_wait(10)
        try:
            admin_page.edit_product(product_name_1, product_name_2)
        except TimeoutException:
            raise TimeoutException('Something went wrong when editing product')
    assert not admin_page.check_prod_exist_by_name(product_name_2) == []
