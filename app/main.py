from fastapi import FastAPI

from app.api.router import api_router

from app.db.database import engine, Base
from app.db import models

app = FastAPI(title="Rastad AI Assistant")

Base.metadata.create_all(bind=engine)

app.include_router(api_router)
