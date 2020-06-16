import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions
from pages.adminpage import AdminLoginPage
from pages.mainpage import MainPage
from pages.catalogpage import CatalogPage
from pages.productpage import ProductPage
from pages.userloginpage import UserLoginPage
from selenium.common.exceptions import TimeoutException

import logging
logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', level=logging.INFO, filename='selenium.log')


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     choices=["chrome", "firefox", "opera", "yandex"])
    parser.addoption("--selenoid", action="store", default="localhost")


@pytest.fixture(scope='session')
def browser(request):
    test_name = request.node.name
    logger = logging.getLogger('browser fixture')
    logger.info("\nStarted tests {}".format(test_name))

    selenoid = request.config.getoption("--selenoid")
    exec_url = f"http://{selenoid}:4444/wd/hub"

    browser = request.config.getoption("--browser")

    # capabilities for selenoid
    caps = {"browserName": browser,
            "version": "81.0",
            "enableLog": True,
            "enableVNC": True,
            "screenResolution": "1280x720",
            "name": request.node.name
            }

    wd = webdriver.Remote(command_executor=exec_url, desired_capabilities=caps)
    logger.info("\n {} started {}".format(browser, wd.desired_capabilities))
    logger.info(f"\n Start session {wd.session_id}")
    request.addfinalizer(wd.quit)
    return wd

    # if b == "chrome":
    #     options = ChromeOptions()
    #     options.headless = True
    #     options.add_argument('--disable-infobars')
    #     options.add_argument('--disable-notifications')
    #     options.add_argument('--disable-web-security')
    #     options.add_argument('--ignore-certificate-errors')
    #     wd = webdriver.Chrome(options=options)
    #     logger.info("\n {} started {}".format(b, wd.desired_capabilities))
    #     request.addfinalizer(wd.quit)
    #     return wd
    # elif b == "firefox":
    #     options = FirefoxOptions()
    #     options.headless = True
    #     wd = webdriver.Firefox(options=options)
    #     logger.info("\n {} started {}".format(b, wd.desired_capabilities))
    #     request.addfinalizer(wd.quit)
    #     return wd


# @pytest.fixture(scope='session')
# def remote(request):
#     """ для запуска тестов в Selenium Server Grid """
#
#     browser = request.config.getoption("--browser")
#     executor = request.config.getoption("--executor")
#
#     wd = webdriver.Remote(command_executor=f"http://{executor}:4445/wd/hub",
#                           desired_capabilities={"browserName": browser})    # , "platform": "linux"
#
#     request.addfinalizer(wd.quit)
#     return wd


@pytest.fixture()
def admin_page(browser):
    logger = logging.getLogger('admin_page fixture')
    logger.info("\nAdmin page loading ...")
    page = AdminLoginPage(browser)
    try:
        page.go_to()
    except TimeoutException:
        logger.exception("Admin page not loaded")
        raise TimeoutException

    logger.info("\nAdmin page is opened")
    return page


@pytest.fixture()
def main_page(browser):
    logger = logging.getLogger('main_page fixture')
    logger.info("\nMain page loading ...")
    page = MainPage(browser)
    try:
        page.go_to()
    except TimeoutException:
        logger.exception("Main page not loaded")
        raise TimeoutException
    logger.info("\nMain page is opened")
    return page


@pytest.fixture()
def catalog_page(browser):
    logger = logging.getLogger('catalog_page fixture')
    logger.info("\nCatalog page loading ...")
    page = CatalogPage(browser)
    try:
        page.go_to()
    except TimeoutException:
        logger.exception("Catalog page not loaded")
        raise TimeoutException
    logger.info("\nCatalog page is opened")
    return page


@pytest.fixture()
def product_page(browser):
    logger = logging.getLogger('product_page fixture')
    logger.info("\nProduct page loading ...")
    page = ProductPage(browser)
    try:
        page.go_to()
    except TimeoutException:
        logger.exception("Product page not loaded")
        raise TimeoutException
    logger.info("\nProduct page is opened")
    return page


@pytest.fixture()
def user_login_page(browser):
    logger = logging.getLogger('user_login_page fixture')
    logger.info("\nUser Login page loading ...")
    page = UserLoginPage(browser)
    try:
        page.go_to()
    except TimeoutException:
        logger.exception("User login page not loaded")
        raise TimeoutException
    logger.info("\nUser Login page is opened")
    return page