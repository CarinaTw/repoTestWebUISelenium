import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        help="This is request url",
        default='http://localhost:80'
    )

    parser.addoption(
        "--browser",
        help="Browser",
        default='chrome',
        choices=['chrome', 'firefox', 'ie']
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def driver_factory(request):
    b = request.config.getoption("--browser")
    if b == "chrome":
        options = ChromeOptions()
        options.headless = False
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-web-security')
        options.add_argument('--ignore-certificate-errors')
        wd = webdriver.Chrome(options=options)
        request.addfinalizer(wd.quit)
        return wd
    elif b == "firefox":
        options = FirefoxOptions()
        options.headless = True
        wd = webdriver.Firefox(options=options)
        return wd
    elif b == "ie":
        options = IeOptions()
        options.headless = True
        wd = webdriver.Ie(options=options)
        return wd
