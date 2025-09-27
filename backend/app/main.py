from __future__ import annotations

from difflib import SequenceMatcher
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from .database import get_db
from .models import Ingredient
from .schemas import IngredientRead, PaginatedIngredients

app = FastAPI(title="Flavor Index API", version="0.1.0")


@app.get("/healthz")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ingredients", response_model=PaginatedIngredients)
def list_ingredients(
    q: Optional[str] = Query(default=None, description="Optional search string."),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=25, gt=0, le=100),
    db: Session = Depends(get_db),
) -> PaginatedIngredients:
    base_query = db.query(Ingredient).options(
        joinedload(Ingredient.botanical_relatives),
        joinedload(Ingredient.related_ingredients),
        joinedload(Ingredient.flavor_affinities),
    )

    total_query = base_query
    if q:
        like_pattern = f"%{q.lower()}%"
        filtered_query = base_query.filter(func.lower(Ingredient.name).like(like_pattern))
        total = filtered_query.count()
        items = (
            filtered_query.order_by(Ingredient.name)
            .offset(offset)
            .limit(limit)
            .all()
        )

        if not items:
            all_items = base_query.all()
            ranked = sorted(
                all_items,
                key=lambda ingredient: SequenceMatcher(
                    None, q.lower(), ingredient.name.lower()
                ).ratio(),
                reverse=True,
            )
            total = len(ranked)
            items = ranked[offset : offset + limit]
    else:
        total = total_query.count()
        items = (
            base_query.order_by(Ingredient.name).offset(offset).limit(limit).all()
        )

    return PaginatedIngredients(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
        q=q,
    )


@app.get("/ingredients/{ingredient_id}", response_model=IngredientRead)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)) -> IngredientRead:
    ingredient = (
        db.query(Ingredient)
        .options(
            joinedload(Ingredient.botanical_relatives),
            joinedload(Ingredient.related_ingredients),
            joinedload(Ingredient.flavor_affinities),
        )
        .filter(Ingredient.id == ingredient_id)
        .one_or_none()
    )

    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    return ingredient


@app.get("/ingredients/search", response_model=PaginatedIngredients)
def search_ingredients(
    q: str = Query(description="Search string used for fuzzy matching."),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=25, gt=0, le=100),
    db: Session = Depends(get_db),
) -> PaginatedIngredients:
    return list_ingredients(q=q, offset=offset, limit=limit, db=db)
