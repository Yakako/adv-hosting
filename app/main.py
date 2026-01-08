from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database.db import engine
from app.database.models import Base
from app.api.routes import api_router
from app.web.routes import web_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI with Database")

app.include_router(api_router, prefix="/api")

# Web UI routes
app.include_router(web_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")