#!/usr/bin/env python3
#
# Multi-Purpose APRS Daemon
# Author: Joerg Schultze-Lutter, 2020
#
# Core process
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import sys
import logging
import aprslib
import time

########################################


# APRSlib callback
# Extract the fields from the APRS message, start the parsing process,
# execute the command and send the command output back to the user
def mycallback(raw_aprs_packet):
    global number_of_served_packages
    global aprs_message_cache

    logger = logging.getLogger(__name__)
    logger.info(raw_aprs_packet)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(module)s -%(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

aprsis_callsign = "N0CALL"
aprsis_passcode = "-1"
aprsis_simulate_send = True
aprsis_filter = "g/WXBOT/DF1JSL*"
aprsis_server_name = "euro.aprs2.net"  # our login server
aprsis_server_port = 14580  # server port

# Define dummy values for both APRS task schedules and AIS object
AIS = None

#
# Finally, let's enter the 'eternal loop'
#
try:
    while True:
        # Set call sign and pass code
        AIS = aprslib.IS(aprsis_callsign, aprsis_passcode)

        # Set the APRS_IS server name and port
        AIS.set_server(aprsis_server_name, aprsis_server_port)

        # Set the APRS_IS (call sign) filter, based on our config file
        AIS.set_filter(aprsis_filter)

        # Debug info on what we are trying to do
        logger.info(
            msg=f"Establish connection to APRS_IS: server={aprsis_server_name},"
            f"port={aprsis_server_port},filter={aprsis_filter}"
            f"APRS-IS User: {aprsis_callsign}, APRS-IS passcode: {aprsis_passcode}"
        )

        AIS.connect(blocking=True)
        if AIS._connected == True:
            logger.info(msg="Established the connection to APRS_IS")

            #
            # We are on the verge of starting the aprslib callback consumer
            # This section is going to be left only in the case of network
            # errors or if the user did raise an exception
            #
            logger.info(msg="Starting callback consumer")
            AIS.consumer(mycallback, blocking=True, immortal=True, raw=False)

            #
            # We have left the callback, let's clean up a few things
            logger.info("Have left the callback")

            # Verbindung schließen
            logger.info(msg="Closing APRS connection to APRS_IS")
            AIS.close()
        else:
            logger.info(msg="Cannot re-establish connection to APRS_IS")

except (KeyboardInterrupt, SystemExit):
    logger.info("received exception!")

    # Close the socket if it is still open
    if AIS:
        AIS.close()
