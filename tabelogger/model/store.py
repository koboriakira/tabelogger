from __future__ import annotations
from abc import ABCMeta, abstractmethod
import dataclasses
from typing import List
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StoreRepository(object):
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


class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(1000))
    navigation = Column(String(1000))
    rate = Column(Float)
    address = Column(String(1000))
    address_image_url = Column(String(2083))
    url = Column(String(767))

    def is_high_rating(self) -> bool:
        return self.rate >= 3.5 and self.rate <= 5.0

    def latitude_longitude(self) -> List[str]:
        return self.address_image_url.split(
            "&center=")[1].split("&style=")[0].split(",")

    def __str__(self):
        return self.name


@dataclasses.dataclass
class Stores:
    stores: List[Store]

    def to_urls(self) -> List[str]:
        return list(map(lambda s: s.url, self.stores))

    def __str__(self) -> str:
        return ",".join(list(map(lambda s: str(s), self.stores)))
