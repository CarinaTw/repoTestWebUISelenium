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
