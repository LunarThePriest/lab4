from abc import ABC, abstractmethod
from typing import Any

import psycopg
from psycopg.rows import dict_row

from .schemas import BeerCreate, BeerUpdate

DSN = "postgresql://postgres:postgres@localhost:5432/lab4_db"


class AbstractBeerRepository(ABC):

    @abstractmethod
    def get_all(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]: ...

    @abstractmethod
    def get_by_id(self, item_id: int) -> dict[str, Any] | None: ...

    @abstractmethod
    def create(self, item: BeerCreate) -> dict[str, Any]: ...

    @abstractmethod
    def update(self, item_id: int, item: BeerUpdate) -> dict[str, Any] | None: ...

    @abstractmethod
    def delete(self, item_id: int) -> bool: ...


class PostgresBeerRepository(AbstractBeerRepository):

    def __init__(self, dsn: str = DSN) -> None:
        self.dsn = dsn

    def get_all(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    "SELECT id, title, style, abv, sku, brewery_id FROM beers ORDER BY id LIMIT %s OFFSET %s;",
                    (limit, offset),
                )
                return list(cur.fetchall())

    def get_by_id(self, item_id: int) -> dict[str, Any] | None:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    "SELECT id, title, style, abv, sku, brewery_id FROM beers WHERE id = %s;",
                    (item_id,),
                )
                return cur.fetchone()

    def create(self, item: BeerCreate) -> dict[str, Any]:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    INSERT INTO beers (title, style, abv, sku, brewery_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, title, style, abv, sku, brewery_id;
                    """,
                    (item.title, item.style, item.abv, item.sku, item.brewery_id),
                )
                res = cur.fetchone()
                conn.commit()
                if res is None:
                    raise RuntimeError("Не вдалося створити запис у базі даних.")
                return res

    def update(self, item_id: int, item: BeerUpdate) -> dict[str, Any] | None:
        existing = self.get_by_id(item_id)
        if not existing:
            return None

        title = item.title if item.title is not None else existing["title"]
        style = item.style if item.style is not None else existing["style"]
        abv = item.abv if item.abv is not None else existing["abv"]
        sku = item.sku if item.sku is not None else existing["sku"]
        brewery_id = item.brewery_id if item.brewery_id is not None else existing["brewery_id"]

        with psycopg.connect(self.dsn) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    UPDATE beers
                    SET title = %s, style = %s, abv = %s, sku = %s, brewery_id = %s
                    WHERE id = %s
                    RETURNING id, title, style, abv, sku, brewery_id;
                    """,
                    (title, style, abv, sku, brewery_id, item_id),
                )
                res = cur.fetchone()
                conn.commit()
                return res

    def delete(self, item_id: int) -> bool:
        with psycopg.connect(self.dsn) as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM beers WHERE id = %s;", (item_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted
