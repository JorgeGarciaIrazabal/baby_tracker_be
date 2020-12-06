from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Baby, PBaby, Parent
from src.services.auth import get_parent_from_token, validate_baby_relationship


def _validate_p_baby_with_parent(p_baby: PBaby, parent: Parent):
    if parent.id not in p_baby.parent_ids:
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED.value,
            detail="No relationship with baby",
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
    if new_parent.id not in baby.parent_ids:
        baby.parent_ids.append(new_parent.id)
    db.add(baby)
    db.commit()
    return PBaby.from_orm(baby)
