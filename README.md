# Flavor Index and Relationships
The objective of this project is to digitize one of my favourite culinary books "The Flavor Bible" by Karen Page and Andrew Dornenburg. The book is excellent and gives insight into improving creativity, enhanceing the eating expierence and impact of a dish. Page and Dornenburg have provided readers with a thorough tool which can be used as a reference while cooking. The book contains some 500 charts, describing the relationship between an ingredient, cuisine, flavor, and taste.

Over the last 5 years I've used this book countless times, and finally relented to the nagging voice in my head. The primary issue I've identified is flipping between multiple ingredients as a build out a dish. To combat this, I've presented the book as a web page with search functionality.

## Credits:
If you like this idea and want to learn more about the book, please support the authors and pick up a copy. They can be purchased from [Amazon](https://www.amazon.ca/gp/product/0316118400/ref=dbs_a_def_rwt_bibl_vppi_i0) or direct [from the authors](https://karenandandrew.com/books/the-flavor-bible/).

## PY Processing of ebook
Using a epub of the book we can strip the required text and process with a short python script. Once the data is cleaned and organized it can be passed to a front end web app for presentation. The is built in Vue.js and allows each ingredient to be retrieved, and presented via search in a text box, or via an alphabet line. 

# Next Steps
Future Functionality:
* Based on the flavor relation weight matrix groups of ingredients can be entered in a list and an overall score calculated
* Web recipes can be passed from jackcooks.ca to evaluate them and give a score
* Suggestions for added ingredients based on a recipe or list, to improve the score
* Relationship graphing: social graphs can be modeled, showing the relationship, and ingredient families

## Backend service

The repository now includes a lightweight FastAPI backend under `backend/` that exposes the ingredient dataset via a
relational database. The service reads its configuration from environment variables and defaults to SQLite for local
development while supporting PostgreSQL/MySQL deployments through the `FLAVOR_INDEX_DATABASE_URL` setting.

### Local setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create the schema
python -m backend.migrations.0001_create_tables

# Load the dataset from data/list.json
python -m backend.app.commands.load_data

# Start the API
uvicorn backend.app.main:app --reload
```

`uvicorn` binds to `http://127.0.0.1:8000` by default. The FastAPI interactive documentation is available at
`http://127.0.0.1:8000/docs` once the server is running.

### Configuration

Set the following optional environment variables to tailor the deployment:

| Variable | Description | Default |
| --- | --- | --- |
| `FLAVOR_INDEX_DATABASE_URL` | SQLAlchemy connection URL. | SQLite database in the repository root. |
| `FLAVOR_INDEX_ENVIRONMENT` | Arbitrary environment name (e.g., `production`). | `development` |

When pointing to PostgreSQL or MySQL provide a URL such as `postgresql+psycopg2://user:password@host/dbname`.

### Database migrations

New schema revisions should be recorded under `backend/migrations/`. The initial migration (`0001_create_tables.py`)
materialises the SQLAlchemy models. Execute migrations in sequence to keep environments consistent.

### Data loading command

Run the seeding script whenever the ingredient dataset changes:

```bash
python -m backend.app.commands.load_data --data /path/to/list.json
```

The command upserts ingredient records and their botanical relatives, related ingredients, and flavor affinities so
deployments remain synchronised with `data/list.json` or other parsers.

### REST API

| Method & Path | Description |
| --- | --- |
| `GET /healthz` | Lightweight health probe. |
| `GET /ingredients` | Paginated list of ingredients. Supports optional `q`, `offset`, and `limit` query parameters for search and pagination. |
| `GET /ingredients/{id}` | Retrieve a single ingredient with its botanical relatives, related ingredients, and flavor affinities. |
| `GET /ingredients/search` | Convenience endpoint that performs fuzzy search with the same pagination parameters as `/ingredients`. |

#### Searching

Provide the `q` parameter to search for ingredients. The service first applies case-insensitive substring matching. When no
direct matches are found it falls back to a lightweight fuzzy matcher (based on Python's `SequenceMatcher`) to surface close
results. Use the `offset` and `limit` parameters to page through the response payload, which also includes the total result
count for UI integration.
