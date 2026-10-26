import re

from pydantic import BaseModel, Field, field_validator

SKU_REGEX = r"^BEER-\d{4}$"
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class BreweryBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=50)
    email: str

    @field_validator("email")
    def validate_email_format(cls, v: str) -> str:
        if not re.match(EMAIL_REGEX, v):
            raise ValueError(
                "Email повинен мати коректний формат, наприклад: user@domain.com"
            )
        return v


class BreweryCreate(BreweryBase):
    pass


class BreweryResponse(BreweryBase):
    id: int


class BeerBase(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    style: str = Field(min_length=2, max_length=50)
    abv: float = Field(ge=0.0, le=100.0)
    sku: str
    brewery_id: int

    @field_validator("sku")
    def validate_sku_format(cls, v: str) -> str:
        if not re.match(SKU_REGEX, v):
            raise ValueError(
                "SKU має відповідати шаблону 'BEER-XXXX' (наприклад: BEER-1001)"
            )
        return v


class BeerCreate(BeerBase):
    pass


class BeerUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    style: str | None = Field(default=None, min_length=2, max_length=50)
    abv: float | None = Field(default=None, ge=0.0, le=100.0)
    sku: str | None = None
    brewery_id: int | None = None

    @field_validator("sku")
    def validate_sku_format(cls, v: str | None) -> str | None:
        if v is not None and not re.match(SKU_REGEX, v):
            raise ValueError("SKU має відповідати шаблону 'BEER-XXXX'")
        return v


class BeerResponse(BeerBase):
    id: int
