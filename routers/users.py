from fastapi import APIRouter, Request, Form
from sqlmodel import select
from fastapi.responses import HTMLResponse, RedirectResponse
from ..db.session import get_session, SessionDep
from ..db.models import User
from ..core.templates import templates

router = APIRouter(prefix="/users")

@router.get("/", response_class=HTMLResponse)
def get_users(request: Request, session: SessionDep):
    users = session.exec(select(User).order_by(User.name)).all()
    return templates.TemplateResponse("users/users.html", {"request": request, "users": users})

@router.get("/add", response_class=HTMLResponse)
def add_user_page(request: Request):
    return templates.TemplateResponse("users/add.html", {"request": request})

@router.post("/add")
def create_user(session: SessionDep, name: str = Form(...)):
    db_user = User(name=name)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return RedirectResponse(url="/users/", status_code=302)

@router.get("/{user_id}/edit", response_class=HTMLResponse)
def edit_user(request: Request, session: SessionDep, user_id: int):
    user = session.exec(select(User).where(User.id == user_id)).first()
    return templates.TemplateResponse("users/add.html", {"request": request, "user": user})

@router.post("/{user_id}/edit")
def update_user(session: SessionDep, user_id: int, name: str = Form(...)):
    user = session.get(User, user_id)
    if user:
        user.name = name
        session.add(user)
        session.commit()
    return RedirectResponse(url="/users/", status_code=302)

@router.post("/{user_id}/delete")
def delete_user(session: SessionDep, user_id: int):
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
    return RedirectResponse(url="/users/", status_code=302)
