from __future__ import annotations
from abc import ABCMeta, abstractmethod
import dataclasses
from typing import List, Tuple
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from geopy.distance import geodesic

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

    def pos(self) -> Tuple[float]:
        """
        経度、緯度のタプルを返却します
        """
        param: List[str] = self.address_image_url.split(
            "&center=")[1].split("&style=")[0].split(",")
        return tuple(map(lambda el: float(el), param))

    def __str__(self):
        return self.name


@dataclasses.dataclass
class Stores:
    size: int = dataclasses.field(default=0, init=False)
    stores: List[Store]

    def __post_init__(self):
        self.size = len(self.stores)

    def filter_geo_location(
            self,
            latitude: float,
            longitude: float,
            distance) -> Stores:
        """
        指定された経度・緯度と距離をもとに、対象を店をしぼります
        """
        if not latitude:
            return self
        if not longitude:
            return self

        result: List[Store] = []
        my_pos = (latitude, longitude)
        for store in self.stores:
            dis = geodesic(my_pos, store.pos()).m
            print('distance:', dis)
            if dis < distance:
                result.append(store)
        return Stores(result)

    def to_urls(self) -> List[str]:
        return list(map(lambda s: s.url, self.stores))

    def __str__(self) -> str:
        return ",".join(list(map(lambda s: str(s), self.stores)))
