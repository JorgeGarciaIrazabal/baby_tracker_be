from fastapi import Depends
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Baby, PBaby, Parent


@app.post("/baby", response_model=PBaby, tags=["api"])
def create_baby(pydantic_baby: PBaby, db: Session = Depends(get_db)):
    baby = Baby(**pydantic_baby.dict())
    db.add(baby)
    db.commit()
    return PBaby.from_orm(baby)


@app.put("/baby/{id}", response_model=PBaby, tags=["api"])
def update_baby(id: int, pydantic_baby: PBaby, db: Session = Depends(get_db)):
    baby = db.query(Baby).get(id)
    return PBaby.from_orm(baby)


@app.put("/baby/{id}/new_parent", response_model=PBaby, tags=["api"])
def new_parent_for_baby(id: int, new_parent_email: str, db: Session = Depends(get_db)):
    baby: Baby = db.query(Baby).get(id)
    new_parent = db.query(Parent).filter_by(email=new_parent_email).one()
    if baby.father_id is None:
        baby.father = new_parent
    if baby.mother_id is None:
        baby.mother = new_parent
    db.add(baby)
    db.commit()
    return PBaby.from_orm(baby)
