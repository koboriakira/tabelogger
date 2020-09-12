from __future__ import annotations
from enum import Enum
from abc import ABCMeta, abstractmethod
import dataclasses
from typing import List, Tuple
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JobRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self, urls: List[str]) -> Jobs:
        pass

    @abstractmethod
    def select_all(self) -> Jobs:
        pass

    @abstractmethod
    def insert(self, job: Job) -> None:
        pass

    @abstractmethod
    def update(self, job_id: str, status: int) -> None:
        pass


class JobStatus(Enum):
    RUNNING = 1
    COMPLETE = 2
    ERROR = 9


class Job(Base):
    __tablename__ = 'jobs'
    job_id = Column(String(100), primary_key=True)
    status = Column(Integer)
    url = Column(String(767))
    limit_page_count = Column(Integer)
    create_datetime = Column(DateTime)
    update_datetime = Column(DateTime)

    def update_complete(self) -> None:
        self.status = JobStatus.COMPLETE.value
        self.update_datetime = datetime.now()

    def update_error(self) -> None:
        self.status = JobStatus.ERROR.value
        self.update_datetime = datetime.now()

    @classmethod
    def create(cls, url: str, limit_page_count: int = 1) -> Job:
        job_id: str = str(uuid.uuid1())
        status: int = JobStatus.RUNNING.value
        now = datetime.now()
        return Job(
            job_id=job_id,
            status=status,
            url=url,
            limit_page_count=limit_page_count,
            create_datetime=now,
            update_datetime=now
        )

    def __str__(self) -> str:
        return self.job_id


@dataclasses.dataclass
class Jobs:
    jobs: List[Job]

    def __str__(self) -> str:
        return ",".join(list(map(lambda s: str(s), self.jobs)))
