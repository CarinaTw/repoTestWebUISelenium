import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions
from pages.adminpage import AdminLoginPage
from pages.mainpage import MainPage
from pages.catalogpage import CatalogPage
from pages.productpage import ProductPage
from pages.userloginpage import UserLoginPage


# @pytest.fixture(scope='session')
# def browser(request):
#     options = ChromeOptions()
#     options.headless = False
#     options.add_argument('--disable-infobars')
#     options.add_argument('--disable-notifications')
#     options.add_argument('--disable-web-security')
#     options.add_argument('--ignore-certificate-errors')
#     wd = webdriver.Chrome(options=options)
#     request.addfinalizer(wd.quit)
#     return wd


# @pytest.fixture(scope='session')
# def remote(request):
#     """ для запуска тестов в Selenium Server Grid """
#
#     #browser = request.config.getoption("--browser")
#     #executor = request.config.getoption("--executor")
#
#     wd = webdriver.Remote(command_executor=f"http://0.0.0.0:4444/wd/hub",
#                           desired_capabilities={"browserName": "chrome", "platform": "linux"})   # , "platform": "linux"
#
#     request.addfinalizer(wd.quit)
#     return wd


@pytest.fixture(scope='session')
def browser(request):
    test_name = request.node.name
    #logger = logging.getLogger('browser fixture')
    #logger.info("\nStarted tests {}".format(test_name))

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
    #logger.info("\n {} started {}".format(browser, wd.desired_capabilities))
    #logger.info(f"\n Start session {wd.session_id}")
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