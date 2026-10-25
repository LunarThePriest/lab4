from dataclasses import dataclass
from typing import Optional


@dataclass
class Brewery:
    id: Optional[int]
    name: str
    country: str
    email: str


@dataclass
class Beer:
    id: Optional[int]
    title: str
    style: str
    abv: float
    sku: str
    brewery_id: int
