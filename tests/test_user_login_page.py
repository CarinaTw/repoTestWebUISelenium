import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


BREADCRUMB_LOCATOR = (By.XPATH, "//div[@id='account-login']/ul[@class='breadcrumb']/li")
HOME_LOCATOR = (By.XPATH, "//a[@href='http://localhost/index.php?route=common/home']")
FIELD_CUSTOMER_LOCATOR = (By.XPATH, "//div[@class='well']/h2")
ALERT_LOCATOR = (By.XPATH, "//div[@class='alert alert-danger alert-dismissible']")
EMAIL_LOCATOR = (By.XPATH, "//input[@name='email']")
PASSWORD_LOCATOR =(By.XPATH, "//input[@name='password']")
SUBMIT_LOCATOR = (By.XPATH, "//div[@id='content']//div[@class='col-sm-6']//"
                            "form[@action='https://localhost/index.php?route=account/login']"
                            "//input[@type='submit']")
INPUT_EMAIL_LOCATOR = (By.ID, "input-email")
INPUT_PASSWORD_LOCATOR = (By.ID, "input-password")
BUTTON_LOCATOR = (By.XPATH, "//input[@class='btn btn-primary']")


def test_page_title(user_login_page):
    assert user_login_page.driver.title == 'Account Login'


def test_login_page_breadcrumbs(user_login_page):
    user_login_page.find_element(HOME_LOCATOR).click()
    assert user_login_page.driver.title == 'Your Store'

    user_login_page.driver.get(user_login_page.url)
    item = user_login_page.find_elements(BREADCRUMB_LOCATOR)
    assert item[1].text == 'Account'

    user_login_page.driver.get(user_login_page.url)
    item = user_login_page.find_elements(BREADCRUMB_LOCATOR)
    assert item[2].text == 'Login'


def test_login_page_register_new_acc_form_exist(user_login_page):
    item_txt = user_login_page.find_elements(FIELD_CUSTOMER_LOCATOR)[0].text
    assert item_txt == 'New Customer'


def test_login_page_login_form_exist(user_login_page):
    item_txt = user_login_page.find_elements(FIELD_CUSTOMER_LOCATOR)[1].text
    assert item_txt == 'Returning Customer'


def test_login_page_login_frong_user_check_err_msg(user_login_page):
    el = user_login_page.find_element(EMAIL_LOCATOR)
    el.click()
    el.send_keys('wrong_login')
    user_login_page.driver.implicitly_wait(2)

    el = user_login_page.find_element(PASSWORD_LOCATOR)
    el.click()
    el.send_keys('wrong_password')
    user_login_page.driver.implicitly_wait(2)

    btn = user_login_page.find_element(SUBMIT_LOCATOR)
    btn.click()

    alert_item = user_login_page.find_element(ALERT_LOCATOR)
    ActionChains(user_login_page.driver).move_to_element(alert_item).perform()
    assert (alert_item.text == 'Warning: Your account has exceeded allowed number ' \
                              'of login attempts. Please try again in 1 hour.') or \
           (alert_item.text == 'Warning: No match for E-Mail Address and/or Password.')


def test_login_check(user_login_page):
    el = user_login_page.find_element(INPUT_EMAIL_LOCATOR)
    el.click()
    el.send_keys('dex@example.ru')

    el = user_login_page.find_element(INPUT_PASSWORD_LOCATOR)
    el.click()
    el.send_keys('codex')

    btn = user_login_page.find_element(BUTTON_LOCATOR)
    btn.click()
    try:
        user_login_page.driver.implicitly_wait(2)
        assert user_login_page.driver.title == "My Account"
    except TimeoutException:
        TimeoutException('My Account page not loaded')


def test_login_page_logout_check(user_login_page):
    el = user_login_page.find_element(INPUT_EMAIL_LOCATOR)
    el.click()
    el.send_keys('dex@example.ru')

    el = user_login_page.find_element(INPUT_PASSWORD_LOCATOR)
    el.click()
    el.send_keys('codex')

    btn = user_login_page.find_element(BUTTON_LOCATOR)
    btn.click()

    user_login_page.driver.implicitly_wait(2)
    assert user_login_page.driver.title == "My Account"
    try:
        logout_btn = user_login_page.find_element_by_link_text("Logout")
        logout_btn.click()
        user_login_page.driver.implicitly_wait(2)
        user_login_page.driver.title == "Account Logout"

        logout_btn = user_login_page.find_element_by_link_text("Continue")
        logout_btn.click()
        user_login_page.driver.implicitly_wait(2)
        user_login_page.driver.title == "Your Store"
    except TimeoutException:
        TimeoutException("Logout page not loaded")

