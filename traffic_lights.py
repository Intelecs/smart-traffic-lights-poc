import os,sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from device.TrafficLights import traffic_light


if __name__ == '__main__':
    while True:
        traffic_light()