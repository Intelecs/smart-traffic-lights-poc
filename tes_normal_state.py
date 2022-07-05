import os, sys

from cv2 import log

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import time

from utils.utils import get_logger
from device.TrafficLights import (
    run
)

if __name__ == '__main__':
    run()

# is_raspberry = True
# logger = get_logger(name="traffic_observer")
# BUTTON = 20
# try:

#     import RPi.GPIO as GPIO

#     # try:
#     #     GPIO.cleanup()
#     # except Exception as e:
#     #     pass

#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     # GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#     is_raspberry = True
# except Exception as e:
#     logger.error(f"Not running on Raspberry Pi {e}")
#     is_raspberry = False

# try:
#     logger.info("Starting Traffic Lights threading...")
#     while True:
#         button_state = GPIO.input(BUTTON)
#         logger.info("Button state: %s", button_state)
#         if GPIO.input(BUTTON) == GPIO.LOW:
#             print("Button pressed")
#             logger.info("Sending SIGNALS To other juction")
#             counter = 0
#             while counter < 61:
#                 logger.info(f"count {counter}")
#                 if counter == 60:
#                     logger.info("Do something...")
#                     # traffic_state(1, 0, 0)  # stop the vehicles
#                     #
#                     traffic_state(1, 0, 0)
#                     time.sleep(5)
#                     traffic_light_pedestrian()

#                     # traffic_light_pedestrian()

#                 time.sleep(1)
#                 counter += 1
#         traffic_normal()
#         # ped_traffic_state(1, 1, 1)
#         # traffic_light_pedestrian()
#         # ped_traffic_state(0, 0, 0)
# except KeyboardInterrupt as e:
#     logger.error("Something went wrong with traffic lights {}".format(e), exc_info=True)
# finally:
#     GPIO.cleanup()
