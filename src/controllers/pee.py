from typing import List, Optional

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Pee, PPee
from src.services.auth import validate_baby_relationship


@app.get("/baby/{baby_id}/pee", response_model=List[PPee], tags=["api"])
def get_baby_pees(
        baby_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        db: Session = Depends(get_db),
        auth: AuthJWT = Depends(),
):
    validate_baby_relationship(auth, baby_id)
    current_filter = Pee.baby_id == baby_id

    if page_size is not None:
        page = page or 0
    if page is not None:
        page_size = page_size or 30

    pees_query = db.query(Pee).order_by(desc(Pee.at)).filter(current_filter)
    if page is not None:
        pees = pees_query[page * page_size: (page * page_size) + page_size]
    else:
        pees = pees_query.all()
    return [PPee.from_orm(pee) for pee in pees]


@app.post("/pee", response_model=PPee, tags=["api"])
def create_pee(
        p_pee: PPee, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    validate_baby_relationship(auth, p_pee.baby_id)

    pee = Pee(**p_pee.dict())
    db.add(pee)
    db.commit()
    return PPee.from_orm(pee)


@app.put("/pee", response_model=PPee, tags=["api"])
def update_pee(
        p_pee: PPee, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    validate_baby_relationship(auth, p_pee.baby_id)
    pee: Pee = db.query(Pee).get(p_pee.id)
    pee.update(p_pee)
    db.add(pee)
    db.commit()
    return PPee.from_orm(pee)


@app.delete("/pee/{id}", response_model=PPee, tags=["api"])
def delete_pee(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    pee: Pee = db.query(Pee).get(id)
    validate_baby_relationship(auth, pee.baby_id)

    db.delete(pee)
    db.commit()
    return PPee.from_orm(pee)
