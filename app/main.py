from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from .database import engine, get_session
from .models import SQLModel, Link
from .schemas import LinkCreate, LinkOut
from .crud import create_link
import datetime

app = FastAPI(title="QuickPath")

@app.get("/")
async def root():
    return {"message": "Welcome to QuickPath, the URL shortener app!"}

# Crée toutes les tables au lancement (simple pour SQLite)
SQLModel.metadata.create_all(bind=engine)

@app.post("/links", response_model=LinkOut, status_code=status.HTTP_201_CREATED)
def shorten_link(payload: LinkCreate, session: Session = Depends(get_session)):
    link = create_link(session, str(payload.url), payload.expires_at)
    return {
        "slug": link.slug
    }
