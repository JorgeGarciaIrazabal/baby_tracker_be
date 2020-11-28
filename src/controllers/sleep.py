from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.app import app, get_db
from src.models import Sleep, PSleep
from src.services.auth import validate_baby_relationship


@app.get("/baby/{baby_id}/sleep", response_model=List[PSleep], tags=["api"])
def get_baby_sleeps(
        baby_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
        db: Session = Depends(get_db),
        auth: AuthJWT = Depends(),
):
    validate_baby_relationship(auth, baby_id)

    current_filter = Sleep.baby_id == baby_id
    if start_at is not None:
        current_filter &= Sleep.start_at >= start_at
    if end_at is not None:
        current_filter &= Sleep.end_at <= end_at
    if page_size is not None:
        page = page or 0
    if page is not None:
        page_size = page_size or 30

    sleeps_query = db.query(Sleep).order_by(desc(Sleep.start_at)).filter(current_filter)
    if page is not None:
        sleeps = sleeps_query[page * page_size : (page * page_size) + page_size]
    else:
        sleeps = sleeps_query.all()
    return [PSleep.from_orm(sleep) for sleep in sleeps]


@app.post("/sleep", response_model=PSleep, tags=["api"])
def create_sleep(
        p_sleep: PSleep, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    validate_baby_relationship(auth, p_sleep.baby_id)

    sleep = Sleep(**p_sleep.dict())
    db.add(sleep)
    db.commit()
    return PSleep.from_orm(sleep)


@app.put("/sleep", response_model=PSleep, tags=["api"])
def update_sleep(
        p_sleep: PSleep, db: Session = Depends(get_db), auth: AuthJWT = Depends()
):
    validate_baby_relationship(auth, p_sleep.baby_id)
    sleep: Sleep = db.query(Sleep).get(p_sleep.id)
    sleep.update(p_sleep)
    db.add(sleep)
    db.commit()
    return PSleep.from_orm(sleep)


@app.delete("/sleep/{id}", response_model=PSleep, tags=["api"])
def delete_sleep(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    sleep: Sleep = db.query(Sleep).get(id)
    validate_baby_relationship(auth, sleep.baby_id)

    db.delete(sleep)
    db.commit()
    return PSleep.from_orm(sleep)
