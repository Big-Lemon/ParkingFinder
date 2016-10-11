from clay import config
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

meta = config.get('database')
url = URL(**meta)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
