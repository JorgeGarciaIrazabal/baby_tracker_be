from typing import List, Optional

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Growth, PGrowth
from src.services.auth import validate_baby_relationship


@app.get("/baby/{baby_id}/growth", response_model=List[PGrowth], tags=["api"])
def get_baby_growths(
    baby_id: int,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    db: Session = Depends(get_db),
    auth: AuthJWT = Depends(),
):
    validate_baby_relationship(auth, baby_id)
    current_filter = Growth.baby_id == baby_id

    if page_size is not None:
        page = page or 0
    if page is not None:
        page_size = page_size or 30

    growths_query = db.query(Growth).order_by(desc(Growth.at)).filter(current_filter)
    if page is not None:
        growths = growths_query[page * page_size : (page * page_size) + page_size]
    else:
        growths = growths_query.all()
    return [PGrowth.from_orm(growth) for growth in growths]


@app.post("/growth", response_model=PGrowth, tags=["api"])
def create_growth(
    p_growth: PGrowth, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    validate_baby_relationship(auth, p_growth.baby_id)

    growth = Growth(**p_growth.dict())
    db.add(growth)
    db.commit()
    return PGrowth.from_orm(growth)


@app.put("/growth", response_model=PGrowth, tags=["api"])
def update_growth(
    p_growth: PGrowth, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    validate_baby_relationship(auth, p_growth.baby_id)
    growth: Growth = db.query(Growth).get(p_growth.id)
    growth.update(p_growth)
    db.add(growth)
    db.commit()
    return PGrowth.from_orm(growth)


@app.delete("/growth/{id}", response_model=PGrowth, tags=["api"])
def delete_growth(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    growth: Growth = db.query(Growth).get(id)
    validate_baby_relationship(auth, growth.baby_id)

    db.delete(growth)
    db.commit()
    return PGrowth.from_orm(growth)
