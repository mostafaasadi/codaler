import logging
import sqlalchemy
from sys import exit
from models import Audite
from sqlalchemy.orm import sessionmaker

try:
    db_engine = sqlalchemy.create_engine('sqlite:///audites.db')
    Session = sessionmaker(bind=db_engine)
    Audite.metadata.create_all(db_engine)
except Exception as e:
    logging.error(e)
    exit(1)
