#!/usr/bin/python3
# ======================= Preamble =====================================

# Monitors a Renegade X Server, let's people know through a webhook if it restarts.

# ======================= Imports =====================================


# For time based stuff.
import time as time
from datetime import datetime, timezone

# For interaction with the host OS
import psutil

# Interaction with the webhook
import requests

# ======================= Metadata =====================================

AUTHOR = "Bas Imth"
LICENSE = "GPL-3"
SCRIPT_VERSION = "1.1"
headertext = """Monitors a Renegade X Server, let's people know through a webhook if it restarts."""

# ======================= Config ======================================

# Webhook used to notify the channel.
WEBHOOK = ""

# TODO: Multi-tennet
# Service to monitor
RX_SERVER = "renegade-x-marathon"

# We restart the server around these times in UTC
RESTART_HOUR = 4
RESTART_MINUTE = 30
# ======================= Functions =====================================


def version_information():
    print(
        "Author: {}\nLicense: {}\nVersion: {}\n".format(AUTHOR, LICENSE, SCRIPT_VERSION)
    )
    return


def monitor_service(server):
    starttime = time.time()
    print("Monitoring: {}".format(server))
    while True:
        service = service_running(server)
        if service and service["status"] == "running":
            # print(server, "is running")
            # Bit of a weird delay, but it goes too fast for its own good sometimes.
            time.sleep(1.2 - ((time.time() - starttime) % 1.2))
        elif service and service["status"] == "stopped":
            time.sleep(10.0 - ((time.time() - starttime) % 10.0))
        else:
            # print(server, "is not running")
            prepare_message(server, service["status"], "exited")
            time.sleep(10.0 - ((time.time() - starttime) % 10.0))


def service_running(name):
    service = None
    try:
        service = psutil.win_service_get(name)
        service = service.as_dict()
    except Exception as ex:
        print(str(ex))
    return service


def prepare_message(service, running, status):
    now = datetime.now(timezone.utc)
    if (
        now.hour == RESTART_HOUR
        and RESTART_MINUTE - 2 <= now.minute <= RESTART_MINUTE + 5
    ):
        print("We ignore this time.")
    else:
        data = {"content": "", "username": "Sho's clone"}
        data["embeds"] = [
            {
                "description": "Status: {}".format(running),
                "title": "Server: {} {}!".format(service, status),
            }
        ]
        notify_webhook(data)


def notify_webhook(data):
    message = requests.post(WEBHOOK, json=data)
    try:
        message.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(message.status_code))


def main():
    version_information()
    monitor_service(RX_SERVER)


# ======================= Main =====================================
main()
