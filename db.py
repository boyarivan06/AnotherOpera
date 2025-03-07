import sqlalchemy as db
from sqlalchemy.orm import Session

engine = db.create_engine('sqlite:///data/data.db')
conn = engine.connect()

from models.sqlalch_models import Base


Base.metadata.create_all(bind=engine)
session = Session(bind=engine)