from device.TrafficLights import traffic_light
import os,sys
from utils.utils import get_logger

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


logger = get_logger(name=__name__)

def traffic_lights():
    while True:
        try:
            logger.info("Starting Trafiic Lights threading...")
            traffic_light()
        except Exception as e:
            logger.error("Something went wrong with traffic lights {}".format(e), exc_info=True)
            continue

traffic_lights()