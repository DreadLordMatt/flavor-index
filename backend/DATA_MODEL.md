# Flavor Index Data Model

The backend organizes culinary knowledge around a central `ingredients` table and a trio of detail tables that capture relationships and tasting notes. All tables are managed through SQLAlchemy models in [`backend/app/models.py`](app/models.py) and are automatically created by the migration in [`backend/migrations/0001_create_tables.py`](migrations/0001_create_tables.py).

## Tables

### `ingredients`
* **Primary key:** `id` (integer, auto-increment)
* **Unique name:** `name` ensures each ingredient is stored once.
* **Descriptive attributes:** `season`, `taste`, `function`, `weight`, and `volume` store short free-form descriptors that power filtering and search.
* **Narrative fields:** `technique` and `tips` capture longer guidance pulled from the source material.
* **Relationships:**
  * One-to-many with [`botanical_relatives`](#botanical_relatives)
  * One-to-many with [`related_ingredients`](#related_ingredients)
  * One-to-many with [`flavor_affinities`](#flavor_affinities)

Every related record cascades deletes through the `ingredient_id` foreign key, so removing an ingredient automatically clears its dependent notes.

### `botanical_relatives`
* **Primary key:** `id`
* **Foreign key:** `ingredient_id` references `ingredients.id`
* **Content:** `name` holds a single relative (plant family or closely related item) for display in the UI.

### `related_ingredients`
* **Primary key:** `id`
* **Foreign key:** `ingredient_id`
* **Content:** `name` holds a complementary ingredient that pairs well with the base ingredient.

### `flavor_affinities`
* **Primary key:** `id`
* **Foreign key:** `ingredient_id`
* **Content:** `description` stores multiline affinity text directly from the Flavor Bible source, preserving formatting for later rendering.

## ORM relationships and serialization

SQLAlchemy back-populated relationships on the `Ingredient` model expose each child collection via `ingredient.botanical_relatives`, `ingredient.related_ingredients`, and `ingredient.flavor_affinities`. These lists are eagerly available when loading an ingredient, and they are serialized with Pydantic response schemas defined in [`backend/app/schemas.py`](app/schemas.py).

The API returns fully expanded ingredient payloads, with pagination handled by the `PaginatedIngredients` schema that wraps:

```json
{
  "items": [
    {
      "id": 1,
      "name": "Apple",
      "botanical_relatives": [ ... ],
      "related_ingredients": [ ... ],
      "flavor_affinities": [ ... ]
    }
  ],
  "total": 1,
  "limit": 25,
  "offset": 0,
  "q": "apple"
}
```

This structure keeps the client simple while leaving room to add additional joins (for example, tagging or regional notes) without breaking existing responses.
