import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True)
class Store:
    name: str
    rate: float
    address: str
    address_image_url: str
    url: str
    navigation: str

    def __str__(self):
        return 'name:' + self.name + ' rate:' + \
            str(self.rate) + ' url:' + self.url

    def is_high_rating(self) -> bool:
        return self.rate >= 3.5 and self.rate <= 5.0

    def latitude_longitude(self) -> List[str]:
        return self.address_image_url.split(
            "&center=")[1].split("&style=")[0].split(",")

    def to_entity(self):
        return {
            'name': self.name,
            'rate': self.rate,
            'address': self.address,
            'address_image_url': self.address_image_url,
            'url': self.url,
            'navigation': self.navigation
        }


@dataclasses.dataclass
class Stores:
    stores: List[Store]

    def to_urls(self) -> List[str]:
        return list(map(lambda s: s.url, self.stores))

    def __str__(self) -> str:
        return ",".join(list(map(lambda s: str(s), self.stores)))
