# 1. Написать тесты проверяющие наличие элементов на разных страницах приложения opencart.
# 2. Реализовать минимум пять тестов (одни тест = одна страница приложения)
# 3. Какие элементы проверять определить самостоятельно, но не меньше 5 для каждой страницы.
# http://localhost/admin/
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.common.keys import Keys
from page import Page
from time import sleep
import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class AdminLogPage(Page):
    def __init__(self, driver):
        page = Page(driver)
        self.url = page.url + "/admin/"
        self.driver = page.driver

    def get_page_title(self):
        adm_login_page = AdminLogPage(self.driver)
        adm_login_page.driver.get(adm_login_page.url)
        title = adm_login_page.driver.title
        assert title == 'Administration'
        return title

    def admin_login(self):
        adm_login_page = AdminLogPage(self.driver)
        adm_login_page.driver.get(adm_login_page.url)

        try:
            usr_name = adm_login_page.driver.find_element(By.ID, "input-username")
            usr_name.click()
            usr_name.send_keys('user')

            usr_pwd = adm_login_page.driver.find_element(By.ID, "input-password")
            usr_pwd.click()
            usr_pwd.send_keys('bitnami1')
            usr_pwd.send_keys(Keys.ENTER)

            adm = adm_login_page.driver.find_element(By.XPATH, "//div[@class='page-header']//h1")
            assert adm.text == "Dashboard"
            return adm_login_page

        except NoSuchElementException:
            raise NoSuchElementException('User not logged by any reason')

    def add_prod(self, tkn, product_name='Some Product', product_meta='Some metadata', product_model='Some model'):
        products = [product_name, product_meta, product_model]
        wait = WebDriverWait(self.driver, 2)
        catalog = wait.until(EC.visibility_of_element_located((By.ID, "menu-catalog")))
        catalog.click()

        prod = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//ul[@id='collapse1']/li")))
        prod[1].click()

        try:
            add_new = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='content']/div[@class='page-header']//"
                                                            "a[@data-original-title='Add New']")))
            add_new.click()

            prod_name = tkn.driver.find_element(By.XPATH, "//input[@id='input-name1']")
            prod_name.click()
            prod_name.send_keys(products[0])

            meta = tkn.driver.find_element(By.XPATH, "//input[@id='input-meta-title1']")
            meta.click()
            meta.send_keys(products[1])

            data_tab = tkn.driver.find_elements(By.XPATH, "//ul[@class='nav nav-tabs']/li")[1].click()
            data_model = tkn.driver.find_element(By.XPATH, "//input[@id='input-model']")
            data_model.click()
            data_model.send_keys(products[2])

            save = tkn.driver.find_element(By.XPATH, "//button[@data-original-title='Save']")
            save.click()
            return products
        except TimeoutException:
            raise TimeoutException('Product not added')

    def check_prod_exist_by_name(self, token, product_name):
        wait = WebDriverWait(self.driver, 2)

        table_rows = wait.until(EC.visibility_of_all_elements_located((By.XPATH,
                                                                       "//table[@class='table table-bordered table-hover']/"
                                                                       "tbody/tr")))
        for i in range(len(table_rows)):
            el = token.driver.find_elements(By.XPATH, "//tbody/tr")[i]
            p = re.findall(product_name, el.text)
            if p != []:
                assert p[0] == product_name
                item_position = i
                return item_position

    def delete_prod_by_name(self, token, product_name):
        wait = WebDriverWait(self.driver, 2)

        try:
            pp = token.check_prod_exist_by_name(token, product_name)

            checkbox = token.driver.find_elements(By.XPATH, "//input[@type='checkbox']")[pp + 1]
            checkbox.click()
            token.driver.implicitly_wait(2)

            del_btn = token.driver.find_element(By.XPATH, "//button[@data-original-title='Delete']")
            del_btn.click()
            token.driver.implicitly_wait(2)

            wait.until(EC.alert_is_present(), "Alert is not present!")
            alert = token.driver.switch_to_alert()
            alert.accept()

            token.check_prod_exist_by_name(token, product_name)

        except TimeoutException:
            raise TimeoutException('Delete not performed!')


def test_login_page_title(driver_factory):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)
    assert adm_login_page.driver.title == adm_login_page.get_page_title()


def test_adimn_page_logo(driver_factory):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)
    assert adm_login_page.driver.find_element(By.XPATH,
                                              "//body//div[@id='header-logo']//img[@src='view/image/logo.png']")


def test_admin_page_form_enter_login_text(driver_factory):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)
    txt = adm_login_page.driver.find_element(By.XPATH,
                                             "//div[@id='content']//div[@class='panel-heading']/"
                                             "h1[@class='panel-title']").text
    assert txt == "Please enter your login details."


def test_admin_page_username_field(driver_factory):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)
    txt = adm_login_page.driver.find_element(By.XPATH,
                                             "//div[@id='content']//div[@class='panel-body']//"
                                             "form//label[@for='input-username']").text
    assert txt == "Username"
    adm_login_page.driver.find_element(By.XPATH,
                                       "//div[@id='content']//div[@class='panel-body']//"
                                       "form//input[@name='username']").click()


def test_admin_login_page_enter_only_username(driver_factory):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)
    txt = adm_login_page.driver.find_element(By.XPATH,
                                             "//div[@id='content']//div[@class='panel-body']//"
                                             "form//label[@for='input-username']").text
    assert txt == "Username"
    usr_name = adm_login_page.driver.find_element(By.XPATH,
                                                  "//div[@id='content']//div[@class='panel-body']//"
                                                  "form//input[@name='username']")
    usr_name.click()
    usr_name.send_keys('user1')
    usr_name.send_keys(Keys.ENTER)

    el_alert = WebDriverWait(adm_login_page.driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                        "//div[@class='alert alert-danger alert-dismissible']")))
    ActionChains(adm_login_page.driver).move_to_element(el_alert).perform()
    assert re.search('No match for Username and/or Password', el_alert.text)


def test_admin_page_footer_text(driver_factory):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)
    foot = adm_login_page.driver.find_element(By.XPATH, "//footer[@id='footer']")
    assert foot.text == "OpenCart © 2009-2020 All Rights Reserved."


def test_admin_login(driver_factory):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)

    adm_login_page.admin_login()

    adm = adm_login_page.driver.find_element(By.XPATH, "//div[@class='page-header']//h1")
    assert adm.text == "Dashboard"


@pytest.mark.parametrize("product_name, product_meta, product_model", [('Product_2020', 'Prod2020', 'Model XXX')])
def test_admin_login_product_add(driver_factory, product_name, product_meta, product_model):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)

    token = adm_login_page.admin_login()

    adm = token.driver.find_element(By.XPATH, "//div[@class='page-header']//h1")
    assert adm.text == "Dashboard"

    token.add_prod(token, product_name=product_name, product_meta=product_meta, product_model=product_model)

    pp = token.check_prod_exist_by_name(token, product_name)
    assert pp != None
    token.delete_prod_by_name(token, product_name)


@pytest.mark.parametrize("product_name_1, product_name_2", [('Product 2020', 'Product 2020 NEW')])
def test_admin_login_product_edit(driver_factory, product_name_1, product_name_2):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)
    wait = WebDriverWait(driver_factory, 3)

    token = adm_login_page.admin_login()

    token.add_prod(token, product_name_1, 'Prod2020', 'Model XXX')

    pp = token.check_prod_exist_by_name(token, product_name_1)

    wait.until(EC.visibility_of_all_elements_located((By.XPATH,
                                                      "//table[@class='table table-bordered table-hover']/"
                                                      "tbody/tr")))

    btn = token.driver.find_elements(By.XPATH, "//a[@data-original-title='Edit']")[pp]
    btn.click()

    prod_name = token.driver.find_element(By.XPATH, "//input[@id='input-name1']")
    prod_name.click()
    prod_name.send_keys(Keys.BACKSPACE*len(product_name_1))
    prod_name.send_keys(product_name_2)

    save = token.driver.find_element(By.XPATH, "//button[@data-original-title='Save']")
    save.click()
    assert token.check_prod_exist_by_name(token, product_name_2) != None

    token.delete_prod_by_name(token, product_name_2)


@pytest.mark.parametrize("product_name_1", ['Product 2033'])
def test_admin_login_product_delete(driver_factory, product_name_1):
    adm_login_page = AdminLogPage(driver_factory)
    adm_login_page.driver.get(adm_login_page.url)
    wait = WebDriverWait(driver_factory, 3)

    token = adm_login_page.admin_login()

    adm = token.driver.find_element(By.XPATH, "//div[@class='page-header']//h1")
    assert adm.text == "Dashboard"

    token.add_prod(token, product_name_1, 'Prod2020', 'Model XXX')

    wait.until(EC.visibility_of_all_elements_located((By.XPATH,
                                                      "//table[@class='table table-bordered table-hover']/"
                                                      "tbody/tr")))

    token.delete_prod_by_name(token, product_name_1)

    # Check product deleted:
    prod = token.check_prod_exist_by_name(token, product_name_1)
    assert prod == None
