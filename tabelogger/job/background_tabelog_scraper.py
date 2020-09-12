from tabelogger.model.job import Job, JobRepository, JobStatus
from typing import Dict, List, Tuple, Text, Any
from tabelog_scraper.tabelog_scraper import scrape
from tabelogger.model.store import Store, StoreRepository


class BackgroundTabelogScraper:
    def __init__(
            self,
            job: Job,
            store_repository: StoreRepository,
            job_repository: JobRepository,
            logging) -> None:
        self.job: Job = job
        self.job_repository: JobRepository = job_repository
        self.store_repository: StoreRepository = store_repository
        self.logger = logging.get_logger(__name__)

    def __call__(self):
        self.job_repository.insert(self.job)
        try:
            store_list = self.__scrape()
            for store in store_list:
                self.__insert(store)
            self.job_repository.update(
                self.job.job_id, JobStatus.COMPLETE.value)
        except Exception as e:
            print(e)
            self.job_repository.update(
                self.job.job_id, JobStatus.ERROR.value)
        finally:
            print(f'{self.job.job_id}: finish')

    def __get_ignore_urls(self) -> List[str]:
        stores = self.store_repository.select_all()
        return stores.to_urls()

    def __scrape(self) -> List[Store]:
        print(f'{self.job.job_id}: scraping')
        results: Tuple[Dict[Text, Any]] = scrape(
            target_url=self.job.url,
            limit_page_count=self.job.limit_page_count,
            ignore_urls=self.__get_ignore_urls())
        return list(map(lambda res: Store(**res), results))

    def __insert(self, store) -> None:
        self.store_repository.insert(store)
        print(f'{self.job.job_id}: insert {store.name}')


# jobs: Dict[UUID, BackgroundTabelogScraper] = {}
