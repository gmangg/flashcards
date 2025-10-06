from fastapi import APIRouter, Request, Form
from sqlmodel import select
from fastapi.responses import HTMLResponse, RedirectResponse
from ..db.session import get_session, SessionDep
from ..db.models import Card, Set
from ..core.templates import templates

router = APIRouter(prefix="/cards")

@router.get("/", response_class=HTMLResponse)
def get_cards(request: Request, session: SessionDep):
    cards = session.exec(select(Card).order_by(Card.front)).all()
    return templates.TemplateResponse("cards/cards.html", {"request": request, "cards": cards})

@router.get("/add", response_class=HTMLResponse)
def add_card_page(request: Request, session: SessionDep):
    sets = session.exec(select(Set)).all()
    return templates.TemplateResponse("cards/add.html", {"request": request, "sets": sets})

@router.post("/add")
def create_card(session: SessionDep, front: str = Form(...), back: str = Form(...), set_id: int = Form(...)):
    db_card = Card(front=front, back=back, set_id=set_id)
    session.add(db_card)
    session.commit()
    session.refresh(db_card)
    return RedirectResponse(url=f"/cards/{db_card.id}", status_code=302)

@router.get("/{card_id}/edit", response_class=HTMLResponse)
def edit_card(request: Request, session: SessionDep, card_id: int):
    card = session.exec(select(Card).where(Card.id == card_id)).first()
    sets = session.exec(select(Set)).all()
    return templates.TemplateResponse("cards/add.html", {"request": request, "card": card, "sets": sets})

@router.post("/{card_id}/delete")
def delete_card(session: SessionDep, card_id: int):
    card = session.get(Card, card_id)
    if card:
        session.delete(card)
        session.commit()
    return RedirectResponse(url="/cards/", status_code=302)
