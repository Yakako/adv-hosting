from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import User

web_router = APIRouter()


templates = Jinja2Templates(directory="app/web/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@web_router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "users": users
        }
    )