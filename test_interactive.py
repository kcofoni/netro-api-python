"""
This is a client program for testing the netrofunction module interactively
usage : [-hv] -e [getinfo|setstatus]
-h : help
-v : verbose mode
-e : execute a netro function among (getinfo, setstatus)
-s : status as a parameter of the netro function to be executed
"""

import logging
import time
import os
import netrofunction
import sys, getopt
import json

# get the device keys from the environment variables
ctrl_key = os.environ['NPA_CTRL']
sens_key = os.environ['NPA_SENS']

# set log level (WARNING, INFO, DEBUG, ERROR, CRITICAL)
logging.basicConfig(format='%(asctime)s -- %(name)s:%(levelname)s:%(message)s',
                    level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S',
                    encoding='utf-8')

def getinfo(key):
    res = netrofunction.get_info(key)
    logging.info("return = %s", res["status"])
    logging.info("token_remaining = %s", res["meta"]["token_remaining"])
    if (res["data"].get("device")) is not None:
        logging.info("name = %s", res["data"]["device"]["name"])
        logging.info("status = %s", res["data"]["device"]["status"])
    elif (res["data"].get("sensor")):
        logging.info("name = %s", res["data"]["sensor"]["name"])
        logging.info("status = %s", res["data"]["sensor"]["status"])
    else:
        logging.error("type of netro device not managed %s")

def main (argv):
    netro_function = ''
    status_tobeset = ''
    device_type = ''
    opts, args = getopt.getopt(argv, "hd:ve:s:", ["execute=", "status=", "device="])
    for opt, arg in opts:
        if opt == '-h':
            print ('usage : test_interactive [-hv] -e [getinfo|setstatus] [-s [on|off]] [-d [ctrl|sensor]]')
            sys.exit()
        elif opt in ("-e", "--execute"):
            netro_function = arg
        elif opt in ("-s", "--status"):
            status_tobeset = arg
        elif opt in ("-d", "--device"):
            device_type = arg
    if netro_function == '':
        print ('missing netro function')
        sys.exit()
    elif netro_function == 'getinfo':
        print ('get info...')
        if (device_type == "ctrl"):
            getinfo(ctrl_key)
        elif (device_type == "sensor"):
            getinfo(sens_key)
        else:
            getinfo(ctrl_key)
            getinfo(sens_key)            
    elif netro_function == 'setstatus':
        if status_tobeset == '':
            print ('status missing for set status netro function')
        else:
            print ('set status', status_tobeset, '...')
            netrofunction.set_status(ctrl_key, 1 if status_tobeset == "on" else 0)
    else:
        print('unknown netro function')

if __name__ == "__main__":
    main(sys.argv[1:])
    

    
            