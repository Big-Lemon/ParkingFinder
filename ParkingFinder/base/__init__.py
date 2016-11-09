from clay import config
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session

meta = config.get('database')
url = URL(**meta)

engine = create_engine(url)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
