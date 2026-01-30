from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Teraser0000Pro@localhost:5432/codewars_tracker"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def db_add(data):
    db = SessionLocal()
    db.add(data)
    db.commit()
    db.refresh(data)

Base = declarative_base()