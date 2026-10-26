from dataclasses import dataclass


@dataclass
class Brewery:
    id: int | None
    name: str
    country: str
    email: str


@dataclass
class Beer:
    id: int | None
    title: str
    style: str
    abv: float
    sku: str
    brewery_id: int
