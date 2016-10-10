from clay import config
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

meta = config.get('database')
url = URL(**meta)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
