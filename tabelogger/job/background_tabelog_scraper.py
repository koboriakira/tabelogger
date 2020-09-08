from abc import ABCMeta, abstractmethod
from uuid import UUID
from typing import Dict, List, Tuple, Text, Any
from tabelog_scraper.tabelog_scraper import scrape
from tabelogger.model.store import Store, StoreRepository


class BackgroundTabelogScraper:
    def __init__(
            self,
            job_id: UUID,
            url: str,
            store_repository: StoreRepository,
            logging,
            limit_page_count: int = 1) -> None:
        self.job_id: UUID = job_id
        self.url: str = url
        self.limit_page_count: int = limit_page_count
        self.store_repository: StoreRepository = store_repository
        self.logger = logging.get_logger(__name__)

    def __call__(self):
        jobs[self.job_id] = self
        try:
            store_list = self.__scrape()
            for store in store_list:
                self.__insert(store)
        finally:
            print(f'{self.job_id}: finish')

    def __get_ignore_urls(self) -> List[str]:
        stores = self.store_repository.select_all()
        return stores.to_urls()

    def __scrape(self) -> List[Store]:
        print(f'{self.job_id}: scraping')
        results: Tuple[Dict[Text, Any]] = scrape(
            target_url=self.url,
            limit_page_count=self.limit_page_count,
            ignore_urls=self.__get_ignore_urls())
        return list(map(lambda res: Store(**res), results))

    def __insert(self, store) -> None:
        self.store_repository.insert(store)
        print(f'{self.job_id}: insert {store.name}')


jobs: Dict[UUID, BackgroundTabelogScraper] = {}
