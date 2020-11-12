import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

static_path = Path(__file__).parent / "dist/static"
engine_url = os.environ.get("DATABASE_URL", "postgresql://flatiron:flatiron@localhost:6432/data")
engine = create_engine(engine_url)
app = FastAPI()
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
Session.configure(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
