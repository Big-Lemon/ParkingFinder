import redis
from clay import config

port = config.get('redis.port')
host = config.get('redis.host')
db = config.get('redis.db')

redis_pool = redis.ConnectionPool(host=host, port=port, db=db)
