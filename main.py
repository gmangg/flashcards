# flashcards/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import select
import random

from .core.templates import templates
from .routers import cards, sets
from .db.session import create_db_and_tables, SessionDep
from .db.models import Card

# ---- App setup ----
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---- Startup ----
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ---- Routes ----
@app.get("/", response_class=HTMLResponse)
def index(request: Request, session: SessionDep):
    cards = session.exec(select(Card)).all()
    return templates.TemplateResponse("index.html", {"request": request, "cards": cards})


@app.get("/play", response_class=HTMLResponse)
def play(request: Request, session: Session = Depends(get_session)):
    from .db.models import Card
    cards = session.exec(select(Card)).all()
    card = random.choice(cards) if cards else None
    return templates.TemplateResponse(
        "play.html", 
        {"request": request, "card": card, "card_macro": templates.get_template("card.html").module}
    )


# ---- Include routers ----
app.include_router(cards.router)
app.include_router(sets.router)
