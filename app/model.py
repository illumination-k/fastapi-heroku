from sqlalchemy import Column, create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, TEXT


def create_new_engine():
    import os

    database_url = os.environ.get("DATABASE_URL")

    if database_url is None:
        uri = "postgresql://postgres:postgres@postgres-heroku:5432/main"
        echo = True
    else:
        uri = database_url.replace("postgres", "postgresql")
        echo = False

        return create_engine(url=uri, encoding="utf-8", echo=echo)


Engine = create_new_engine()

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=Engine)
)

Base = declarative_base()

# declare for query
Base.query = db_session.query_property()


class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(TEXT)
    created_at = Column(DateTime, default=func.now())


# Create Table
metadata = MetaData(Engine)
Base.metadata.create_all(bind=Engine, checkfirst=True)


# model to dict


def to_dict(model) -> dict:
    return dict((col.name, getattr(model, col.name)) for col in model.__table__.columns)
