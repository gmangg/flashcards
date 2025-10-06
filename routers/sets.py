from fastapi import APIRouter, Request, Form
from sqlmodel import select
from fastapi.responses import HTMLResponse, RedirectResponse
from ..db.session import get_session, SessionDep
from ..db.models import Set
from ..core.templates import templates

router = APIRouter(prefix="/sets")

@router.get("/", response_class=HTMLResponse)
def get_sets(request: Request, session: SessionDep):
    sets = session.exec(select(Set).order_by(Set.name)).all()
    return templates.TemplateResponse("sets/sets.html", {"request": request, "sets": sets})

@router.get("/add", response_class=HTMLResponse)
def add_set_page(request: Request):
    return templates.TemplateResponse("sets/add.html", {"request": request})

@router.post("/add")
def create_set(session: SessionDep, name: str = Form(...)):
    db_set = Set(name=name)
    session.add(db_set)
    session.commit()
    session.refresh(db_set)
    return RedirectResponse(url="/sets/", status_code=302)

@router.get("/{set_id}/edit", response_class=HTMLResponse)
def edit_set(request: Request, session: SessionDep, set_id: int):
    set_obj = session.exec(select(Set).where(Set.id == set_id)).first()
    return templates.TemplateResponse("sets/add.html", {"request": request, "set": set_obj})

@router.post("/{set_id}/edit")
def update_set(session: SessionDep, set_id: int, name: str = Form(...)):
    set_obj = session.get(Set, set_id)
    if set_obj:
        set_obj.name = name
        session.add(set_obj)
        session.commit()
    return RedirectResponse(url="/sets/", status_code=302)

@router.post("/{set_id}/delete")
def delete_set(session: SessionDep, set_id: int):
    set_obj = session.get(Set, set_id)
    if set_obj:
        # delete all cards in the set
        for card in set_obj.cards:
            session.delete(card)
        session.delete(set_obj)
        session.commit()
    return RedirectResponse(url="/sets/", status_code=302)
