from fastapi import Depends
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import PParent, Parent


@app.put("/sign_in", response_model=PParent, tags=["api"])
def sign_in(email: str, password: str, db: Session = Depends(get_db)):
    parent = db.query(Parent).filter_by(email=email, password=password).one()
    return PParent.from_orm(parent)
