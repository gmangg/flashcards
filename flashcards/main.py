from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, create_engine, select
from .core.templates import templates
from .routers import cards, sets
import random

# ---- App setup ----
app = FastAPI()

# 👇 Mount static files correctly (works if "static/" is in project root)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---- Database setup ----
sqlite_file_name = "database.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# ---- Startup ----
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ---- Homepage ----
@app.get("/", response_class=HTMLResponse)
def index(request: Request, session: Session = Depends(get_session)):
    from .db.models import Card  # avoid circular imports
    cards = session.exec(select(Card)).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "cards": cards},
    )


# ---- Play Route ----
@app.get("/play", response_class=HTMLResponse)
def play(request: Request, session: Session = Depends(get_session)):
    from .db.models import Card
    cards = session.exec(select(Card)).all()
    card = random.choice(cards) if cards else None
    return templates.TemplateResponse(
        "play.html",
        {"request": request, "card": card},
    )


# ---- Routers ----
app.include_router(cards.router)
app.include_router(sets.router)


# ---- Debug: List routes (optional, remove later) ----
for route in app.routes:
    print("ROUTE:", route)
