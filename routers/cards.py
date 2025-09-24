from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import select
from ..db.session import get_session, SessionDep
from ..db.models import Card, Set
from ..core.templates import templates

router = APIRouter(prefix="/cards")


# ---- List all cards ----
@router.get("/", response_class=HTMLResponse)
def get_cards(request: Request, session: SessionDep):
    cards = session.exec(select(Card)).all()
    return templates.TemplateResponse(
        "cards/cards.html",
        {"request": request, "cards": cards},
    )


# ---- Add card form ----
@router.get("/add", response_class=HTMLResponse)
def add_card_form(request: Request, session: SessionDep):
    sets = session.exec(select(Set)).all()
    return templates.TemplateResponse(
        "cards/add.html",
        {"request": request, "sets": sets},
    )


# ---- Add card (POST) ----
@router.post("/add")
def create_card(
    session: SessionDep,
    front: str = Form(...),
    back: str = Form(...),
    set_id: int = Form(...),
):
    db_card = Card(front=front, back=back, set_id=set_id)
    session.add(db_card)
    session.commit()
    session.refresh(db_card)
    return RedirectResponse(url=f"/cards/{db_card.id}", status_code=302)


# ---- View single card ----
@router.get("/{card_id}", response_class=HTMLResponse)
def get_card(card_id: int, request: Request, session: SessionDep):
    card = session.get(Card, card_id)
    if not card:
        return HTMLResponse("<h1>Card not found</h1>", status_code=404)
    return templates.TemplateResponse(
        "cards/card.html",
        {"request": request, "card": card},
    )
