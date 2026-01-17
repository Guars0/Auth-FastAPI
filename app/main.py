from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="Aplicación de autenticación basica")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok"}