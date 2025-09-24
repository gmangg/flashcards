from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Field, Session, create_engine, select
from starlette.templating import Jinja2Templates
import random

# ---- App setup ----
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---- Database setup ----
sqlite_file_name = "database.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# ---- Models ----
class Set(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Card(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question: str
    answer: str
    set_id: int | None = Field(default=None, foreign_key="set.id")

# ---- Startup ----
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ---- Routes ----
@app.get("/", response_class=HTMLResponse)
def index(request: Request, session: Session = Depends(get_session)):
    cards = session.exec(select(Card)).all()
    return templates.TemplateResponse("index.html", {"request": request, "cards": cards})

@app.get("/play", response_class=HTMLResponse)
def play(request: Request, session: Session = Depends(get_session)):
    cards = session.exec(select(Card)).all()
    card = random.choice(cards) if cards else None
    return templates.TemplateResponse("play.html", {"request": request, "card": card})

@app.get("/card/{card_id}", response_class=HTMLResponse)
def get_card(request: Request, card_id: int, session: Session = Depends(get_session)):
    card = session.get(Card, card_id)
    return templates.TemplateResponse("card.html", {"request": request, "card": card})

@app.post("/sets/add")
def create_set(set: Set, session: Session = Depends(get_session)):
    session.add(set)
    session.commit()
    session.refresh(set)
    return set

@app.post("/card/add")
def create_card(card: Card, session: Session = Depends(get_session)):
    session.add(card)
    session.commit()
    session.refresh(card)
    return card

@app.get("/sets", response_class=HTMLResponse)
def list_sets(request: Request, session: Session = Depends(get_session)):
    sets = session.exec(select(Set).order_by(Set.name)).all()
    return templates.TemplateResponse("sets.html", {"request": request, "sets": sets})

@app.get("/sets/{set_id}", response_class=HTMLResponse)
def view_set(request: Request, set_id: int, session: Session = Depends(get_session)):
    set_obj = session.get(Set, set_id)
    cards = session.exec(select(Card).where(Card.set_id == set_id)).all()
    return templates.TemplateResponse(
        "set_detail.html", {"request": request, "set": set_obj, "cards": cards}
    )
