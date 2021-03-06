import sys
from copy import deepcopy

from clay import config

from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL

import redis
from clay import config


meta = config.get('database')

url_meta = deepcopy(meta)
del url_meta['database']
url = URL(**url_meta)
engine = create_engine(url)


def flush_redis():
    port = config.get('redis.port')
    host = config.get('redis.host')
    db = config.get('redis.db')

    _redis = redis.StrictRedis(host=host, port=port, db=db)
    _redis.flushall()


def create_db():
    conn = None
    try:
        conn = engine.connect()
        
        conn.execute('CREATE DATABASE IF NOT EXISTS ' + config.get('database.database'))
    finally:
        if conn:
            conn.close()


def drop_db():
    conn = None
    try:
        conn = engine.connect()
        conn.execute('DROP DATABASE IF EXISTS ' + config.get('database.database'))
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
        if not len(sys.argv) == 2:
            print 'Usage: python database.py [create|drop]'
        else:
            command = sys.argv[1]

            if command == 'create':
                create_db()
            elif command == 'drop':
                drop_db()
            elif command == 'flush_redis':
                flush_redis()
            else:
                print 'Usage: python database.py [create|drop]'
