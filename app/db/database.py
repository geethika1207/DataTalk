from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..core.config import settings   
#  database.py is sitting inside the db room on Floor 1.
# To reach core — you cannot go directly. You must:

# Exit the db room first → ..
# Then enter the core room → core.config


from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()