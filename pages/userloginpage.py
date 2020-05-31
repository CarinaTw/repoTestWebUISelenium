from selenium.webdriver.common.by import By
from .base import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
from selenium.webdriver.common.keys import Keys


class UserLoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.url = self.base_url + '/index.php?route=account/login'

    def go_to(self):
        return self.driver.get(self.url)    # возвращается стр http://localhost/index.php?route=account/login
