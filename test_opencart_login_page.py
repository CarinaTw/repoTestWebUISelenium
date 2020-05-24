# 1. Написать тесты проверяющие наличие элементов на разных страницах приложения opencart.
# 2. Реализовать минимум пять тестов (одни тест = одна страница приложения)
# 3. Какие элементы проверять определить самостоятельно, но не меньше 5 для каждой страницы.
# http://localhost/index.php?route=account/login
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from page import Page


class LoginPage(Page):
    def __init__(self, driver):
        page = Page(driver)
        self.url = page.url + "/index.php?route=account/login"
        self.driver = page.driver

    def get_page_title(self):
        login_page = LoginPage(self.driver)
        login_page.driver.get(login_page.url)
        title = login_page.driver.title
        assert title == 'Account Login'
        return title


def test_login_page_title(driver_factory):
    login_page = LoginPage(driver_factory)
    login_page.driver.get(login_page.url)
    assert login_page.driver.title == login_page.get_page_title()


def test_login_page_breadcrumbs(driver_factory):
    login_page = LoginPage(driver_factory)
    login_page.driver.get(login_page.url)
    item = login_page.driver.find_elements(By.XPATH, "//div[@id='account-login']/ul[@class='breadcrumb']/li")
    item[0].find_element(By.XPATH, "//a[@href='http://localhost/index.php?route=common/home']").click()
    assert login_page.driver.title == 'Your Store'

    login_page.driver.get(login_page.url)
    item = login_page.driver.find_elements(By.XPATH, "//div[@id='account-login']/ul[@class='breadcrumb']/li")
    assert item[1].text == 'Account'

    login_page.driver.get(login_page.url)
    item = login_page.driver.find_elements(By.XPATH, "//div[@id='account-login']/ul[@class='breadcrumb']/li")
    assert item[2].text == 'Login'


def test_login_page_register_new_acc_form_exist(driver_factory):
    login_page = LoginPage(driver_factory)
    login_page.driver.get(login_page.url)
    item = login_page.driver.find_elements(By.XPATH, "//div[@id='content']//div[@class='col-sm-6']")
    assert item[0].find_element(By.XPATH, "//h2").text == 'New Customer'


def test_login_page_login_form_exist(driver_factory):
    login_page = LoginPage(driver_factory)
    login_page.driver.get(login_page.url)
    item = login_page.driver.find_elements(By.XPATH, "//div[@id='content']//div[@class='col-sm-6']//h2")[1].text
    assert item == 'Returning Customer'


def test_login_page_login_frong_user_check_err_msg(driver_factory):
    login_page = LoginPage(driver_factory)
    login_page.driver.get(login_page.url)
    name = login_page.driver.find_elements(By.XPATH, "//div[@id='content']//div[@class='col-sm-6']//"
                                                     "form[@action='https://localhost/index.php?route=account/login']"
                                                     "//div[@class='form-group']")[0]
    el = name.find_element(By.XPATH, "//input[@name='email']")
    el.click()
    el.send_keys('wrong_login')
    sleep(1)

    pwd = login_page.driver.find_elements(By.XPATH, "//div[@id='content']//div[@class='col-sm-6']//"
                                          "form[@action='https://localhost/index.php?route=account/login']"
                                          "//div[@class='form-group']")[1]
    el = pwd.find_element(By.XPATH, "//input[@name='password']")
    el.click()
    el.send_keys('wrong_password')
    sleep(1)

    btn = login_page.driver.find_element(By.XPATH, "//div[@id='content']//div[@class='col-sm-6']//"
                                         "form[@action='https://localhost/index.php?route=account/login']"
                                         "//input[@type='submit']")
    btn.click()

    alert_item = WebDriverWait(login_page.driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                    "//div[@class='alert alert-danger alert-dismissible']")))
    ActionChains(login_page.driver).move_to_element(alert_item).perform()
    assert alert_item.text == 'Warning: No match for E-Mail Address and/or Password.'







