from abc import ABCMeta, abstractmethod
from uuid import UUID
from typing import Dict, List, Tuple, Text, Any
from tabelog_scraper.tabelog_scraper import scrape
from tabelogger.model.store import Store, Stores


class DataObject(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self, urls: List[str]) -> Stores:
        pass

    @abstractmethod
    def select_all(self) -> Stores:
        pass

    @abstractmethod
    def insert(self, store: Store) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class BackgroundTabelogScraper:
    def __init__(
            self,
            job_id: UUID,
            url: str,
            data_object: DataObject,
            logging,
            limit_page_count: int = 1) -> None:
        self.job_id: UUID = job_id
        self.url: str = url
        self.limit_page_count: int = limit_page_count
        self.data_object: DataObject = data_object
        self.logger = logging.get_logger(__name__)

    def __call__(self):
        jobs[self.job_id] = self
        try:
            stores = self.data_object.select_all()
            ignore_urls = stores.to_urls()

            print(f'{self.job_id}: scraping')
            scraping_result: Tuple[Dict[Text, Any]] = scrape(
                target_url=self.url,
                limit_page_count=self.limit_page_count,
                ignore_urls=ignore_urls)

            # データベースに挿入
            for store_dict in scraping_result:
                store = _to_store(store_dict)
                self.data_object.insert(store)
                print(f'{self.job_id}: insert {store.name}')

                # if self.is_cancelled:
                #     del jobs[self.job_id]
                #     break

        finally:
            # データ管理を閉じる
            self.data_object.close()
            print(f'{self.job_id}: finish')


jobs: Dict[UUID, BackgroundTabelogScraper] = {}


def _to_store(store_dict: Dict[Text, Any]) -> Store:
    return Store(
        name=store_dict['name'],
        rate=store_dict['rate'],
        address=store_dict['address'],
        address_image_url=store_dict['address_image_url'],
        url=store_dict['url'],
        navigation=store_dict['navigation']
    )
