import enum
from datetime import datetime, timezone

from pydantic import BaseConfig, BaseModel
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import relationship

from src.services.sqlalchemy_pydantic import sqlalchemy_to_pydantic

Base = declarative_base()


class FeedTypes(enum.Enum):
    FORMULA = 1
    BREAST_MILK_BOTTLE = 2
    RIGHT_BREAST = 3
    LEFT_BREAST = 4
    SOLID = 5


class GrowthTypes(enum.Enum):
    HEIGHT = "HEIGHT"
    HEAD = "HEAD"
    WEIGHT = "WEIGHT"


class MutableList(Mutable, list):

    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        list.__delitem__(self, key)
        self.changed()

    def append(self, value):
        list.append(self, value)
        self.changed()

    def pop(self, index=0):
        value = list.pop(self, index)
        self.changed()
        return value

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value


class BTMixin:
    def update(self, model: BaseModel):
        kwargs = model.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Parent(BTMixin, Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True, nullable=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Baby(BTMixin, Base):
    __tablename__ = "babies"
    id = Column(Integer, primary_key=True, nullable=True)
    birth_date = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    parent_ids = Column(MutableList.as_mutable(ARRAY(Integer)), default=dict)


class Feed(BTMixin, Base):
    __tablename__ = "feeds"
    id = Column(Integer, primary_key=True, nullable=True)
    start_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_at = Column(DateTime, nullable=True)
    amount = Column(Integer)
    type = Column(Enum(FeedTypes), nullable=False)
    baby_id = Column(Integer, ForeignKey("babies.id"))
    baby = relationship("Baby", foreign_keys=[baby_id])


class Pee(BTMixin, Base):
    __tablename__ = "pees"
    id = Column(Integer, primary_key=True, nullable=True)
    at = Column(DateTime, nullable=False, default=datetime.utcnow)
    baby_id = Column(Integer, ForeignKey("babies.id"))
    baby = relationship("Baby", foreign_keys=[baby_id])


class Poop(BTMixin, Base):
    __tablename__ = "poops"
    id = Column(Integer, primary_key=True, nullable=True)
    at = Column(DateTime, nullable=False, default=datetime.utcnow)
    baby_id = Column(Integer, ForeignKey("babies.id"))
    baby = relationship("Baby", foreign_keys=[baby_id])


class Growth(BTMixin, Base):
    __tablename__ = "growths"
    id = Column(Integer, primary_key=True, nullable=True)
    at = Column(DateTime, nullable=False, default=datetime.utcnow)
    baby_id = Column(Integer, ForeignKey("babies.id"))
    baby = relationship("Baby", foreign_keys=[baby_id])
    type = Column(Enum(GrowthTypes), nullable=False)
    measure = Column(Integer)


class Sleep(BTMixin, Base):
    __tablename__ = "sleeps"
    id = Column(Integer, primary_key=True, nullable=True)
    start_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_at = Column(DateTime, nullable=True)
    baby_id = Column(Integer, ForeignKey("babies.id"))
    baby = relationship("Baby", foreign_keys=[baby_id])


class PConfig(BaseConfig):
    orm_mode = True
    json_encoders = {
        datetime: lambda d: d.replace(tzinfo=timezone.utc).isoformat()
    }


PBaby = sqlalchemy_to_pydantic(Baby, config=PConfig)
PParent = sqlalchemy_to_pydantic(Parent, config=PConfig)
PFeed = sqlalchemy_to_pydantic(Feed, config=PConfig)
PPee = sqlalchemy_to_pydantic(Pee, config=PConfig)
PPoop = sqlalchemy_to_pydantic(Poop, config=PConfig)
PGrowth = sqlalchemy_to_pydantic(Growth, config=PConfig)
PSleep = sqlalchemy_to_pydantic(Sleep, config=PConfig)


class ParentWithToken(BaseModel):
    parent: PParent
    token: str
