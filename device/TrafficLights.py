import time

import os, sys
from uuid import getnode



CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from utils.utils import get_logger

logger = get_logger(name=__name__)

is_raspberry = False
try:
    
    import RPi.GPIO as GPIO
    GPIO.setWarnings(False)
    GPIO.setmode(GPIO.BCM)
    is_raspberry = True

except:
    logger.error("Not running on Raspberry Pi")
    is_raspberry = False


RED_PIN = 17 
GREEN_PIN = 27
YELLOW_PIN = 22

if is_raspberry:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(YELLOW_PIN, GPIO.OUT)

def traffic_state(red, yellow, green) -> None:
    if is_raspberry:
        GPIO.output(RED_PIN, red)
        GPIO.output(YELLOW_PIN, yellow)
        GPIO.output(GREEN_PIN, green)


def traffic_light():
    traffic_state(1, 0, 0)
    time.sleep(5)
    traffic_state(0, 1, 0)
    time.sleep(5)
    traffic_state(0, 0, 1)
    time.sleep(5)
    traffic_state(1, 0, 0)
    time.sleep(5)

def run():
    while True:
        traffic_light()

