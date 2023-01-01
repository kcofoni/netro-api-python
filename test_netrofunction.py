"""
This is a client program for testing the netrofunction module
"""

import logging
import time
import os
import netrofunction

# get the device keys from the environment variables
ctrl_key = os.environ['NPA_CTRL']
sens_key = os.environ['NPA_SENS']

# set log level (WARNING, INFO, DEBUG, ERROR, CRITICAL)
logging.basicConfig(format='%(asctime)s -- %(name)s:%(levelname)s:%(message)s',
                    level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S',
                    encoding='utf-8')

# get info
logging.info("running get info...")
res = netrofunction.get_info(ctrl_key)

# set status on
logging.info("running status on...")
res = netrofunction.set_status(ctrl_key, 1)

# attente de 30s
logging.info("waiting for 30s...")
time.sleep(30)

# set status off
logging.info("running status off...")
res = netrofunction.set_status(ctrl_key, 0)

# stop water
# logging.info("running stop water...")
# res = netrofunction.stopWater(ctrl_key)

# water
# logging.info("running water...")
# res = netrofunction.water(ctrl_key, 5, {'1'}, 0, '11:00')
# res = netrofunction.water(ctrl_key, 5, {'1'}, 10)

# set moisture
# logging.info("running set moisture...")
# res = netrofunction.setMoisture(ctrl_key, 70, {'1'})

# get moistures
logging.info("running get moistures...")
res = netrofunction.get_moistures(ctrl_key, {'1', '2'})

# no water
# logging.info("running no water...")
# res = netrofunction.noWater(ctrl_key, 10)

# get sensor data
logging.info("running get sensor data...")
res = netrofunction.get_sensor_data(sens_key, '2022-12-28', '2022-12-28')
res = netrofunction.get_sensor_data(sens_key)

# get events
logging.info("running get events...")
res = netrofunction.get_events(ctrl_key, 4, '2022-12-01', '2022-12-02')
res = netrofunction.get_events(ctrl_key)

# get schedules
logging.info("running get schedules...")
res = netrofunction.get_schedules(ctrl_key, {'1', '2', '3'})
res = netrofunction.get_schedules(
    ctrl_key, {'1', '2', '3'}, '2022-12-01', '2022-12-02')
res = netrofunction.get_schedules(ctrl_key, {'1', '2', '3'}, '2022-12-01')
