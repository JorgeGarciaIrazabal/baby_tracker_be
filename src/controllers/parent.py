from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Baby, PBaby, PParent, Parent


@app.get("/parent", response_model=List[PParent], tags=["api"])
def get_parents(db: Session = Depends(get_db)):
    parents = db.query(Parent).all()
    pydantic_parents = [PParent.from_orm(parent) for parent in parents]
    return pydantic_parents


@app.get("/parent/{id}", response_model=PParent, tags=["api"])
def get_parent(id: int, db: Session = Depends(get_db)):
    parent = db.query(Parent).get(id)
    return PParent.from_orm(parent)


@app.post("/parent", response_model=PParent, tags=["api"])
def create_parent(pydantic_parent: PParent, db: Session = Depends(get_db)):
    parent = Parent(**pydantic_parent.dict())
    db.add(parent)
    db.commit()
    return PParent.from_orm(parent)


@app.get("/baby/parent/{id}", response_model=PBaby, tags=["api"])
def get_parents_baby(id: int, db: Session = Depends(get_db)):
    baby = db.query(Baby).filter((Baby.father_id == id) | (Baby.mother_id == id)).one()
    return PBaby.from_orm(baby)


@app.put("/baby/{baby_id}/parent/{parent_id}", response_model=PBaby, tags=["api"])
def remove_parents_baby(baby_id: int, parent_id: int, db: Session = Depends(get_db)):
    baby = db.query(Baby).get(baby_id).one()
    if baby.father_id == parent_id:
        baby.father_id = None

    if baby.mother_id == parent_id:
        baby.mother_id = None
    db.add(baby)
    db.commit()
    return PBaby.from_orm(baby)
