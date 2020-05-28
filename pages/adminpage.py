from selenium.webdriver.common.by import By
from .base import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
from selenium.webdriver.common.keys import Keys


class AdminLoginPage(BasePage):
    username = (By.ID, 'input-username')
    password = (By.ID, 'input-password')

    MENU_CATALOG_LOCATOR = (By.ID, "menu-catalog")
    MENU_CATALOG_SUB_ITEMS_LOCATOR = (By.XPATH, "//ul[@id='collapse1']/li")
    BUTTON_ADD_NEW_LOCATOR = (By.XPATH, "//div[@id='content']/div[@class='page-header']//a[@data-original-title='Add New']")
    INPUT_NAME_LOCATOR = (By.XPATH, "//input[@id='input-name1']")
    INPUT_META_LOCATOR = (By.XPATH, "//input[@id='input-meta-title1']")
    NAV_TAB_LOCATOR = (By.XPATH, "//ul[@class='nav nav-tabs']/li")
    INPUT_MODEL_LOCATOR = (By.XPATH, "//input[@id='input-model']")
    BUTTON_SAVE_PRODUCT_LOCATOR = (By.XPATH, "//button[@data-original-title='Save']")
    TABLE_ROWS_LOCATOR = (By.XPATH, "//table[@class='table table-bordered table-hover']/tbody/tr")
    CHECKBOX_PRODUCT_LOCATOR = (By.XPATH, "//input[@type='checkbox']")
    DELETE_BUTTON_LOCATOR = (By.XPATH, "//button[@data-original-title='Delete']")
    EDIT_BUTTON_LOCATOR = (By.XPATH, "//a[@data-original-title='Edit']")

    submit_button = (By.CSS_SELECTOR, 'button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.url = self.base_url + "/admin/"

    def go_to(self):
        return self.driver.get(self.url)       # возвращается страница http://localhost/admin/

    def _set_username(self, name):
        self.find_element(locator=self.username, time=5).clear()
        self.find_element(locator=self.username, time=5).send_keys(name)

    def _set_password_(self, password):
        self.find_element(locator=self.password).clear()
        self.find_element(locator=self.password).send_keys(password)

    def login(self, username='user', password='bitnami1'):
        self._set_username(username)
        self._set_password_(password)
        self.find_element(locator=self.submit_button, time=5).click()

    def logout(self):
        pass

    def add_product(self, product_name='Some Product', product_meta='Some metadata', product_model='Some model'):
        product_params = [product_name, product_meta, product_model]
        catalog = self.find_element(locator=self.MENU_CATALOG_LOCATOR)
        catalog.click()

        products = self.find_elements(locator=self.MENU_CATALOG_SUB_ITEMS_LOCATOR)
        products[1].click()

        try:
            add_new = self.find_element(locator=self.BUTTON_ADD_NEW_LOCATOR)
            add_new.click()

            prod_name = self.find_element(locator=self.INPUT_NAME_LOCATOR)
            prod_name.click()
            prod_name.send_keys(product_params[0])

            meta = self.find_element(locator=self.INPUT_META_LOCATOR)
            meta.click()
            meta.send_keys(product_params[1])

            data_tab = self.find_elements(locator=self.NAV_TAB_LOCATOR)
            data_tab[1].click()

            data_model = self.find_element(locator=self.INPUT_MODEL_LOCATOR)
            data_model.click()
            data_model.send_keys(product_params[2])

            save = self.find_element(locator=self.BUTTON_SAVE_PRODUCT_LOCATOR)
            save.click()
            return products
        except TimeoutException:
            raise TimeoutException('Product not added')

    def check_prod_exist_by_name(self, product_name):
        ''' Function check product exist
            and returns list of items positions '''
        items_position = []
        table_rows = self.find_elements(locator=self.TABLE_ROWS_LOCATOR)
        for i in range(len(table_rows)):
            rows = self.find_elements(self.TABLE_ROWS_LOCATOR)
            row = rows[i]
            p = re.findall(product_name, row.text)
            if p != []:
                assert p[0] == product_name
                items_position.append(i)
        return items_position

    def go_to_products_table(self):
        catalog = self.find_element(locator=self.MENU_CATALOG_LOCATOR)
        catalog.click()

        products = self.find_elements(locator=self.MENU_CATALOG_SUB_ITEMS_LOCATOR)
        products[1].click()

    def delete_product_by_name(self, product_name):
        try:
            prod_pos_list = self.check_prod_exist_by_name(product_name)

            if prod_pos_list == []:
                pass

            elif len(prod_pos_list) >= 1:
                for i in range(len(prod_pos_list)):
                    checkbox = self.find_elements(self.CHECKBOX_PRODUCT_LOCATOR)
                    pos = prod_pos_list[i]
                    checkbox[pos + 1].click()
                    self.driver.implicitly_wait(2)

                del_btn = self.find_element(self.DELETE_BUTTON_LOCATOR)
                del_btn.click()
                self.driver.implicitly_wait(2)

                self.swch_to_alert(self.driver)

        except TimeoutException:
            raise TimeoutException('Delete not performed!')

    def edit_product(self, product_name_1, product_name_2):
        try:
            prod_pos_list = self.check_prod_exist_by_name(product_name_1)

            if prod_pos_list == []:
                pass

            elif len(prod_pos_list) == 1:
                checkbox = self.find_elements(self.CHECKBOX_PRODUCT_LOCATOR)
                pos = prod_pos_list[0]
                checkbox[pos + 1].click()
                self.driver.implicitly_wait(2)

                edit_btn = self.find_elements(self.EDIT_BUTTON_LOCATOR)
                edit_btn[pos + 1].click()

                prod_name = self.find_element(locator=self.INPUT_NAME_LOCATOR)
                prod_name.click()

                prod_name.send_keys(Keys.BACKSPACE * len(product_name_1))
                prod_name.send_keys(product_name_2)

                save = self.find_element(locator=self.BUTTON_SAVE_PRODUCT_LOCATOR)
                save.click()

        except TimeoutException:
            raise TimeoutException('Delete not performed!')