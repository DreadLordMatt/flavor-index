"""Initial database schema for the Flavor Index backend."""

from backend.app.database import engine
from backend.app.models import Base


def run() -> None:
    """Create all tables defined in the SQLAlchemy metadata."""

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    run()
