import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import time

from utils.utils import get_logger
from device.TrafficLights import (
    run_normal_state,
    traffic_light_pedestrian,
    traffic_state,
    traffic_normal,
    ped_traffic_state
)

is_raspberry = True
logger = get_logger(name="traffic_observer")
BUTTON = 20
try:

    import RPi.GPIO as GPIO

    try:
        GPIO.cleanup()
    except Exception as e:
        pass

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    is_raspberry = True
except Exception as e:
    logger.error(f"Not running on Raspberry Pi {e}")
    is_raspberry = False

# try:
#     logger.info("Starting Traffic Lights threading...")
#     while True:
#         if GPIO.input(BUTTON) == GPIO.HIGH:
#             print('Button pressed')
#             logger.info("Sending SIGNALS To other juction")
#             counter = 0
#             while counter < 61:
#                 logger.info(f"count {counter}")
#                 if counter == 60:
#                     pass
#                     # traffic_state(1, 0, 0)  # stop the vehicles

#                     # traffic_light_pedestrian()
#                 time.sleep(1)
#                 counter += 1
#         # traffic_normal()
#         ped_traffic_state(1, 0, 0)
# except KeyboardInterrupt as e:
#     logger.error("Something went wrong with traffic lights {}".format(e), exc_info=True)
#     GPIO.cleanup()
