import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import allure

LOGO_LOCATOR = (By.XPATH, "//body//div[@id='header-logo']//img[@src='view/image/logo.png']")
FOOTER_TEXT_LOCATOR = (By.XPATH, "//footer[@id='footer']")
TITLE_TEXT_LOCATOR = (By.XPATH, "//div[@class='page-header']//h1")


@allure.feature('User Authorization')
@allure.story('User authorization phase #1')
@allure.title('Test admin success login')
def test_admin_login_success(admin_page):
    with allure.step('Логинимся в админку'):
        try:
            admin_page.login()
        except TimeoutException:
            allure.attach(body=admin_page.driver.get_screenshot_as_png(),
                          name="screenshot_exception_login",
                          attachment_type=allure.attachment_type.PNG)
            raise TimeoutException('Cannot login')
    with allure.step('Проверяем Title'):
        assert admin_page.driver.title == 'Dashboard'


@allure.feature('User Authorization')
@allure.story('User authorization phase #1')
@allure.title('Test logo exists on page')
def test_adimn_page_logo(admin_page):
    with allure.step('Поиск логитипа на странице'):
        assert admin_page.find_element(locator=LOGO_LOCATOR)


@allure.feature('User Authorization')
@allure.story('User authorization phase #1')
@allure.title('Test footer text')
def test_admin_page_footer_text(admin_page):
    with allure.step('Проверяем текст футера'):
        assert admin_page.find_element(locator=FOOTER_TEXT_LOCATOR).text == "OpenCart © 2009-2020 All Rights Reserved."


@allure.feature('User Authorization')
@allure.story('User authorization phase #1')
@allure.title('Test add new product')
@pytest.mark.parametrize("product_name, product_meta, product_model", [('Product_2020', 'Prod2020', 'Model XXX')])
def test_admin_login_product_add(admin_page, product_name, product_meta, product_model):
    with allure.step('Логинимся в админку'):
        try:
            admin_page.login()
        except TimeoutException:
            allure.attach(body=admin_page.driver.get_screenshot_as_png(),
                          name="screenshot_exception_login",
                          attachment_type=allure.attachment_type.PNG)
            raise TimeoutException('Cannot login')
    with allure.step('Добавляем новый продукт'):
        try:
            admin_page.add_product(product_name=product_name, product_meta=product_meta, product_model=product_model)
        except TimeoutException:
            allure.attach(body=admin_page.driver.get_screenshot_as_png(),
                          name="screenshot_exception_not_add",
                          attachment_type=allure.attachment_type.PNG)
            raise TimeoutException('Product not added')
    with allure.step('Проверяем, что добавился новый продукт'):
        assert not admin_page.check_prod_exist_by_name(product_name) == []


@allure.feature('User Authorization')
@allure.story('User authorization phase #1')
@allure.title('Test delete some product')
@pytest.mark.parametrize("product_name", ['Product_2020'])
def test_admin_login_product_delete(admin_page, product_name):
    with allure.step('Логинимся в админку'):
        try:
            admin_page.login()
        except TimeoutException:
            allure.attach(body=admin_page.driver.get_screenshot_as_png(),
                          name="screenshot_exception_login",
                          attachment_type=allure.attachment_type.PNG)
            raise TimeoutException('Cannot login')

    with allure.step('Проверяем, если продукт существует, удаляем продукт'):
        admin_page.go_to_products_table()
        if admin_page.check_prod_exist_by_name(product_name):
            try:
                admin_page.delete_product_by_name(product_name)
            except TimeoutException:
                allure.attach(body=admin_page.driver.get_screenshot_as_png(),
                              name="screenshot_exception_delete",
                              attachment_type=allure.attachment_type.PNG)
                raise TimeoutException('Cannot delete product')
    with allure.step('Проверяем, что продукт удалился'):
        assert admin_page.check_prod_exist_by_name(product_name) == []


@allure.feature('User Authorization')
@allure.story('User authorization phase #2')
@allure.title('Test edit some product')
@pytest.mark.parametrize("product_name_1, product_name_2", [('Product 2020', 'Product 2020 NEW')])
def test_admin_login_product_edit(admin_page, product_name_1, product_name_2):
    with allure.step('Логинимся в админку'):
        admin_page.login()
    with allure.step('Добавляем продукт'):
        admin_page.add_product(product_name=product_name_1)

    with allure.step('Проверяем, что продукт добавился и редактируем'):
        if admin_page.check_prod_exist_by_name(product_name_1):
            admin_page.driver.implicitly_wait(10)
            try:
                admin_page.edit_product(product_name_1, product_name_2)
            except TimeoutException:
                allure.attach(body=admin_page.driver.get_screenshot_as_png(),
                              name="screenshot_exception_edit",
                              attachment_type=allure.attachment_type.PNG)
                raise TimeoutException('Something went wrong when editing product')
    with allure.step('Проверяем, что изменения сохранились (изменилось имя продукта)'):
        assert not admin_page.check_prod_exist_by_name(product_name_2) == []

