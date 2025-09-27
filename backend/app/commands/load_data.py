from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from sqlalchemy import func

from ..database import session_scope
from ..models import (
    BotanicalRelative,
    FlavorAffinity,
    Ingredient,
    RelatedIngredient,
)


def normalise_list(items: Sequence[str] | str | None) -> list[str]:
    if items is None:
        return []

    if isinstance(items, str):
        candidates = [items]
    else:
        candidates = list(items)

    return [item.strip() for item in candidates if item and item.strip()]


def upsert_ingredient(payload: dict) -> None:
    fields = {
        "name": payload.get("name", "").strip(),
        "season": payload.get("season") or None,
        "taste": payload.get("taste") or None,
        "function": payload.get("function") or None,
        "weight": payload.get("weight") or None,
        "volume": payload.get("volume") or None,
        "technique": payload.get("technique") or None,
        "tips": payload.get("tips") or None,
    }

    if not fields["name"]:
        return

    botanical_relatives = normalise_list(payload.get("botanical_relatives"))
    related_ingredients = normalise_list(payload.get("related_ingredients"))
    flavor_affinities = normalise_list(payload.get("flavor_affinities"))

    with session_scope() as session:
        ingredient = (
            session.query(Ingredient)
            .filter(func.lower(Ingredient.name) == fields["name"].lower())
            .one_or_none()
        )

        if ingredient is None:
            ingredient = Ingredient(**fields)
            session.add(ingredient)
            session.flush()
        else:
            for key, value in fields.items():
                setattr(ingredient, key, value)

        ingredient.botanical_relatives.clear()
        ingredient.related_ingredients.clear()
        ingredient.flavor_affinities.clear()

        ingredient.botanical_relatives.extend(
            BotanicalRelative(name=name) for name in botanical_relatives
        )
        ingredient.related_ingredients.extend(
            RelatedIngredient(name=name) for name in related_ingredients
        )
        ingredient.flavor_affinities.extend(
            FlavorAffinity(description=description) for description in flavor_affinities
        )


def load_data(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    for ingredient in payload.get("ingredients", []):
        upsert_ingredient(ingredient)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Load flavor data into the database.")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "data" / "list.json",
        help="Path to the JSON file with ingredient data.",
    )
    args = parser.parse_args(argv)

    if not args.data.exists():
        raise FileNotFoundError(f"Data file not found: {args.data}")

    load_data(args.data)


if __name__ == "__main__":
    main()
