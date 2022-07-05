import re
import time

import os, sys
from uuid import getnode
import threading
import socket
import nmap

# import asyncio
import websocket
import rel

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from utils.utils import get_logger

logger = get_logger(name=__name__)

is_raspberry = False
try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    is_raspberry = True
except Exception as e:
    logger.error(f"Not running on Raspberry Pi {e}")
    is_raspberry = False


# Control pins for traffic lights for vehicles
RED_PIN = 17
GREEN_PIN = 22
YELLOW_PIN = 27

# control pins for traffic lights for pedestrians
PED_YELLOW_PIN = 23
PED_RED_PIN = 24
PED_GREEN_PIN = 25


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 8000))
local_ip = sock.getsockname()[0]
sock.close()


ip_address = local_ip.split(".")[:-1]
ip_address = ".".join(ip_address) + ".0-255"

nmap_scanner = nmap.PortScanner()
scan_range = nmap_scanner.scan(hosts=ip_address, arguments="-p 8000 --open")
ip_address = None
if len(scan_range) > 0:
    ip_address = list(scan_range["scan"].keys())[0]


def on_message(ws, message):
    received_message = str(message)
    print(received_message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")

# server = websocket.enableTrace(True)

from websocket import create_connection

ws = websocket.WebSocketApp(
    "ws://" + ip_address + ":8000/ws",
    on_message=on_message,
    on_close=on_close,
    on_open=on_open,
    on_error=on_error,
)

def run_ws_client():
    ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)
    rel.dispatch()

# threading.Thread(target=run_ws_client, daemon=True).start()

ws = create_connection(
    "ws://" + ip_address + ":8000/ws")

# ws.run_forever(dispatcher=rel)
# rel.signal(2, rel.abort)
# rel.dispatch()


BUTTON = 20
if is_raspberry:
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(YELLOW_PIN, GPIO.OUT)
    GPIO.setup(PED_RED_PIN, GPIO.OUT)
    GPIO.setup(PED_GREEN_PIN, GPIO.OUT)
    GPIO.setup(PED_YELLOW_PIN, GPIO.OUT)

    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def traffic_state(red, yellow, green) -> None:
    if is_raspberry:
        GPIO.output(RED_PIN, red)
        GPIO.output(YELLOW_PIN, yellow)
        GPIO.output(GREEN_PIN, green)


def ped_traffic_state(red, yellow, green) -> None:
    if is_raspberry:
        GPIO.output(PED_RED_PIN, red)
        GPIO.output(PED_YELLOW_PIN, yellow)
        GPIO.output(PED_GREEN_PIN, green)


def traffic_light_vehicles(delay: int = 10):
    logger.info("Should open Send RED Signal to Junction A")
    traffic_state(1, 0, 0)
    time.sleep(delay)
    logger.info("Should open Send YELLOW Signal to Junction A")
    traffic_state(0, 1, 0)
    time.sleep(delay)
    logger.info("Should open Send GREEN Signal to Junction A")
    traffic_state(0, 0, 1)
    time.sleep(delay)


def traffic_light_pedestrian(delay: int = 10):
    logger.info("Should open Send RED Signal to Junction A")
    ped_traffic_state(1, 0, 0)
    time.sleep(delay)
    logger.info("Should open Send YELLOW Signal to Junction A")
    ped_traffic_state(0, 1, 0)
    time.sleep(delay)
    logger.info("Should open Send GREEN Signal to Junction A")
    ped_traffic_state(0, 0, 1)
    time.sleep(delay)


MASTER = True


def traffic_normal(delay=10):
    traffic_state(1, 0, 0)
    ped_traffic_state(0, 0, 1)
    payload = {"traffic_light_vehicles": "RED", "traffic_light_pedestrian": "GREEN"}
    ws.send(str(payload))

    time.sleep(delay)

    traffic_state(0, 1, 0)
    ped_traffic_state(0, 1, 0)
    payload = {"traffic_light_vehicles": "YELLOW", "traffic_light_pedestrian": "YELLOW"}
    ws.send(str(payload))
    time.sleep(delay)

    traffic_state(0, 0, 1)
    ped_traffic_state(1, 0, 0)
    payload = {"traffic_light_vehicles": "GREEN", "traffic_light_pedestrian": "RED"}
    ws.send(str(payload))
    time.sleep(delay)

    traffic_state(0, 1, 0)
    ped_traffic_state(0, 1, 0)
    payload = {"traffic_light_vehicles": "YELLOW", "traffic_light_pedestrian": "YELLOW"}
    ws.send(str(payload))
    time.sleep(delay)


def run():
    try:
        logger.info("Starting Traffic Lights threading...")
        message = ws.recv()
        print(message)
        while True:
            button_state = GPIO.input(BUTTON)
            logger.info("Button state: %s", button_state)
            if GPIO.input(BUTTON) == GPIO.LOW:
                print("Button pressed")
                logger.info("Sending SIGNALS To other juction")
                counter = 0
                while counter < 61:
                    logger.info(f"count {counter}")
                    if counter == 60:
                        logger.info("Do something...")
                        # traffic_state(1, 0, 0)  # stop the vehicles
                        #
                        traffic_state(1, 0, 0)
                        time.sleep(5)
                        traffic_light_pedestrian()

                        # traffic_light_pedestrian()

                    time.sleep(1)
                    counter += 1
            traffic_normal()
            # ped_traffic_state(1, 1, 1)
            # traffic_light_pedestrian()
            # ped_traffic_state(0, 0, 0)
    except KeyboardInterrupt as e:
        logger.error("Something went wrong with traffic lights {}".format(e), exc_info=True)
    except Exception as e:
        logger.error("Something went wrong with traffic lights {}".format(e), exc_info=True)
    finally:
        GPIO.cleanup()
