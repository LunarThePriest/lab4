from typing import List
from fastapi import FastAPI, HTTPException, Query, status

from .repositories import AbstractBeerRepository, PostgresBeerRepository
from .schemas import BeerCreate, BeerResponse, BeerUpdate

app = FastAPI(
    title="Beer & Breweries Management API",
    description="Лабораторна робота №4: REST API з Data Persistence",
    version="1.0.0",
)


def get_beer_repository() -> AbstractBeerRepository:
    return PostgresBeerRepository()


@app.get("/beers", response_model=List[BeerResponse], status_code=status.HTTP_200_OK)
def list_beers(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    repo = get_beer_repository()
    return repo.get_all(limit=limit, offset=offset)


@app.get("/beers/{beer_id}", response_model=BeerResponse, status_code=status.HTTP_200_OK)
def get_beer(beer_id: int):
    repo = get_beer_repository()
    beer = repo.get_by_id(beer_id)
    if beer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пиво з id={beer_id} не знайдено",
        )
    return beer


@app.post("/beers", response_model=BeerResponse, status_code=status.HTTP_201_CREATED)
def create_beer(beer_in: BeerCreate):
    repo = get_beer_repository()
    try:
        return repo.create(beer_in)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Помилка створення: {str(exc)}",
        )


@app.put("/beers/{beer_id}", response_model=BeerResponse, status_code=status.HTTP_200_OK)
def update_beer(beer_id: int, beer_in: BeerUpdate):
    repo = get_beer_repository()
    updated = repo.update(beer_id, beer_in)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пиво з id={beer_id} не знайдено для оновлення",
        )
    return updated


@app.delete("/beers/{beer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_beer(beer_id: int):
    repo = get_beer_repository()
    deleted = repo.delete(beer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пиво з id={beer_id} не знайдено для видалення",
        )
    return None
