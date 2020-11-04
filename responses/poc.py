#%%
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, Feed, FeedTypes, Parent, Baby

engine = create_engine("postgresql://flatiron:flatiron@localhost:6432/data", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

#%%
father = Parent(email="j1@.com", name="j1")
session.add(father)

baby = Baby(birth_date=datetime.utcnow(), name="b1", father=father)
session.add(baby)
session.commit()


#%%
b1 = session.query(Baby).filter((Baby.father == father) | (Baby.mother == father)).one()

#%%
baby = session.query(Baby).filter_by(name="b1").one()
feed = Feed(baby=baby, type=FeedTypes.FORMULA)
session.add(feed)
session.commit()