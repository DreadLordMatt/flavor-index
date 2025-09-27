from typing import List, Optional

from pydantic import BaseModel


class BotanicalRelativeRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class RelatedIngredientRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class FlavorAffinityRead(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True


class IngredientBase(BaseModel):
    name: str
    season: Optional[str] = None
    taste: Optional[str] = None
    function: Optional[str] = None
    weight: Optional[str] = None
    volume: Optional[str] = None
    technique: Optional[str] = None
    tips: Optional[str] = None


class IngredientRead(IngredientBase):
    id: int
    botanical_relatives: List[BotanicalRelativeRead]
    related_ingredients: List[RelatedIngredientRead]
    flavor_affinities: List[FlavorAffinityRead]

    class Config:
        orm_mode = True


class PaginatedIngredients(BaseModel):
    items: List[IngredientRead]
    total: int
    limit: int
    offset: int
    q: Optional[str] = None
