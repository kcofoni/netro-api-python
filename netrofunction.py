import requests

NETRO_BASE_URL = 'https://api.netrohome.com/npa/v1/'
NETRO_GET_SCHEDULES = 'schedules.json'
NETRO_GET_INFO = 'info.json'
NETRO_GET_MOISTURES = 'moistures.json'
NETRO_GET_SENSORDATA = 'sensor_data.json'
NETRO_POST_REPORTWEATHER = 'report_weather.json'
NETRO_POST_MOISTURE = 'set_moisture.json'
NETRO_POST_WATER = 'water.json'
NETRO_POST_STOPWATER = 'stop_water.json'
NETRO_POST_NOWATER = 'no_water.json'
NETRO_POST_STATUS = 'set_status.json'
NETRO_GET_EVENTS = 'events.json'

NETRO_STATUS_ENABLE = 1
NETRO_STATUS_DISABLE = 0
NETRO_STATUS_STANDBY = "STANDBY"
NETRO_STATUS_WATERING = "WATERING"
NETRO_SCHEDULE_EXECUTED = "EXECUTED"
NETRO_SCHEDULE_EXECUTING = "EXECUTING"
NETRO_SCHEDULE_VALID = "VALID"
NETRO_ERROR = "ERROR"
NETRO_OK = "OK"   
NETRO_EVENT_DEVICEOFFLINE = 1
NETRO_EVENT_DEVICEONLINE = 2
NETRO_EVENT_SCHEDULESTART = 3
NETRO_EVENT_SCHEDULEEND = 4

DEBUG_MODE = True

class netroException(Exception):
	def __init__(self, result) :
		self.message = result["errors"][0]["message"]
		self.code = result["errors"][0]["code"]

	def __str__(self) :
		return "a netro (NPA) error occurred -- error code #{0} -> {1}".format(self.code, self.message)

def getInfo(key) :
	payload = {'key': key}
	r = requests.get(NETRO_BASE_URL + NETRO_GET_INFO, params=payload)

	if DEBUG_MODE :
		print("netrofunction.getSchedules --> url = {0}".format(r.url))
		print("netrofunction.getInfo --> GET request status code = {0}, json result = {1}".format(r.status_code, r.json()))

	# is there a netro error ?
	if (r.json()['status'] == NETRO_ERROR) :
		raise netroException(r.json())
	# is there an http error
	elif (not r.ok) :
		r.raise_for_status()
	# so, it seems everything is ok !
	else :
		return r.json()

def setStatus(key, status) :
	payload = {'key': key, 'status' : status}
	r = requests.post(NETRO_BASE_URL + NETRO_POST_STATUS, data=payload)


	if DEBUG_MODE :
		print("netrofunction.getSchedules --> url = {0}".format(r.url))
		print("netrofunction.setStatus --> POST request status code = {0}, json result = {1}".format(r.status_code, r.json()))

	# is there a netro error ?
	if (r.json()['status'] == NETRO_ERROR) :
		raise netroException(r.json())
	# is there an http error
	elif (not r.ok) :
		r.raise_for_status()
	# so, it seems everything is ok !
	else :
		return r.json()

def getSchedules(key, zoneIds=None, startDate='', endDate='') :
	payload = {'key': key}
	if (zoneIds is not None) :
		payload['zones'] = '[{0}]'.format(', '.join(zoneIds))
	if (startDate) :
		payload['start_date'] = startDate
	if (endDate) :
		payload['end_date'] = endDate
	r = requests.get(NETRO_BASE_URL + NETRO_GET_SCHEDULES, params=payload)

	if DEBUG_MODE :
		print("netrofunction.getSchedules --> url = {0}".format(r.url))
		print("netrofunction.getSchedules --> GET request status code = {0}, json result = {1}".format(r.status_code, r.json()))

	# is there a netro error ?
	if (r.json()['status'] == NETRO_ERROR) :
		raise netroException(r.json())
	# is there an http error
	elif (not r.ok) :
		r.raise_for_status()
	# so, it seems everything is ok !
	else :
		return r.json()

