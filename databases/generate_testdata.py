from databases.db_client import DB_Client
import random


class TestProduct(DB_Client):

    def __init__(self):
        super(DB_Client, self).__init__()
        self.postfix = self.add_postfix()
        self.product_name = "MODEL_" + self.postfix
        self.product_model = "PRODUCT_" + self.postfix
        self.products = []

    @staticmethod
    def add_postfix():
        postfix = random.randint(0, 1000)
        postfix = str(postfix)
        return postfix

    def insert_product(self):

        oc_product_data = {'model': self.product_model, 'sku': '', 'upc': '', 'ean': '', 'jan': '', 'isbn': '', 'mpn': '',
                           'location': '', 'quantity': self.postfix, 'stock_status_id': '5', 'manufacturer_id': '7', 'shipping': '1',
                           'price': '100.0000', 'points': '11', 'tax_class_id': '9', 'date_available': '0000-00-00',
                           'weight': '0.00000000', 'weight_class_id': '1', 'length': '0.00000000', 'width': '0.00000000',
                           'height': '0.00000000', 'length_class_id': '2', 'subtract': '1', 'minimum': '1',
                           'sort_order': '0', 'status': '1', 'viewed': '0', 'date_added': DB_Client.global_date,
                           'date_modified': DB_Client.global_date}

        db_connect = DB_Client()

        db_connect.insert_data(table_name='oc_product', data=oc_product_data)

        pr_id = db_connect.select_data_by_key(table_name='oc_product', key='product_id', data={'model': self.product_model})
        prod_id = pr_id[0]

        oc_product_description_data = {'product_id': prod_id,
                                       'language_id': '1',
                                       'name': self.product_name,
                                       'description': 'Description',
                                       'tag': '',
                                       'meta_title': self.product_name,
                                       'meta_description': '',
                                       'meta_keyword': ''}

        db_connect.insert_data(table_name='oc_product_description', data=oc_product_description_data)

        self.products.append({'product_id': prod_id, 'product_name': self.product_name, 'product_model': self.product_model})
        return self.products

    def remove_product_data(self, id):
        db_connect = DB_Client()
        p_id = id
        pp = db_connect.select_data_by_key(table_name='oc_product_description', key='product_id', data={'product_id': p_id})
        if not pp == [] and not pp == None:
            try:
                db_connect.delete_data_by_key(table_name='oc_product_description',
                                                    data={'product_id': p_id})
            except Exception:
                raise Exception("No data found")
        elif pp == None:
            pass

        pp = db_connect.select_data_by_key(table_name='oc_product', key='product_id', data={'product_id': p_id})
        if not pp == [] and not pp == None:
            try:
                db_connect.delete_data_by_key(table_name='oc_product', data={'product_id': p_id})
            except Exception:
                raise Exception("No data found")
        elif pp == None:
            pass

        return p_id


