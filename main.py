from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pydantic import BaseModel
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ---- Model ----
class Card(BaseModel):
    id: int
    question: str
    answer: str

# ---- Your 5 trivia cards (Objective #1) ----
card_list: list[Card] = [
    Card(id=1, question="Where do you go to school?", answer="At Taylor University"),
    Card(id=2, question="What is your favorite food?", answer="Hotpot"),
    Card(id=3, question="What church do you go to?", answer="FBCI"),
    Card(id=4, question="How many credits did you take this semester?", answer="15"),
    Card(id=5, question="Do you drive?", answer="Yes"),
]

# ---- "/" shows ALL cards in HTML (Objective #2) ----
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "cards": card_list},
    )

# ---- "/play" shows ONE random card (Objectives #3 & #4) ----
@app.get("/play", response_class=HTMLResponse)
async def play(request: Request):
    card = random.choice(card_list)
    return templates.TemplateResponse(
        "play.html",
        {"request": request, "card": card},
    )
