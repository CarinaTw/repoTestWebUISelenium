import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        help="This is request url",
        default='http://127.0.0.1:80'
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
def browser(request):
    b = request.config.getoption("--browser")
    if b == "chrome":
        options = ChromeOptions()
        options.headless = True
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

