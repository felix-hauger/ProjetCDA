from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shortener.db")
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session
