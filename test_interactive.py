"""
This is a client program for testing the netrofunction module interactively
usage : [-hv] -e [getinfo|setstatus]
-h : help
-v : verbose mode
-e : execute a netro function among (getinfo, setstatus)
-s : status as a parameter of the netro function to be executed
"""

import logging
import os
import sys
import getopt
import datetime
from time import gmtime, strftime
import netrofunction

# get the device keys from the environment variables
ctrl_key = os.environ["NPA_CTRL"]
sens_key = os.environ["NPA_SENS"]

# set log level (WARNING, INFO, DEBUG, ERROR, CRITICAL)
logging.basicConfig(
    format="%(asctime)s -- %(name)s:%(levelname)s:%(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S",
    encoding="utf-8",
)

SIMU_NETRO_URL = "http://vmtest:9080/"
PROD_NETRO_URL = "https://api.netrohome.com/npa/v1/"

NETRO_ZONE_ITH = "ith"
NETRO_ZONE_ENABLED = "enabled"
NETRO_ZONE_SMART = "smart"
NETRO_ZONE_NAME = "name"


# set proper netro environnement (prod or simu)
netrofunction.set_netro_base_url(PROD_NETRO_URL)

# pylint: disable=cell-var-from-loop,consider-using-dict-items,unused-variable


class Zone:
    """Zone of a Netro controller."""

    def __init__(
        self,
        ith: int,
        enabled: bool,
        smart: str,
        name: str,
    ) -> None:
        """Create a zone (virtual device)."""
        self.ith = ith
        self.enabled = enabled
        self.smart = smart
        self.name = name
        self.past_schedules = list[dict[str, any]]  # type: ignore[valid-type]
        self.coming_schedules = list[dict[str, any]]  # type: ignore[valid-type]
        self.moistures = list[dict[str, any]]  # type: ignore[valid-type]

    @property
    def last_run(self) -> dict:
        """Get the last executed/executing run."""
        if len(self.past_schedules) != 0:
            return self.past_schedules[0]
        return None

    @property
    def next_run(self) -> dict:
        """Get the next valid run to be executed in the future."""
        if len(self.coming_schedules) != 0:
            return self.coming_schedules[0]
        return None

    @property
    def moisture(self) -> dict:
        """Get the last reported moisture."""
        if len(self.moistures) != 0:
            return self.moistures[0]
        return None


zones = dict()


def getinfo(key):
    """get current information of the device whose key is the serial number and log the main data"""
    res = netrofunction.get_info(key)
    logging.info("return = %s", res["status"])
    logging.info("token_remaining = %s", res["meta"]["token_remaining"])
    if (res["data"].get("device")) is not None:
        logging.info("name = %s", res["data"]["device"]["name"])
        logging.info("status = %s", res["data"]["device"]["status"])
        if res["data"]["device"].get("battery_level"):
            logging.info("battery level = %s", res["data"]["device"]["battery_level"])
        for zone in res["data"]["device"]["zones"]:
            if zone["enabled"]:
                logging.info(
                    "zone [%s]: (%s, %s, %s)",
                    zone["ith"],
                    zone["name"],
                    zone["enabled"],
                    zone["smart"],
                )
                zones[zone["ith"]] = Zone(
                    zone["ith"], zone["enabled"], zone["smart"], zone["name"]
                )
        logging.debug("---------------- zones --------------------")
        for zone_key in zones:
            logging.info(
                "ith : %s, name : %s, enabled : %s, smart : %s",
                zones[zone_key].ith,
                zones[zone_key].name,
                zones[zone_key].enabled,
                zones[zone_key].smart,
            )
        logging.debug("-----------------fin zone-------------------")
    elif res["data"].get("sensor"):
        logging.info("name = %s", res["data"]["sensor"]["name"])
        logging.info("status = %s", res["data"]["sensor"]["status"])
    else:
        logging.error("type of netro device not managed %s")


def getschedules(key):
    """get the schedules and determine the last and next watering"""
    schedules = netrofunction.get_schedules(key)["data"]["schedules"]
    for schedule in schedules:
        logging.debug("schedule[%s] : %s", type(schedule), schedule)
    # split par zone et tri par start date
    if not zones:
        getinfo(key)
    for zone_key in zones:
        #    for i in range(1, 4):
        past_schedules_of_zone = list(
            filter(
                lambda schedule: schedule["zone"]
                == zone_key  # pylint: disable=cell-var-from-loop
                and schedule["status"] in ["EXECUTED", "EXECUTING"],
                schedules,
            )
        )
        logging.debug("past schedules pour la zone %s", zone_key)
        past_schedules_of_zone_sorted = sorted(
            past_schedules_of_zone,
            key=(lambda schedule_of_zone: schedule_of_zone["start_time"]),
            reverse=True,
        )
        for schedule in past_schedules_of_zone_sorted:
            # tri par start_date
            logging.debug(schedule)
        post_schedules_of_zone = list(
            filter(
                lambda schedule: schedule["zone"]
                == zone_key  # pylint: disable=cell-var-from-loop
                and schedule["status"] == "VALID"
                and schedule["start_time"] > strftime("%Y-%m-%dT%H:%M:%S", gmtime()),
                schedules,
            )
        )
        logging.debug("post schedules pour la zone %s", zone_key)
        post_schedules_of_zone_sorted = sorted(
            post_schedules_of_zone,
            key=(lambda schedule_of_zone: schedule_of_zone["start_time"]),
            reverse=False,
        )
        for schedule in post_schedules_of_zone_sorted:
            # tri par start_date
            logging.debug(schedule)
        if past_schedules_of_zone_sorted:
            logging.info(
                "le dernier arrosage pour la zone %s était le %s (UTC)",
                zone_key,
                datetime.datetime.fromisoformat(
                    past_schedules_of_zone_sorted[0]["start_time"]
                ),
            )
        else:
            logging.info("pas d'info sur le dernier arrosage de la zone %s", zone_key)
        if post_schedules_of_zone_sorted:
            logging.info(
                "le prochain arrosage pour la zone %s sera le %s à %s",
                zone_key,
                post_schedules_of_zone_sorted[0]["local_date"],
                post_schedules_of_zone_sorted[0]["local_start_time"],
            )
        else:
            logging.info("pas d'info sur le prochain arrosage de la zone %s", zone_key)


def getmoistures(key):
    """get the moistures and determine the last value for each zone"""
    moistures = netrofunction.get_moistures(key)["data"]["moistures"]
    for moisture in moistures:
        logging.debug("moisture[%s] : %s", type(moisture), moisture)
    # split par zone et tri par start date
    for i in range(1, 4):
        moistures_of_zone = list(
            filter(lambda moisture: moisture["zone"] == i, moistures)
        )
        logging.debug("moistures pour la zone %s", i)
        for moisture in moistures_of_zone:
            # tri par start_date
            logging.debug(moisture)
        if moistures_of_zone:
            logging.info(
                "humidité de %s%% estimée le 2023-03-29 pour la zone %s",
                moistures_of_zone[0]["moisture"],
                i,
            )
        else:
            logging.info("pas d'info sur l'humidité de la zone %s", i)


def main(argv):
    """main program"""
    netro_function = ""
    status_tobeset = ""
    moisture_tobeset = ""
    device_type = ""
    zone_id = ""
    opts, args = getopt.getopt(argv, "hd:z:m:ve:s:", ["execute=", "status=", "device="])
    for opt, arg in opts:
        if opt == "-h":
            print(
                "usage : test_interactive [-hv] -e <getinfo|getschedules|getmoistures|setstatus> [-s <on|off>] [-d <ctrl|sensor>] [-z <id_zone>] [-m <moisture>]"
            )
            sys.exit()
        elif opt in ("-e", "--execute"):
            netro_function = arg
        elif opt in ("-s", "--status"):
            status_tobeset = arg
        elif opt in ("-d", "--device"):
            device_type = arg
        elif opt in ("-z", "--zone"):
            zone_id = arg
        elif opt in ("-m", "--moisture"):
            moisture_tobeset = arg
    if netro_function == "":
        print("missing netro function")
        sys.exit()
    elif netro_function == "getinfo":
        print("get info...")
        if device_type == "ctrl":
            getinfo(ctrl_key)
        elif device_type == "sensor":
            getinfo(sens_key)
        else:
            getinfo(ctrl_key)
            getinfo(sens_key)
    elif netro_function == "getschedules":
        print("get schedules...")
        getschedules(ctrl_key)
    elif netro_function == "getmoistures":
        print("get moistures...")
        getmoistures(ctrl_key)
    elif netro_function == "setstatus":
        if status_tobeset == "":
            print("status missing for set status netro function")
        else:
            print("set status", status_tobeset, "...")
            netrofunction.set_status(ctrl_key, 1 if status_tobeset == "on" else 0)
    elif netro_function == "setmoisture":
        if moisture_tobeset == "":
            print("moisture missing for set moisture netro function")
        elif zone_id == "":
            print("zone id missing for set moisture netro function")
        else:
            print("set moisture", status_tobeset, "...")
            netrofunction.set_moisture(ctrl_key, moisture_tobeset, zone_id)
    else:
        print("unknown netro function")


if __name__ == "__main__":
    main(sys.argv[1:])
