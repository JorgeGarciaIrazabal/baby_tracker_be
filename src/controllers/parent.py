from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Baby, PBaby, PParent
from src.services.auth import (
    get_parent_from_token,
    validate_baby_relationship,
)


@app.get(
    "/parent",
    response_model=PParent,
    response_model_exclude={"parent.password"},
    tags=["api"],
)
def get_parent(auth: AuthJWT = Depends()):
    parent = get_parent_from_token(auth)
    return PParent.from_orm(parent)


@app.get("/baby/parent/{id}", response_model=PBaby, tags=["api"])
def get_parents_baby(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    auth.jwt_required()
    baby = db.query(Baby).filter(Baby.parent_ids.contains([id])).one()
    validate_baby_relationship(auth, baby.id)
    return PBaby.from_orm(baby)


@app.put("/baby/{baby_id}/parent/{parent_id}", response_model=PBaby, tags=["api"])
def remove_parents_baby(
    baby_id: int,
    parent_id: int,
    db: Session = Depends(get_db),
    auth: AuthJWT = Depends(),
):
    validate_baby_relationship(auth, baby_id)

    baby = db.query(Baby).get(baby_id).one()
    baby.parent_ids.remove(parent_id)
    db.add(baby)
    db.commit()
    return PBaby.from_orm(baby)
