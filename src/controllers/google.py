from datetime import datetime
from enum import Enum

import jwt
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.app import app, get_db
from src.models import Baby, Feed, FeedTypes, Parent


@app.post("/", include_in_schema=False)
async def google_action(request: Request, db: Session = Depends(get_db)):
    g_request = await request.json()
    print(g_request)
    g_session = {"id": g_request["session"]["id"], "params": {}, "languageCode": ""}
    intent_query = g_request["intent"]["query"]
    intent_name = g_request["intent"]["name"]

    if "authorization" in request.headers:
        user = jwt.decode(request.headers["authorization"], verify=False, algorithms=["RS256"])
        parent = db.query(Parent).filter_by(email=user["email"]).one()
        baby = db.query(Baby).filter((Baby.father == parent) | (Baby.mother == parent)).one()
    else:
        message = "You need to be authorized to track baby"
        return {
            "session": g_session,
            "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
        }

    if intent_name == INTENTS.FEED.value:
        if db.query(Feed).filter_by(baby=baby, end_at=None).count() > 0:
            feed = db.query(Feed).filter_by(baby=baby, end_at=None).first()
            message = f"Feeding did already started at {feed.start_at}"
            return {
                "session": g_session,
                "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
            }
        feed = Feed(baby=baby, type=FeedTypes.FORMULA)
        db.add(feed)
        db.commit()

    if intent_name == INTENTS.FEED_END.value:
        if db.query(Feed).filter_by(baby=baby, end_at=None).count() == 0:
            message = f"No feeding started"
            return {
                "session": g_session,
                "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
            }
        feed = db.query(Feed).filter_by(baby=baby, end_at=None).one()
        feed.amount = g_request["intent"]["params"]["milliliters"]["resolved"]
        feed.end_at = datetime.utcnow()
        db.add(feed)
        db.commit()

    message = f"{intent_query} recorded"
    return {
        "session": g_session,
        "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
    }


class INTENTS(Enum):
    FEED = "FEED"
    FEED_END = "FEED_END"
    POOP = "POOP"
    PEE = "PEE"