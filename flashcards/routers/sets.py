# flashcards/routers/sets.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import select
from ..db.session import SessionDep
from ..db.models import Set, Card
from ..core.templates import templates

router = APIRouter(prefix="/sets")


# ---- List all sets ----
@router.get("/", response_class=HTMLResponse)
def list_sets(request: Request, session: SessionDep):
    sets = session.exec(select(Set).order_by(Set.name)).all()
    return templates.TemplateResponse(
        "sets/sets.html",
        {"request": request, "sets": sets},
    )


# ---- Add set form ----
@router.get("/add", response_class=HTMLResponse)
def add_set_form(request: Request):
    return templates.TemplateResponse(
        "sets/add.html",
        {"request": request},
    )


# ---- Add set (POST) ----
@router.post("/add")
def create_set(name: str = Form(...), session: SessionDep = None):
    db_set = Set(name=name)
    session.add(db_set)
    session.commit()
    session.refresh(db_set)
    return RedirectResponse(url=f"/sets/{db_set.id}", status_code=302)


# ---- View single set ----
@router.get("/{set_id}", response_class=HTMLResponse)
def view_set(set_id: int, request: Request, session: SessionDep):
    set_obj = session.get(Set, set_id)
    cards = session.exec(select(Card).where(Card.set_id == set_id)).all()
    return templates.TemplateResponse(
        "sets/set_detail.html",
        {"request": request, "set": set_obj, "cards": cards},
    )
