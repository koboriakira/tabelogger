from pymysql import connect, cursors
from typing import List, Dict
from tabelogger.config import mysql_database_config
from tabelogger.job.background_tabelog_scraper import DataObject
from tabelogger.model.store import Store, Stores

INSERT_SQL = 'INSERT INTO stores(name, rate, address, address_image_url, url, navigation) VALUES(%(name)s, %(rate)s, %(address)s, %(address_image_url)s, %(url)s, %(navigation)s)'
TEST_DATA = {
    'name': 'test',
    'rate': 3.5,
    'address': 'address',
    'address_image_url': 'address_image_url',
    'url': 'url'
}


class MySqlDataObject(DataObject):
    def __init__(self) -> None:
        self.conn = connect(
            host=mysql_database_config['host'],
            db=mysql_database_config['db'],
            user=mysql_database_config['user'],
            passwd=mysql_database_config['passwd'],
            charset=mysql_database_config['charset'],
            cursorclass=cursors.DictCursor)

    def search(self, navigation: str, min_rate: float) -> Stores:
        c = self.conn.cursor()
        query = f"SELECT * FROM stores WHERE navigation like '%{navigation}%' AND rate > {min_rate};"
        result_amount = c.execute(query)
        if result_amount == 0:
            c.close()
            return Stores([])

        stores = []
        result_list: List[Dict] = c.fetchall()
        for result in result_list:
            name = result['name']
            rate = result['rate']
            address = result['address']
            address_image_url = result['address_image_url']
            url = result['url']
            navigation = result['navigation']
            store = Store(
                name=name,
                rate=rate,
                address=address,
                address_image_url=address_image_url,
                url=url,
                navigation=navigation)
            stores.append(store)

        c.close()
        return Stores(stores)

    def insert(self, store: Store) -> None:
        try:
            c = self.conn.cursor()
            # print('新しくデータを挿入します', store.name)
            c.execute(INSERT_SQL, store.to_entity())
            self.conn.commit()
            c.close()
        except Exception as e:
            print('insertエラー')
            print(e)

    def select_all(self) -> Stores:
        c = self.conn.cursor()
        query = "SELECT * FROM stores;"
        result_amount = c.execute(query)
        if result_amount == 0:
            c.close()
            return Stores([])

        stores = []
        result_list: List[Dict] = c.fetchall()
        for result in result_list:
            name = result['name']
            rate = result['rate']
            address = result['address']
            address_image_url = result['address_image_url']
            url = result['url']
            navigation = result['navigation']
            store = Store(
                name=name,
                rate=rate,
                address=address,
                address_image_url=address_image_url,
                url=url,
                navigation=navigation)
            stores.append(store)

        c.close()
        return Stores(stores)

    def close(self):
        self.conn.close()
