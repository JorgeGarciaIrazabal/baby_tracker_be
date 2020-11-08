import enum
from datetime import datetime

from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class FeedTypes(enum.Enum):
    FORMULA = 1
    BREAST_MILK_BOTTLE = 2
    RIGHT_BREAST = 3
    LEFT_BREAST = 4
    SOLID = 5


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
    father_id = Column(Integer, ForeignKey("parents.id"))
    mother_id = Column(Integer, ForeignKey("parents.id"))
    father = relationship("Parent", foreign_keys=[father_id])
    mother = relationship("Parent", foreign_keys=[mother_id])


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


PParent = sqlalchemy_to_pydantic(Parent)
PBaby = sqlalchemy_to_pydantic(Baby)
PFeed = sqlalchemy_to_pydantic(Feed)
PPee = sqlalchemy_to_pydantic(Pee)
PPoop = sqlalchemy_to_pydantic(Poop)
