from app.db.session import engine
from app.db.base import Base

# Import the model so SQLAlchemy knows about it
from app.models.link import Link  # noqa: F401


def main():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")


if __name__ == "__main__":
    main()