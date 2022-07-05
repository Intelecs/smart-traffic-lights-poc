import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import time

from utils.utils import get_logger
from device.TrafficLights import (
    run_normal_state,
    traffic_light_pedestrian,
    traffic_state,
)

is_raspberry = True
logger = get_logger(name="traffic_observer")
try:

    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    is_raspberry = True
except Exception as e:
    logger.error(f"Not running on Raspberry Pi {e}")
    is_raspberry = False

try:
    logger.info("Starting Traffic Lights threading...")
    while True:
        if GPIO.input(20) == GPIO.HIGH:
            logger.info("Sending SIGNALS To other juction")
            counter = 0
            while counter < 61:
                if counter == 60:
                    traffic_state(1, 0, 0)  # stop the vehicles
                    traffic_light_pedestrian()
                time.sleep(1)
                counter += 1
        run_normal_state()
except Exception as e:
    logger.error("Something went wrong with traffic lights {}".format(e), exc_info=True)