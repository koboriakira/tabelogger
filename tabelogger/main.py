from tabelogger.adapter.repository.store.job_mysql_repository import JobMysqlRepository
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from tabelogger.job.background_tabelog_scraper import BackgroundTabelogScraper
from tabelogger.adapter.repository.store.store_mysql_repository import StoreMysqlRepository
from tabelogger.adapter.logger.fastapi_logging import FastapiLogging
from tabelogger.model.store import Stores
from tabelogger.model.job import Job

app = FastAPI()

# CORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/recommend")
def recommend(
    navigation: str = '',
    latitude: float = 0,
    longitude: float = 0,
    distance: int = 0,
    min_rate: float = 0,
):
    print(
        f"[recommend] navigation:{navigation}, min_rate:{min_rate}, latitude:{latitude}, longitude:{longitude}")
    stores: Stores = StoreMysqlRepository().search(
        navigation=navigation, min_rate=min_rate)
    stores = stores.filter_geo_location(latitude, longitude, distance)
    print(stores)
    return stores


@ app.get("/scrape")
def scrape(
        background_tasks: BackgroundTasks,
        url: str,
        limit_page_count: int = 1):
    job = Job.create(url, limit_page_count)
    t = BackgroundTabelogScraper(
        job=job,
        logging=FastapiLogging(),
        job_repository=JobMysqlRepository(),
        store_repository=StoreMysqlRepository(),
    )
    background_tasks.add_task(t)
    return job


@ app.get("/jobs")
def jobs():
    jobs = JobMysqlRepository().select_all()
    print(jobs)
    return jobs
