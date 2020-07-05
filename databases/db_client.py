import mysql.connector


class DB_Client:
    global_date = '2020-06-28 00:00:00'

    def __init__(self):
        self.my_connection = mysql.connector.connect(user='root',
                                                host='0.0.0.0',
                                                port='3306',
                                                database='bitnami_opencart')

    def select_data_by_key(self, table_name: str, key: str, data: dict):
        cur = self.my_connection.cursor()
        select_sql = f"""SELECT {key} from {table_name} WHERE {list(data.keys())[0]} = "{list(data.values())[0]}" """
        cur.execute(select_sql)
        return cur.fetchone()

    def insert_data(self, table_name: str, data: dict):
        keys = ','.join(list(data.keys()))

        vals = []

        for item in list(data.values()):
            if isinstance(item, int):
                vals.append(f'{item}')
            if isinstance(item, str):
                value = item.replace("'", "''") if "'" in item else item
                vals.append(f"'{value}'")

        vals = ','.join(vals)

        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, keys, vals)

        cur = self.my_connection.cursor()
        cur.execute(sql)

        self.my_connection.commit()
        return self.my_connection.commit()

    def delete_data_by_key(self, table_name: str, data: dict):
        cur = self.my_connection.cursor()

        prod_id = self.select_data_by_key(table_name=table_name, key='product_id', data=data)

        sql_del = f"""DELETE FROM {table_name} WHERE {list(data.keys())[0]} = "{list(data.values())[0]}" """

        cur.execute(sql_del)
        self.my_connection.commit()
        return self.my_connection.commit(), prod_id[0]
