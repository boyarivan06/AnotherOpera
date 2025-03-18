import sqlalchemy as db
from sqlalchemy.orm import Session
from models import Base


engine = db.create_engine('sqlite:///data/data.db')
conn = engine.connect()

session = Session(bind=engine)

def build():
    Base.metadata.create_all(bind=engine)
