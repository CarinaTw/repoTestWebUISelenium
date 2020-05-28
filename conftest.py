import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions
from pages.adminpage import AdminLoginPage
from pages.mainpage import MainPage
from pages.catalogpage import CatalogPage
from pages.productpage import ProductPage
from pages.userloginpage import UserLoginPage


@pytest.fixture(scope='session')
def browser(request):
    options = ChromeOptions()
    options.headless = False
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-web-security')
    options.add_argument('--ignore-certificate-errors')
    wd = webdriver.Chrome(options=options)
    request.addfinalizer(wd.quit)
    return wd


@pytest.fixture()
def admin_page(browser):
    page = AdminLoginPage(browser)
    page.go_to()
    return page


@pytest.fixture()
def main_page(browser):
    page = MainPage(browser)
    page.go_to()
    return page


@pytest.fixture()
def catalog_page(browser):
    page = CatalogPage(browser)
    page.go_to()
    return page


@pytest.fixture()
def product_page(browser):
    page = ProductPage(browser)
    page.go_to()
    return page


@pytest.fixture()
def user_login_page(browser):
    page = UserLoginPage(browser)
    page.go_to()
    return page