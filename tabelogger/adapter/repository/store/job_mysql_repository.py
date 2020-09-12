from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from tabelogger.config import pymysql_session
from tabelogger.model.job import Job, Jobs, JobRepository

session: Session = pymysql_session()


class JobMysqlRepository(JobRepository):
    def search(self, navigation: str, min_rate: float) -> Jobs:
        session: Session = pymysql_session()
        result = session.query(Job).filter(
            Job.navigation.like(f"%{navigation}%"),
            Job.rate >= min_rate,
        ).all()
        session.commit()
        return Jobs(result)

    def insert(self, job: Job) -> None:
        session = pymysql_session()
        try:
            print(f"ジョブを登録: {job}")
            session.add(job)
            session.commit()
        except Exception as e:
            print('insertエラー')
            print(e)
            session.rollback()

    def update(self, job_id: str, status: int) -> None:
        session = pymysql_session()
        try:
            print(f"ジョブを更新 {job_id} {status}")
            job = session.query(Job).filter(Job.job_id == job_id).first()
            job.status = status
            job.update_datetime = datetime.now()
            session.commit()
        except Exception as e:
            print('updateエラー')
            print(e)
            session.rollback()

    def select_all(self) -> Jobs:
        session: Session = pymysql_session()
        result = session.query(Job).order_by(desc(Job.create_datetime)).all()
        session.commit()
        return Jobs(result)
