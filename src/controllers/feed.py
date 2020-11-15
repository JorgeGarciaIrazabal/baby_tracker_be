from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import desc

from src.app import app, get_db
from src.models import Feed, PFeed

from sqlalchemy.orm import Session


@app.get("/baby/{baby_id}/feed", response_model=List[PFeed], tags=["api"])
def get_baby_feeds(
    baby_id: int,
    start_at: Optional[datetime] = None,
    end_at: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    current_filter = Feed.baby_id == baby_id
    if start_at is not None:
        current_filter &= Feed.start_at >= start_at
    if end_at is not None:
        current_filter &= Feed.end_at <= end_at
    feeds = db.query(Feed).order_by(desc(Feed.start_at)).filter(current_filter).all()
    return [PFeed.from_orm(feed) for feed in feeds]


@app.post("/feed", response_model=PFeed, tags=["api"])
def create_feed(p_feed: PFeed, db: Session = Depends(get_db)):
    feed = Feed(**p_feed.dict())
    db.add(feed)
    db.commit()
    return PFeed.from_orm(feed)


@app.put("/feed", response_model=PFeed, tags=["api"])
def update_feed(p_feed: PFeed, db: Session = Depends(get_db)):
    feed: Feed = db.query(Feed).get(p_feed.id)
    feed.update(p_feed)
    db.add(feed)
    db.commit()
    return PFeed.from_orm(feed)


@app.delete("/feed/{id}", response_model=PFeed, tags=["api"])
def delete_feed(id: int, db: Session = Depends(get_db)):
    feed: Feed = db.query(Feed).get(id)
    db.delete(feed)
    db.commit()
    return PFeed.from_orm(feed)
