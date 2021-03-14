#!/usr/bin/env python3
import sys
import logging
import aprslib
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(module)s -%(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

aprsis_callsign = sys.argv[1]
aprsis_passcode = sys.argv[2]

aprsis_filter = "g/WXBOT/DF1JSL*"
aprsis_server_name = "euro.aprs2.net"
aprsis_server_port = 14580

#
# Message that we want to send
aprsis_send_message = ""
#


AIS = aprslib.IS(aprsis_callsign, aprsis_passcode)
AIS.set_server(aprsis_server_name, aprsis_server_port)
AIS.set_filter(aprsis_filter)

AIS.connect(blocking=True)
if AIS._connected == True:
	logger.info(
    	msg=f"Established connection to APRS_IS: server={aprsis_server_name},"
    	f"port={aprsis_server_port},filter={aprsis_filter}"
    	f"APRS-IS User: {aprsis_callsign}, APRS-IS passcode: {aprsis_passcode}"
	)
	AIS.sendall(aprsis_send_message)
	AIS.close()
else:
	print ("An error has occurred")
