import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.hmset("available_parking:6ELA725", {'plate': '6ELA725', 'latitude': 34.044729, 'longitude': -117.844213, 'expired_at':'2017-11-24 23:36:26.777'})
r.hmset("available_parking:6DAY434", {'plate': '6DAY434', 'latitude': 34.044742, 'longitude': -117.844310, 'expired_at':'2017-11-24 23:36:26.1222'})
r.geoadd("active_parking_coordinate:",  -117.844213, 34.044729, '6ELA725')
r.geoadd("active_parking_coordinate:", -117.844310, 34.044742,  '6DAY434')
