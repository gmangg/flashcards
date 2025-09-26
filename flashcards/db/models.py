from sqlmodel import SQLModel, Field


class Set(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Card(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    front: str
    back: str
    set_id: int | None = Field(default=None, foreign_key="set.id")
