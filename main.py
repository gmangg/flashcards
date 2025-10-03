from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
import random

# local imports
from session import get_session        # because session.py is in project root
from flashcards.db.models import Card  # your Card model
from flashcards.routers import cards, sets

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()

# ---- Mount static files ----
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/playwithfriends", response_class=HTMLResponse)
def playwithfriends(request: Request):
    return templates.TemplateResponse("playwithfriends.html", {"request": request})

# ---- Routes ----
@app.get("/", response_class=HTMLResponse)
def index(request: Request, session: Session = Depends(get_session)):
    cards = session.exec(select(Card)).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "cards": cards},
    )


@app.get("/play", response_class=HTMLResponse)
def play(request: Request, session: Session = Depends(get_session)):
    cards = session.exec(select(Card)).all()
    card = random.choice(cards) if cards else None
    return templates.TemplateResponse(
        "play.html",
        {"request": request, "card": card},
    )


# ---- Include routers ----
app.include_router(cards.router)
app.include_router(sets.router)
