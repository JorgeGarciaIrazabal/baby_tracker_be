from datetime import datetime
from enum import Enum

import humanize
import jwt
from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.app import app, get_db
from src.models import Baby, Feed, FeedTypes, Parent


class INTENTS(Enum):
    FEED = "FEED"
    FEED_END = "FEED_END"
    POOP = "POOP"
    PEE = "PEE"
    SHOW_LIST = "SHOW_LIST"


def show_list(db: Session, g_request: dict, baby: Baby):
    g_session = {"id": g_request["session"]["id"], "params": g_request["session"]["params"],
                 "languageCode": ""
                 }
    if db.query(Feed).filter_by(baby=baby, end_at=None).count() > 0:
        feed = db.query(Feed).filter_by(baby=baby, end_at=None).first()
        message = f"Feeding did already started at {feed.start_at}"
        return {
            "session": g_session,
            "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
        }
    feed = Feed(baby=baby, type=FeedTypes.FORMULA, amount=0)
    db.add(feed)
    db.commit()
    return {
        "session": g_session,
        "prompt": {
            "override": True, "firstSimple": {
                "speech": f"Recoded feeding",
                "text": f"Recoded feeding at {feed.start_at.strftime('%-I:%M %p')} for {baby.name}",
            }
        },
    }


def feeding(db: Session, g_request: dict, baby: Baby):
    g_session = {"id": g_request["session"]["id"], "params": g_request["session"]["params"],
                 "languageCode": ""
                 }
    if db.query(Feed).filter_by(baby=baby, end_at=None).count() > 0:
        feed = db.query(Feed).filter_by(baby=baby, end_at=None).first()
        message = f"Feeding did already started at {feed.start_at}"
        return {
            "session": g_session,
            "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
        }
    feed = Feed(baby=baby, type=FeedTypes.FORMULA, amount=0)
    feeds = db.query(Feed).order_by(desc(Feed.start_at)).filter_by(baby_id=baby.id)[:4]
    db.add(feed)
    db.commit()
    return {
        "session": g_session,
        "prompt": {
            "override": True,
            "firstSimple": {
                "speech": f"Recoded feeding",
                "text": f"Recoded feeding at {feed.start_at.strftime('%-I:%M %p')} for {baby.name}",
            }
        },
    }


def feeding_end(db: Session, g_request: dict, baby: Baby):
    g_session = {"id": g_request["session"]["id"], "params": {}, "languageCode": ""}
    if db.query(Feed).filter_by(baby=baby, end_at=None).count() == 0:
        g_session["params"]["message_type"] = "NO_STARTING_FEEDING"
        g_session["params"]["milliliters"] = g_request["intent"]["params"]["milliliters"][
            "resolved"]
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
    human_time = humanize.precisedelta(feed.end_at - feed.start_at, minimum_unit="minutes")

    return {
        "session": g_session,
        "prompt": {
            "override": True,
            "firstSimple": {
                "speech": f"Finished recoding feeding",
                "text": f"Finished recording feeding for {human_time} on {baby.name} "
            }
        },
    }


@app.post("/", include_in_schema=False)
async def google_action(request: Request, db: Session = Depends(get_db)):
    g_request = await request.json()
    print(g_request)
    g_session = {"id": g_request["session"]["id"], "params": {}, "languageCode": ""}
    intent_query = g_request["intent"]["query"]
    intent_name = g_request["handler"]["name"]

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
        return feeding(db, g_request, baby)

    if intent_name == INTENTS.FEED_END.value:
        return feeding_end(db, g_request, baby)

    message = f"{intent_query} recorded"
    return {
        "session": g_session,
        "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
    }
