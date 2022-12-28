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
    def __init__(self, result):
        self.message = result["errors"][0]["message"]
        self.code = result["errors"][0]["code"]

    def __str__(self):
        return "a netro (NPA) error occurred -- error code #{0} -> {1}".format(self.code, self.message)


def getInfo(key):
    payload = {'key': key}
    r = requests.get(NETRO_BASE_URL + NETRO_GET_INFO, params=payload)

    if DEBUG_MODE:
        print("netrofunction.getInfo --> url = {0}".format(r.url))
        print("netrofunction.getInfo --> GET request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def setStatus(key, status):
    payload = {'key': key, 'status': status}
    r = requests.post(NETRO_BASE_URL + NETRO_POST_STATUS, data=payload)

    if DEBUG_MODE:
        print("netrofunction.setStatus --> url = {0}".format(r.url))
        print("netrofunction.setStatus --> data = {0}".format(payload))
        print("netrofunction.setStatus --> POST request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def getSchedules(key, zoneIds=None, startDate='', endDate=''):
    payload = {'key': key}
    if (zoneIds is not None):
        payload['zones'] = '[{0}]'.format(', '.join(zoneIds))
    if (startDate):
        payload['start_date'] = startDate
    if (endDate):
        payload['end_date'] = endDate
    r = requests.get(NETRO_BASE_URL + NETRO_GET_SCHEDULES, params=payload)

    if DEBUG_MODE:
        print("netrofunction.getSchedules --> url = {0}".format(r.url))
        print("netrofunction.getSchedules --> GET request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def getMoistures(key, zoneIds=None, startDate='', endDate=''):
    payload = {'key': key}
    if (zoneIds is not None):
        payload['zones'] = '[{0}]'.format(', '.join(zoneIds))
    if (startDate):
        payload['start_date'] = startDate
    if (endDate):
        payload['end_date'] = endDate
    r = requests.get(NETRO_BASE_URL + NETRO_GET_MOISTURES, params=payload)

    if DEBUG_MODE:
        print("netrofunction.getMoistures --> url = {0}".format(r.url))
        print("netrofunction.getMoistures --> GET request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def reportWeather(key, date, condition, rain, rain_prob, temp, t_min, t_max, t_dew, wind_speed, humidity, pressure):
    payload = {'key': key, 'date': date}
    if (condition):
        payload['condition'] = condition
    if (rain):
        payload['rain'] = rain
    if (rain_prob):
        payload['rain_prob'] = rain_prob
    if (temp):
        payload['temp'] = temp
    if (t_min):
        payload['t_min'] = t_min
    if (t_max):
        payload['t_max'] = t_max
    if (t_dew):
        payload['t_dew'] = t_dew
    if (wind_speed):
        payload['wind_speed'] = wind_speed
    if (humidity):
        payload['humidity'] = humidity
    if (pressure):
        payload['pressure'] = pressure
    r = requests.post(NETRO_BASE_URL + NETRO_POST_REPORTWEATHER, data=payload)

    if DEBUG_MODE:
        print("netrofunction.reportWeather --> url = {0}".format(r.url))
        print("netrofunction.reportWeather --> data = {0}".format(payload))
        print("netrofunction.reportWeather --> POST request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def setMoisture(key, moisture, zoneIds):
    payload = {'key': key, 'moisture': moisture}
    if (zoneIds is not None):
        payload['zones'] = '[{0}]'.format(', '.join(zoneIds))
    r = requests.post(NETRO_BASE_URL + NETRO_POST_MOISTURE, data=payload)

    if DEBUG_MODE:
        print("netrofunction.setMoisture --> url = {0}".format(r.url))
        print("netrofunction.setMoisture --> data = {0}".format(payload))
        print("netrofunction.setMoisture --> POST request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def water(key, duration, zoneIds=None, delay=0, startTime=''):
    payload = {'key': key, 'duration': duration}
    if (zoneIds is not None):
        payload['zones'] = '[{0}]'.format(', '.join(zoneIds))
    if (delay > 0):
        payload['delay'] = delay
    if (startTime):
        payload['start_time'] = startTime
    r = requests.post(NETRO_BASE_URL + NETRO_POST_WATER, data=payload)

    if DEBUG_MODE:
        print("netrofunction.water --> url = {0}".format(r.url))
        print("netrofunction.water --> data = {0}".format(payload))
        print("netrofunction.water --> POST request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def stopWater(key):
    payload = {'key': key}
    r = requests.post(NETRO_BASE_URL + NETRO_POST_STOPWATER, data=payload)

    if DEBUG_MODE:
        print("netrofunction.stopWater --> url = {0}".format(r.url))
        print("netrofunction.stopWater --> data = {0}".format(payload))
        print("netrofunction.stopWater --> POST request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def noWater(key, days=None):
    payload = {'key': key}
    if (days is not None):
        payload['days'] = round(days)

    r = requests.post(NETRO_BASE_URL + NETRO_POST_NOWATER, data=payload)

    if DEBUG_MODE:
        print("netrofunction.noWater --> url = {0}".format(r.url))
        print("netrofunction.noWater --> data = {0}".format(payload))
        print("netrofunction.noWater --> POST request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def getSensorData(key, startDate='', endDate=''):
    payload = {'key': key}
    if (startDate):
        payload['start_date'] = startDate
    if (endDate):
        payload['end_date'] = endDate
    r = requests.get(NETRO_BASE_URL + NETRO_GET_SENSORDATA, params=payload)

    if DEBUG_MODE:
        print("netrofunction.getSensorData --> url = {0}".format(r.url))
        print("netrofunction.getSensorData --> GET request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()


def getEvents(key, typeOfEvent=0, startDate='', endDate=''):
    payload = {'key': key}
    if (typeOfEvent > 0):
        payload['event'] = typeOfEvent
    if (startDate):
        payload['start_date'] = startDate
    if (endDate):
        payload['end_date'] = endDate
    r = requests.get(NETRO_BASE_URL + NETRO_GET_EVENTS, params=payload)

    if DEBUG_MODE:
        print("netrofunction.getEvents --> url = {0}".format(r.url))
        print("netrofunction.getEvents --> GET request status code = {0}, json result = {1}".format(
            r.status_code, r.json()))

    # is there a netro error ?
    if (r.json()['status'] == NETRO_ERROR):
        raise netroException(r.json())
    # is there an http error
    elif (not r.ok):
        r.raise_for_status()
    # so, it seems everything is ok !
    else:
        return r.json()
