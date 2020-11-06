import json
from datetime import datetime
import os
from enum import Enum
from typing import List, Optional
import jwt

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from starlette.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from src.models import Baby, Base, Feed, FeedTypes, PFeed, Parent, PBaby, PParent

engine_url = os.environ.get("DATABASE_URL", "postgresql://flatiron:flatiron@localhost:6432/data")

engine = create_engine(engine_url)

Base.metadata.create_all(engine)

app = FastAPI()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)


class INTENTS(Enum):
    FEED = "FEED"
    FEED_END = "FEED_END"
    POOP = "POOP"
    PEE = "PEE"


@app.get("/parent", response_model=List[PParent], tags=["api"])
def get_parents():
    session = Session()
    parents = session.query(Parent).all()
    pydantic_parents = [PParent.from_orm(parent) for parent in parents]

    return pydantic_parents


@app.get("/parent/{id}", response_model=PParent, tags=["api"])
def get_parent(id: int):
    session = Session()
    parent = session.query(Parent).get(id)
    return PParent.from_orm(parent)


@app.post("/parent", response_model=PParent, tags=["api"])
def create_parent(pydantic_parent: PParent):
    session = Session()
    parent = Parent(**pydantic_parent.dict())
    session.add(parent)
    session.commit()
    return PParent.from_orm(parent)


@app.post("/baby", response_model=PBaby, tags=["api"])
def create_baby(pydantic_baby: PBaby):
    session = Session()
    baby = Baby(**pydantic_baby.dict())
    session.add(baby)
    session.commit()
    return PBaby.from_orm(baby)


@app.put("/baby/{id}", response_model=PBaby, tags=["api"])
def update_baby(id: int, pydantic_baby: PBaby):
    session = Session()
    baby = session.query(Baby).get(id)
    return PBaby.from_orm(baby)


@app.get("/baby/parent/{id}", response_model=PBaby, tags=["api"])
def get_parents_baby(id: int):
    session = Session()
    baby = session.query(Baby).filter((Baby.father_id == id) | (Baby.mother_id == id)).one()
    return PBaby.from_orm(baby)


@app.put("/baby/{baby_id}/parent/{parent_id}", response_model=PBaby, tags=["api"])
def remove_parents_baby(baby_id: int, parent_id: int):
    session = Session()
    baby = session.query(Baby).get(baby_id).one()
    if baby.father_id == parent_id:
         baby.father_id = None

    if baby.mother_id == parent_id:
        baby.mother_id = None
    session.add(baby)
    session.commit()
    return PBaby.from_orm(baby)


@app.get("/baby/{baby_id}/feeds", response_model=List[PFeed], tags=["api"])
def get_baby_feeds(baby_id: int):
    session = Session()
    feeds = session.query(Feed).order_by(desc(Feed.start_at)).filter_by(baby_id=baby_id).all()
    return [PFeed.from_orm(feed) for feed in feeds]


@app.put("/sign_in", response_model=PParent, tags=["api"])
def sign_in(email: str, password: str):
    session = Session()
    parent = session.query(Parent).filter_by(email=email, password=password).one()
    return PParent.from_orm(parent)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():
    with open("/home/jirazabal/code/baby_tracker_be/src/dist/static/index.html") as f:
        return f.read()


@app.post("/", include_in_schema=False)
async def google_action(request: Request):
    session = Session()
    g_request = await request.json()
    print(g_request)
    g_session = {"id": g_request["session"]["id"], "params": {}, "languageCode": ""}
    intent_query = g_request["intent"]["query"]
    intent_name = g_request["intent"]["name"]

    if "authorization" in request.headers:
        user = jwt.decode(request.headers["authorization"], verify=False, algorithms=["RS256"])
        parent = session.query(Parent).filter_by(email=user["email"]).one()
        baby = session.query(Baby).filter((Baby.father == parent) | (Baby.mother == parent)).one()
    else:
        message = "You need to be authorized to track baby"
        return {
            "session": g_session,
            "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
        }

    if intent_name == INTENTS.FEED.value:
        if session.query(Feed).filter_by(baby=baby, end_at=None).count() > 0:
            feed = session.query(Feed).filter_by(baby=baby, end_at=None).first()
            message = f"Feeding did already started at {feed.start_at}"
            return {
                "session": g_session,
                "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
            }
        feed = Feed(baby=baby, type=FeedTypes.FORMULA)
        session.add(feed)
        session.commit()

    if intent_name == INTENTS.FEED_END.value:
        if session.query(Feed).filter_by(baby=baby, end_at=None).count() == 0:
            message = f"No feeding started"
            return {
                "session": g_session,
                "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
            }
        feed = session.query(Feed).filter_by(baby=baby, end_at=None).one()
        feed.amount = g_request["intent"]["params"]["milliliters"]["resolved"]
        feed.end_at = datetime.utcnow()
        session.add(feed)
        session.commit()

    message = f"{intent_query} recorded"
    return {
        "session": g_session,
        "prompt": {"override": True, "firstSimple": {"speech": message, "text": message}},
    }


def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


app.mount("/", StaticFiles(directory="dist/static"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # token =
    # "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwNWVmMjBjNDUxOTFlZmY2NGIyNWQzODBkNDZmZGU1NWFjMjI5ZDEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2MDQyOTQxMDMsImF1ZCI6IjY1NDM5NzcxNzMtcG83NmNibjVyNDV0aTBtYTRudGE0MXZqNjg2YnJtbmYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTE5NTIyMDg3NTc1NTc4NzA3ODgiLCJlbWFpbCI6ImpvcmdlLmdpcmF6YWJhbEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkpvcmdlIEdhcmPDrWEgSXJhesOhYmFsIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdqdFhFSmxxVGhjMngxNmtvb01nRl9nRmppV0J3S0k4Z0s3T3llS1hnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkpvcmdlIiwiZmFtaWx5X25hbWUiOiJHYXJjw61hIElyYXrDoWJhbCIsImlhdCI6MTYwNDI5NDQwMywiZXhwIjoxNjA0Mjk4MDAzLCJqdGkiOiJiZTYwM2Q0OTdmOGVjYTIzMmVhMWI0YmEzMDU1ZmUzZDJmNDUxOWEwIn0.HIePCJIEQqfKThip4wVVzCE2BrByO61A_KJXouKbYAD82q0l_h8dzQxKTkkeNl21t5ZeEQKrySQzSf38IPzglZnkujlJIVKiydp_VvXTYLPIsiyBMjPhjgT2tCYwsuxvHRznkmZhm9E1mDXXsRVehnrNfvkk49N5rsl6p8OBQomFhZ7wZusTvjvYzNwg1kkwVxcPhuApHZ8ZMDYPUjnMOnhQiUW5_vd2XJeXeihn2pU4n0YrxhVt8gP0nx32t4WJOebhyFC-lXaG7rcRMW-6hS-nafPMzTCEhCkG5g32pMAVp165kkk4ZoLm4A7E2tExkcosyMTq1Gp2bsP7Xw9JfA"
    # jwt.decode(token, SECRET, algorithms=["RS256"])
    with(Path(__file__).parent / "openapi.json").open(mode="w") as f:
        json.dump(app.openapi(), f)
    uvicorn.run(app, host="0.0.0.0", port=9001, debug=True)
