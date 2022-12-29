import netrofunction
import logging
import time
import os

# get the device keys from the environment variables
ctrl_key = os.environ['NPA_CTRL']
sens_key = os.environ['NPA_SENS']

# set log level (WARNING, INFO, DEBUG, ERROR, CRITICAL)
logging.basicConfig(format='%(asctime)s -- %(name)s:%(levelname)s:%(message)s',
                    level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S',
                    encoding='utf-8')

# get info
logging.info("running get info...")
r = netrofunction.getInfo(ctrl_key)

# set status on
logging.info("running status on...")
r = netrofunction.setStatus(ctrl_key, 1)

# attente de 30s
logging.info("waiting for 30s...")
time.sleep(30)

# set status off
logging.info("running status off...")
r = netrofunction.setStatus(ctrl_key, 0)

# stop water
# logging.info("running stop water...")
# r = netrofunction.stopWater(ctrl_key)

# water
# logging.info("running water...")
# r = netrofunction.water(ctrl_key, 5, {'1'}, 0, '11:00')
# r = netrofunction.water(ctrl_key, 5, {'1'}, 10)

# set moisture
# logging.info("running set moisture...")
# r = netrofunction.setMoisture(ctrl_key, 70, {'1'})

# get moistures
logging.info("running get moistures...")
r = netrofunction.getMoistures(ctrl_key, {'1', '2'})

# no water
# logging.info("running no water...")
# r = netrofunction.noWater(ctrl_key, 10)

# get sensor data
logging.info("running get sensor data...")
r = netrofunction.getSensorData(sens_key, '2022-12-28', '2022-12-28')
r = netrofunction.getSensorData(sens_key)

# get events
logging.info("running get events...")
r = netrofunction.getEvents(ctrl_key, 4, '2022-12-01', '2022-12-02')
r = netrofunction.getEvents(ctrl_key)

# get schedules
logging.info("running get schedules...")
r = netrofunction.getSchedules(ctrl_key, {'1', '2', '3'})
r = netrofunction.getSchedules(
    ctrl_key, {'1', '2', '3'}, '2022-12-01', '2022-12-02')
r = netrofunction.getSchedules(ctrl_key, {'1', '2', '3'}, '2022-12-01')
