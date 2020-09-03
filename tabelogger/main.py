import uuid
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from tabelogger.job.background_tabelog_scraper import BackgroundTabelogScraper
from tabelogger.adapter.data_object.mysql_data_object import MySqlDataObject
from tabelogger.adapter.logger.fastapi_logging import FastapiLogging
from tabelogger.model.store import Stores

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


@app.get("/recommend/{navigation}")
def recommend(navigation: str, min_rate: float = 3.0):
    # logger = FastapiLogging().get_logger(__name__)
    # logger.info("recommendを実行")
    print(f"[recommend] navigation:{navigation}, min_rate:{min_rate}")
    stores: Stores = MySqlDataObject().search(
        navigation=navigation, min_rate=min_rate)
    return stores


@app.get("/scrape")
def scrape(background_tasks: BackgroundTasks, url: str, limit_page_count: str):
    job_id: uuid.UUID = uuid.uuid1()
    t = BackgroundTabelogScraper(
        job_id=job_id,
        url=url,
        limit_page_count=int(limit_page_count),
        logging=FastapiLogging(),
        data_object=MySqlDataObject(),
    )
    background_tasks.add_task(t)

    return {
        "job_id": job_id,
        "url": url,
        "limit_page_count": limit_page_count
    }
