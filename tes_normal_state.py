import os,sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


from utils.utils import get_logger
from device.TrafficLights import run_normal_state

is_raspberry = True
logger = get_logger(name="traffic_observer")
try:
    
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    is_raspberry = True
except Exception as e:
    logger.error(f"Not running on Raspberry Pi {e}")
    is_raspberry = False

while True:
    try:
        logger.info("Starting Traffic Lights threading...")
        run_normal_state()
    except Exception as e:
        logger.error("Something went wrong with traffic lights {}".format(e), exc_info=True)
        continue
    break