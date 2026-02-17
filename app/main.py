from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.routers import auth

app = FastAPI(title="Aplicación de autenticación basica")
app.include_router(auth.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok"}