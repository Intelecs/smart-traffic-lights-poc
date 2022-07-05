import time

import os, sys
from uuid import getnode
import threading

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
PED_RED_PIN = 25
PED_GREEN_PIN = 24



if is_raspberry:
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(YELLOW_PIN, GPIO.OUT)
    GPIO.setup(PED_RED_PIN, GPIO.OUT)
    GPIO.setup(PED_GREEN_PIN, GPIO.OUT)
    GPIO.setup(PED_YELLOW_PIN, GPIO.OUT)

    


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

def traffic_normal(delay = 10):
    traffic_state(1, 0, 0)
    ped_traffic_state(0, 0, 1)
    time.sleep(delay)

    traffic_state(0, 1, 0)
    ped_traffic_state(0, 1, 0)
    time.sleep(delay)

    traffic_state(0, 0, 1)
    ped_traffic_state(1, 0, 0)
    time.sleep(delay)

    traffic_state(0, 1, 0)
    ped_traffic_state(0, 1, 0)
    time.sleep(delay)



def run_normal_state(delay=10):

    threading.Thread(target=traffic_light_vehicles, args=(delay,)).start()
    threading.Thread(target=traffic_light_pedestrian, args=(delay,)).start()
    # traffic_light_vehicles(delay)
    # traffic_light_pedestrian(delay)
