from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Baby, PBaby, Parent
from src.services.auth import get_parent_from_token, validate_baby_relationship


def _validate_p_baby_with_parent(p_baby, parent):
    if p_baby.father_id != parent.id and p_baby.mother_id != parent.id:
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED.value,
            detail="No relationship with baby",
        )
    if p_baby.father_id is not None and p_baby.mother_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED.value,
            detail="Baby can only be created with one parent",
        )


@app.post("/baby", response_model=PBaby, tags=["api"])
def create_baby(
    p_baby: PBaby, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    parent = get_parent_from_token(auth)
    _validate_p_baby_with_parent(p_baby, parent)

    baby = Baby(**p_baby.dict())
    db.add(baby)
    db.commit()
    return PBaby.from_orm(baby)


@app.put("/baby/{id}", response_model=PBaby, tags=["api"])
def update_baby(
    id: int,
    p_baby: PBaby,
    db: Session = Depends(get_db),
    auth: AuthJWT = Depends(),
):
    parent = get_parent_from_token(auth)
    validate_baby_relationship(auth, id)

    baby: Baby = db.query(Baby).get(id)
    _validate_p_baby_with_parent(p_baby, parent)
    baby.update(p_baby)
    return PBaby.from_orm(baby)


@app.put("/baby/{id}/new_parent", response_model=PBaby, tags=["api"])
def new_parent_for_baby(
    id: int,
    new_parent_email: str,
    db: Session = Depends(get_db),
    auth: AuthJWT = Depends(),
):
    baby: Baby = db.query(Baby).get(id)
    validate_baby_relationship(auth, id)

    new_parent = db.query(Parent).filter_by(email=new_parent_email).one()
    if baby.father_id is None:
        baby.father = new_parent
    if baby.mother_id is None:
        baby.mother = new_parent
    db.add(baby)
    db.commit()
    return PBaby.from_orm(baby)
