from typing import List, Optional

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Poop, PPoop
from src.services.auth import validate_baby_relationship


@app.get("/baby/{baby_id}/poop", response_model=List[PPoop], tags=["api"])
def get_baby_poops(
        baby_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        db: Session = Depends(get_db),
        auth: AuthJWT = Depends(),
):
    validate_baby_relationship(auth, baby_id)
    current_filter = Poop.baby_id == baby_id

    if page_size is not None:
        page = page or 0
    if page is not None:
        page_size = page_size or 30

    poops_query = db.query(Poop).order_by(desc(Poop.at)).filter(current_filter)
    if page is not None:
        poops = poops_query[page * page_size: (page * page_size) + page_size]
    else:
        poops = poops_query.all()
    return [PPoop.from_orm(poop) for poop in poops]


@app.post("/poop", response_model=PPoop, tags=["api"])
def create_poop(
        p_poop: PPoop, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    validate_baby_relationship(auth, p_poop.baby_id)

    poop = Poop(**p_poop.dict())
    db.add(poop)
    db.commit()
    return PPoop.from_orm(poop)


@app.put("/poop", response_model=PPoop, tags=["api"])
def update_poop(
        p_poop: PPoop, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    validate_baby_relationship(auth, p_poop.baby_id)
    poop: Poop = db.query(Poop).get(p_poop.id)
    poop.update(p_poop)
    db.add(poop)
    db.commit()
    return PPoop.from_orm(poop)


@app.delete("/poop/{id}", response_model=PPoop, tags=["api"])
def delete_poop(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    poop: Poop = db.query(Poop).get(id)
    validate_baby_relationship(auth, poop.baby_id)

    db.delete(poop)
    db.commit()
    return PPoop.from_orm(poop)
