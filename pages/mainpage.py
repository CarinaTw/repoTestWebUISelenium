from selenium.webdriver.common.by import By
from .base import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
from selenium.webdriver.common.keys import Keys


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.url = self.base_url

    def go_to(self):
        return self.driver.get(self.url)       # возвращается страница http://localhost
