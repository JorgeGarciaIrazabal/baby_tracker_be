from datetime import datetime
from enum import Enum

import humanize
import jwt
from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.app import app, get_db
from src.models import Baby, Feed, FeedTypes, Parent, Poop

transfer_to_end_conversation = {
    "name": "ShowList",
    "slotFillingStatus": "UNSPECIFIED",
    "slots": {},
    "next": {"name": "actions.scene.END_CONVERSATION"},
}


class INTENTS(Enum):
    FEED = "FEED"
    FEED_END = "FEED_END"
    POOP = "POOP"
    PEE = "PEE"
    SLEEP = "SLEEP"
    SLEEP_END = "SLEEP_END"
    SHOW_LIST = "SHOW_LIST"
    CREATE_USERS = "create_users"


def _get_last_feeds(db: Session, baby: Baby):
    feeds = db.query(Feed).order_by(desc(Feed.start_at)).filter_by(baby=baby)[:4]

    rows = []
    for feed in feeds:
        end_at = ""
        amount = ""
        if feed.end_at is not None:
            end_at = humanize.precisedelta(
                feed.end_at - feed.start_at, minimum_unit="minutes", format="%0.0f"
            )
            amount = f"{feed.amount} ml"
        rows.append(
            dict(
                cells=[
                    dict(
                        text=humanize.precisedelta(
                            feed.start_at - datetime.utcnow(),
                            minimum_unit="minutes",
                            format="%0.0f",
                        )
                        + " ago",
                    ),
                    dict(text=end_at),
                    dict(text=amount),
                ]
            )
        )

    return dict(
        table=dict(
            columns=[
                dict(header="Started"),
                dict(header="Duration"),
                dict(header="Amount"),
            ],
            rows=rows,
            subtitle=f"last feedings for {baby.name}",
            title="Feedings",
        )
    )


def show_list(db: Session, g_request: dict, baby: Baby):
    g_session = build_g_session(g_request)
    last_feeds = _get_last_feeds(db=db, baby=baby)

    rows = last_feeds["table"]["rows"]
    return {
        "session": g_session,
        "prompt": {
            "override": True,
            "lastSimple": {
                "speech": f"Last feeding was {rows[0]['cells'][0]['text']}. \n"
                f"And the previous feeding was {rows[1]['cells'][0]['text']}",
                "text": f"Listing Feedings",
            },
            "content": last_feeds,
        },
        "scene": transfer_to_end_conversation,
    }


def feeding(db: Session, g_request: dict, baby: Baby):
    g_session = build_g_session(g_request)
    if db.query(Feed).filter_by(baby=baby, end_at=None).count() > 0:
        feed = db.query(Feed).filter_by(baby=baby, end_at=None).first()
        message = (
            f"Feeding already started "
            f"{humanize.naturaltime(feed.start_at, when=datetime.utcnow())}"
        )
        return {
            "session": g_session,
            "prompt": {
                "override": True,
                "firstSimple": {"speech": message, "text": message},
                "content": _get_last_feeds(db=db, baby=baby),
            },
        }
    feed = Feed(baby=baby, type=FeedTypes.FORMULA, amount=0)
    db.add(feed)
    db.commit()
    return {
        "session": g_session,
        "prompt": {
            "override": True,
            "firstSimple": {
                "speech": f"Starting feeding, yummy!",
                "text": f"Recorded feeding at {feed.start_at.strftime('%-I:%M %p')} for "
                f"{baby.name}",
            },
        },
        "scene": transfer_to_end_conversation,
    }


def build_g_session(g_request):
    g_session = {
        "id": g_request["session"]["id"],
        "params": g_request["session"]["params"],
        "languageCode": "",
    }
    return g_session


def feeding_end(db: Session, g_request: dict, baby: Baby):
    g_session = build_g_session(g_request)
    if db.query(Feed).filter_by(baby=baby, end_at=None).count() == 0:
        g_session["params"]["message_type"] = "NO_STARTING_FEEDING"
        g_session["params"]["milliliters"] = g_request["intent"]["params"][
            "milliliters"
        ]["resolved"]
        message = f"No feeding started."
        return {
            "session": g_session,
            "prompt": {
                "override": True,
                "firstSimple": {"speech": message, "text": message},
            },
        }
    feed = db.query(Feed).filter_by(baby=baby, end_at=None).one()
    feed.amount = g_request["intent"]["params"]["milliliters"]["resolved"]
    feed.end_at = datetime.utcnow()
    db.add(feed)
    db.commit()
    human_time = humanize.precisedelta(
        feed.end_at - feed.start_at,
        minimum_unit="minutes",
        format="%0.0f",
    )

    return {
        "session": g_session,
        "prompt": {
            "override": True,
            "firstSimple": {
                "speech": f"Finished recording feeding for {baby.name}, {feed.amount} ml",
                "text": f"Finished recording feeding for {human_time} on {baby.name}, "
                f"{feed.amount} ml",
            },
        },
        "scene": transfer_to_end_conversation,
    }


def pooping(db: Session, g_request: dict, baby: Baby):
    g_session = build_g_session(g_request)
    poop = Poop(baby=baby)
    db.add(poop)
    db.commit()
    return {
        "session": g_session,
        "prompt": {
            "override": True,
            "firstSimple": {
                "variants": [
                    {"speech": f"Poop recorded, did that feel good {baby.name}?",
                     "text": f"Pee Recorded",},
                    {"speech": f"Uhh stinky",
                     "text": f"Pee Recorded",},
                    {"speech": f"number 2 completed!!",
                     "text": f"Pee Recorded",},
                ],
            },
        },
        "scene": transfer_to_end_conversation,
    }


def peeing(db: Session, g_request: dict, baby: Baby):
    g_session = build_g_session(g_request)
    poop = Poop(baby=baby)
    db.add(poop)
    db.commit()
    return {
        "session": g_session,
        "prompt": {
            "override": True,
            "firstSimple": {
                "variants": [
                    {
                        "speech": f"{baby.name}, did you get your diaper wet? yes you did!!",
                        "text": f"Pee Recorded",
                    },
                    {
                        "speech": f"Diaper wet removed, are you dry now {baby.name}?",
                        "text": f"Pee Recorded",
                    },
                    {
                        "speech": f"number 1 completed!!",
                        "text": f"Pee Recorded",
                    },
                ],
            },
        },
        "scene": transfer_to_end_conversation,
    }


@app.post("/google", include_in_schema=False)
async def google_action(request: Request, db: Session = Depends(get_db)):
    g_request = await request.json()
    print(g_request)
    g_session = {"id": g_request["session"]["id"], "params": {}, "languageCode": ""}
    intent_query = g_request["intent"]["query"]
    intent_name = g_request["handler"]["name"]

    if intent_name == INTENTS.CREATE_USERS.value:
        return {
            "session": g_session,
            "prompt": {
                "override": False,
            },
        }

    if "authorization" in request.headers:
        user = jwt.decode(
            request.headers["authorization"], verify=False, algorithms=["RS256"]
        )
        parent = db.query(Parent).filter_by(email=user["email"]).one()
        baby = db.query(Baby).filter(Baby.parent_ids.contains([parent.id])).one()
    else:
        message = "You need to be authorized to track baby"
        return {
            "session": g_session,
            "prompt": {
                "override": True,
                "firstSimple": {"speech": message, "text": message},
            },
        }

    if intent_name == INTENTS.FEED.value:
        return feeding(db, g_request, baby)

    if intent_name == INTENTS.FEED_END.value:
        return feeding_end(db, g_request, baby)

    if intent_name == INTENTS.SHOW_LIST.value:
        return show_list(db, g_request, baby)

    if intent_name == INTENTS.POOP.value:
        return pooping(db, g_request, baby)

    if intent_name == INTENTS.PEE.value:
        return peeing(db, g_request, baby)

    message = f"{intent_query} recorded"
    return {
        "session": g_session,
        "prompt": {
            "override": True,
            "firstSimple": {"speech": message, "text": message},
        },
    }
