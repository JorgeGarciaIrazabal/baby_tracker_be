import os
from enum import Enum
from typing import List, Optional
import jwt

import uvicorn
from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Baby, Base, Feed, Parent, PBaby, PParent

engine_url = os.environ.get("DATABASE_URL", "postgresql://flatiron:flatiron@localhost:6432/data")

engine = create_engine(engine_url)

Base.metadata.create_all(engine)

app = FastAPI()

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)


class INTENTS(Enum):
    FEED = "FEED"
    POOP = "POOP"
    PEE = "PEE"


@app.get("/parent", response_model=List[PParent])
def get_parents():
    session = Session()
    parents = session.query(Parent).all()
    pydantic_parents = [PParent.from_orm(parent) for parent in parents]

    return pydantic_parents


@app.get("/parent/{id}", response_model=PParent)
def get_parent(id: int):
    session = Session()
    parent = session.query(Parent).get(id)
    return PParent.from_orm(parent)


@app.post("/parent", response_model=PParent)
def create_parent(pydantic_parent: PParent):
    session = Session()
    parent = Parent(**pydantic_parent.dict())
    session.add(parent)
    session.commit()
    return PParent.from_orm(parent)


@app.post("/baby", response_model=PBaby)
def create_baby(pydantic_baby: PBaby):
    session = Session()
    baby = Baby(**pydantic_baby.dict())
    session.add(baby)
    session.commit()
    return PBaby.from_orm(baby)


@app.put("/baby/{id}", response_model=PBaby)
def update_baby(id: int, pydantic_baby: PBaby):
    session = Session()
    baby = session.query(Baby).get(id)
    return PBaby.from_orm(baby)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
async def google_action(request: Request):
    session = Session()
    g_request = await request.json()
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

    if intent_name == INTENTS.FEED.value():
        feed = Feed(baby=baby, end_at=None)
        session.add(feed)
        session.commit()

    message = f"{intent_query} recorded"
    return {
        "session": g_session,
        "prompt": {"override": True, "firstSimple": {"speech": message, "text": ""}},
    }


def get_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    # token =
    # "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwNWVmMjBjNDUxOTFlZmY2NGIyNWQzODBkNDZmZGU1NWFjMjI5ZDEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2MDQyOTQxMDMsImF1ZCI6IjY1NDM5NzcxNzMtcG83NmNibjVyNDV0aTBtYTRudGE0MXZqNjg2YnJtbmYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTE5NTIyMDg3NTc1NTc4NzA3ODgiLCJlbWFpbCI6ImpvcmdlLmdpcmF6YWJhbEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkpvcmdlIEdhcmPDrWEgSXJhesOhYmFsIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdqdFhFSmxxVGhjMngxNmtvb01nRl9nRmppV0J3S0k4Z0s3T3llS1hnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkpvcmdlIiwiZmFtaWx5X25hbWUiOiJHYXJjw61hIElyYXrDoWJhbCIsImlhdCI6MTYwNDI5NDQwMywiZXhwIjoxNjA0Mjk4MDAzLCJqdGkiOiJiZTYwM2Q0OTdmOGVjYTIzMmVhMWI0YmEzMDU1ZmUzZDJmNDUxOWEwIn0.HIePCJIEQqfKThip4wVVzCE2BrByO61A_KJXouKbYAD82q0l_h8dzQxKTkkeNl21t5ZeEQKrySQzSf38IPzglZnkujlJIVKiydp_VvXTYLPIsiyBMjPhjgT2tCYwsuxvHRznkmZhm9E1mDXXsRVehnrNfvkk49N5rsl6p8OBQomFhZ7wZusTvjvYzNwg1kkwVxcPhuApHZ8ZMDYPUjnMOnhQiUW5_vd2XJeXeihn2pU4n0YrxhVt8gP0nx32t4WJOebhyFC-lXaG7rcRMW-6hS-nafPMzTCEhCkG5g32pMAVp165kkk4ZoLm4A7E2tExkcosyMTq1Gp2bsP7Xw9JfA"
    # jwt.decode(token, SECRET, algorithms=["RS256"])

    uvicorn.run(app, host=get_ip(), port=9001, debug=True)
