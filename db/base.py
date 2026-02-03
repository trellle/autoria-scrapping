from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, MetaData
from db.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    metadata = MetaData()
