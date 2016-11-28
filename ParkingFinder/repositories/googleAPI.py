import json
import requests

from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return
from tornado.httpclient import AsyncHTTPClient

class TranslateAddressService(object):

	@classmethod
	@coroutine
	def getAddressBylatlng(self,latitude=None,
						longitude=None):
		latitudestr = str(latitude)
		longitudestr = str(longitude)
		url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
		key = "AIzaSyDvDQyqF3He6ButhI_rapU9BTvMC5qXgpA"
		url += latitudestr+","+longitudestr+"&key="+key
		response = requests.get(url)
		json_data = json.loads(response.text)
		if len(json_data['results']) == 0:
			raise NoResultFound
		else:
			raise Return(json_data['results'][0]['formatted_address'])