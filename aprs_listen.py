#!/usr/bin/env python3
import sys
import logging
import aprslib
import time

def mycallback(raw_aprs_packet):
    logger = logging.getLogger(__name__)
    logger.info(raw_aprs_packet)


## main test core
###
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(module)s -%(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

aprsis_callsign = "N0CALL"
aprsis_passcode = "-1"
aprsis_simulate_send = True
aprsis_filter = "g/WXBOT/DF1JSL*"
aprsis_server_name = "euro.aprs2.net"
aprsis_server_port = 14580
AIS = None

try:
    while True:
        AIS = aprslib.IS(aprsis_callsign, aprsis_passcode)
        AIS.set_server(aprsis_server_name, aprsis_server_port)
        AIS.set_filter(aprsis_filter)
        logger.info(
            msg=f"Establish connection to APRS_IS: server={aprsis_server_name},"
            f"port={aprsis_server_port},filter={aprsis_filter}"
            f"APRS-IS User: {aprsis_callsign}, APRS-IS passcode: {aprsis_passcode}"
        )

        AIS.connect(blocking=True)
        if AIS._connected == True:
            logger.info(msg="Established the connection to APRS_IS")
            logger.info(msg="Starting callback consumer")
            AIS.consumer(mycallback, blocking=True, immortal=True, raw=False)
            logger.info("Have left the callback")
            logger.info(msg="Closing APRS connection to APRS_IS")
            AIS.close()
        else:
            logger.info(msg="Cannot re-establish connection to APRS_IS")

except (KeyboardInterrupt, SystemExit):
    logger.info("received exception!")
    if AIS:
        AIS.close()
