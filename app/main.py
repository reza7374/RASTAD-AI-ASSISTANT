from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import router
from app.db.database import engine, Base 
from app.db import models


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)



@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "database": "disconnected",
            "details": str(e),
        }
