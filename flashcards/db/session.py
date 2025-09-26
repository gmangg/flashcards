from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "database.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# reusable type annotation
SessionDep = Annotated[Session, Depends(get_session)]
