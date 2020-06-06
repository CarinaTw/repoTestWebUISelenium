from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import logging
logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', level=logging.DEBUG)


class BasePage(object):
    def __init__(self, driver):
        self.base_url = "http://localhost"
        self.driver = driver
        self.logger = logging.getLogger(type(self).__name__)

    def go_to(self):
        self.logger.info("Open URL {}:".format(self.base_url))
        return self.driver.get(self.base_url)       # возвращается страница http://localhost

    def find_element(self, locator, time=10):
        self.logger.debug("Find element by locator: {}". format(locator))
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        self.logger.debug("Find elements by locator: {}". format(locator))
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def find_element_by_link_text(self, text, time=10):
        self.logger.debug("Find element by link text: {}".format(text))
        wait = WebDriverWait(self.driver, time)
        return self.driver.find_element_by_link_text(text)

    def catalog_url_matches(self, time=10):
        if WebDriverWait(self.driver, time).until(EC.url_matches(r'http:\/\/localhost\/index\.php\?route=product\/category\&path\=\d*')):
            return True

