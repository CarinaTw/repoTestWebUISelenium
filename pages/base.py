from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage(object):
    def __init__(self, driver):
        self.base_url = "http://localhost"
        self.driver = driver

    def go_to(self):
        return self.driver.get(self.base_url)       # возвращается страница http://localhost

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def find_element_by_link_text(self, text, time=10):
        wait = WebDriverWait(self.driver, time)
        return self.driver.find_element_by_link_text(text)

    def catalog_url_matches(self, time=10):
        if WebDriverWait(self.driver, time).until(EC.url_matches(r'http:\/\/localhost\/index\.php\?route=product\/category\&path\=\d*')):
            return True

    def swch_to_alert(self, time=2):
        alert = self.driver.switch_to_alert()
        self.driver.implicitly_wait(time)
        alert.accept()
        self.driver.implicitly_wait(time)
