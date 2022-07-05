import os,sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from datetime import datetime
from cv_processor.CentroidTracker import CentroidTracker
from cv_processor.TrackableObject import TrackableObject
import numpy as np
import imutils
import cv2
import math
import json
import base64
from utils.utils import get_logger
from device.TrafficLights import traffic_light
import asyncio
from vidgear.gears import VideoGear, PiGear
import requests
import socket
import dlib
import time
from threading import Thread


is_raspberry = True
logger = get_logger(name="traffic_observer")
try:
    
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    is_raspberry = True
except Exception as e:
    logger.error(f"Not running on Raspberry Pi {e}")
    is_raspberry = False

config_file = "configs/traffic_observer.json"



config = None
with open(config_file, "r") as f:
    config = json.load(f)
    f.close()

""" _summary_
Get IP address to connect with Async server
"""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
local_ip = sock.getsockname()[0]
sock.close()

conf = config

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]


async def violation_api(image):
    url = f"http://{local_ip}:8000/violations"
    headers = {'Content-Type': 'application/json'}
    data = {
        "image": image
    }
    try:
        requests.post(url, json=data, headers=headers)
        logger.info(f"Violation sent to {url}")
    except Exception as e:
        logger.error(f"Error sending violation to {url}")
        logger.error(e)

async def send_violation(image):
    asyncio.ensure_future(violation_api(image))
    await asyncio.sleep(0)


def traffic_lights():
    while True:
        try:
            logger.info("Starting Trafiic Lights threading...")
            traffic_light()
        except Exception as e:
            logger.error("Something went wrong with traffic lights {}".format(e), exc_info=True)
            continue



if __name__ == '__main__':

    # Starting Raspberry Pi GPIO
    Thread(target=traffic_lights).start()


    net = cv2.dnn.readNetFromCaffe(conf["prototxt_path"],
        conf["model_path"])
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    if is_raspberry:
        # stream = PiGear( logging=True).start()
        pass
    else:
        pass
    stream = VideoGear(source=0, stabilize=False, logging=True).start()
    
    # stream = cv2.VideoCapture(0)

    H = None
    W = None

    ct = CentroidTracker(maxDisappeared=conf["max_disappear"],
        maxDistance=conf["max_distance"])
    trackers = []
    trackable_objects = {}

    total_frames = 0

    logFile = None

    points = [("A", "B"), ("B", "C"), ("C", "D")]
    
    # fps = FPS().start()

    total_frames = 0
   
    logFile = None

    points = [("A", "B"), ("B", "C"), ("C", "D")]

    # fps = FPS().start()

    while True:

        frame = stream.read()
        ts = datetime.now()

        # logger.info("Red Ligh status {}".format(GPIO.input(17)))

        if frame is None:
            break


        frame = imutils.resize(frame, width=conf["frame_width"])
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if is_raspberry:

                # Red
                # cv2.circle(
                #     frame, (30, 30), 20, (0,0,255), -1
                # )
                if GPIO.input(17) == GPIO.HIGH:
                    cv2.circle(frame, (30, 30), 20, (0,0,255), -1)

                    # cv2.circle(frame, (30, 130), 20, (0,128,0), -1)
                else:

                    cv2.circle(
                    frame, (30, 30), 20, (128,128,128), -1
                    )
                

                GREEN_PIN = 27
                
                YELLOW_PIN = 22
                if GPIO.input(27) == GPIO.HIGH:
                    # Yellow 
                    cv2.circle(frame, (30, 80), 20, (51, 255, 249), -1)

                    # cv2.circle(frame, (30, 30), 20, (0,0,255), -1)
                else:
                    cv2.circle(
                    frame, (30, 80), 20, (128,128,128), -1
                    )
                
                if GPIO.input(22) == GPIO.HIGH:
                    # Green
                    cv2.circle(frame, (30, 130), 20, (0,128,0), -1)
                    # cv2.circle(frame, (30, 80), 20, (51, 255, 249), -1)
                else:
                    cv2.circle(
                    frame, (30, 130), 20, (128,128,128), -1
                    )
                 
        
        # set frame dimensions if are empty
        if W is None or H is None:
            (H, W) = frame.shape[:2]
            # (H, W) = (480, 640)
            meterPerPixel = conf["distance"] / W
        
        """ _summary_
        initialize our list of bounding box rectangles returned by
        either (1) our object detector or (2) the correlation trackers
        """
        rects = []

        """ _summary_ 
        check to see if we should run a more computationally expensive
        object detection method to aid our tracker

        1. initialize our new set of object trackers
        2. network and obtain the detections
        3. loop over the detections
        4. extract the confidence (i.e., probability) associated  with the prediction
        5. filter out weak detections by ensuring the `confidence`
        6. extract the index of the class label from the
        """

        if total_frames % conf["track_object"] == 0:

            trackers = []
            blob = cv2.dnn.blobFromImage(frame, size=(300, 300),
                ddepth=cv2.CV_8U)
            net.setInput(blob, scalefactor=1.0/127.5, mean=[127.5,
                127.5, 127.5])
            detections = net.forward()

            for i in np.arange(0, detections.shape[2]):
                
                confidence = detections[0, 0, i, 2]

                if confidence > conf["confidence"]:
                    idx = int(detections[0, 0, i, 1])
                    

                    if CLASSES[idx] not in [ "bicycle", "bus", "car", "motorbike", "train"]:
                        continue
                    object_name = CLASSES[idx]

                    box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                    (startX, startY, endX, endY) = box.astype("int")

                    """ 
                    _summary_
                    construct a dlib rectangle object from the bounding
                    box coordinates and then start the dlib correlation
                    tracker
                    """

                    text_size = cv2.getTextSize(object_name, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                    text_width, text_height = text_size[0], text_size[1]


                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)

                    cv2.rectangle(frame, (startX, startY + 20), (startX + text_width, startY + text_height),  (0, 255, 0), -1)
                    cv2.putText(frame, object_name, (startX, startY + 20)
                , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
                    tracker = {
                        "tracker": tracker,
                        "object_name": object_name
                    }
                    trackers.append(tracker)

        else:

            for _tracker in trackers:

                tracker = _tracker["tracker"]
                tracker.update(rgb)
                pos = tracker.get_position()
    
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())
                # add the bounding box coordinates to the rectangles list

                rects.append((startX, startY, endX, endY))

        """ _summary_
        use the centroid tracker to associate the (1) old object
        centroids with (2) the newly computed object centroids
        """

        objects = ct.update(rects)

        for (objectID, centroid) in objects.items():
            to = trackable_objects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid)

            elif not to.estimated:
                if to.direction is None:
                    y = [c[0] for c in to.centroids]
                    direction = centroid[0] - np.mean(y)
                    to.direction = direction

                """ _summary_
                if the direction is positive (indicating the object is moving from left to right)

                1. if the centroid's x-coordinate is greater than the corresponding point then set the timestamp as current timestamp and set the position as the centroid's x-coordinate
                2. if the centroid's x-coordinate is greater than the corresponding point then set the timestamp as current timestamp and set the position as the centroid's x-coordinate
                """

                
                if to.direction > 0:
                    if to.timestamp["A"] == 0 :

                        if centroid[0] > conf["speed_estimation_zone"]["A"]:
                            to.timestamp["A"] = ts
                            to.position["A"] = centroid[0]

                    elif to.timestamp["B"] == 0:
                        
                        if centroid[0] > conf["speed_estimation_zone"]["B"]:
                            to.timestamp["B"] = ts
                            to.position["B"] = centroid[0]
                    elif to.timestamp["C"] == 0:
                        
                        if centroid[0] > conf["speed_estimation_zone"]["C"]:
                            to.timestamp["C"] = ts
                            to.position["C"] = centroid[0]
                    elif to.timestamp["D"] == 0:
                        if centroid[0] > conf["speed_estimation_zone"]["D"]:
                            to.timestamp["D"] = ts
                            to.position["D"] = centroid[0]
                            to.lastPoint = True
                elif to.direction < 0:

                    if to.timestamp["D"] == 0 :
                        if centroid[0] < conf["speed_estimation_zone"]["D"]:
                            to.timestamp["D"] = ts
                            to.position["D"] = centroid[0]

                    elif to.timestamp["C"] == 0:

                        if centroid[0] < conf["speed_estimation_zone"]["C"]:
                            to.timestamp["C"] = ts
                            to.position["C"] = centroid[0]

                    elif to.timestamp["B"] == 0:

                        if centroid[0] < conf["speed_estimation_zone"]["B"]:
                            to.timestamp["B"] = ts
                            to.position["B"] = centroid[0]

                    elif to.timestamp["A"] == 0:

                        if centroid[0] < conf["speed_estimation_zone"]["A"]:
                            to.timestamp["A"] = ts
                            to.position["A"] = centroid[0]
                            to.lastPoint = True

                """ _summary_ 
                # check to see if the vehicle is past the last point and
                # the vehicle's speed has not yet been estimated, if yes,
                # then calculate the vehicle speed and log it if it's
                # over the limit
                """
                if to.lastPoint and not to.estimated:
                    
                    estimatedSpeeds = []
                    # loop over all the pairs of points and estimate the
                    # vehicle speed
                    for (i, j) in points:
                        # calculate the distance in pixels
                        d = to.position[j] - to.position[i]
                        distanceInPixels = abs(d)
                        # check if the distance in pixels is zero, if so,
                        # skip this iteration
                        if distanceInPixels == 0:
                            continue
                        # calculate the time in hours
                        t = to.timestamp[j] - to.timestamp[i]
                        timeInSeconds = abs(t.total_seconds())
                        timeInHours = timeInSeconds / (60 * 60)
                        # calculate distance in kilometers and append the
                        # calculated speed to the list
                        distanceInMeters = distanceInPixels * meterPerPixel
                        distanceInKM = distanceInMeters / 1000
                        estimatedSpeeds.append(distanceInKM / timeInHours)
                    # calculate the average speed
                    to.calculate_speed(estimatedSpeeds)
                    # set the object as estimated
                    to.estimated = True
                    # print("[INFO] Speed of the vehicle ID: {} that just passed"\
                    #     " is: {:.2f} KPH".format(to.objectID, to.speedKMPH))
            # store the trackable object in our dictionary
            trackable_objects[objectID] = to

            current_object = trackable_objects[objectID]

            speed = 0 if to.speedKMPH is None or  math.isnan(to.speedKMPH) else int(to.speedKMPH)
    
            text = "SPEED {} Km/h".format('--')
            # text = "OBJECT {}".format(current_object.objectID)
            
            """ _summary_
            Look if the object has violated the speed limit
            """
            area_3 = [(600, 350), (1050, 350), (850, 250), (500, 250)]

            bounding_line = cv2.line(frame, (10, 600), (500, 600), (0, 0, 255), 2)
            for area in [area_3]:
                pass
                # cv2.polylines(frame, [np.array(area, np.int32)], True, (15,220,10), 2)



            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_width, text_height = text_size[0], text_size[1]
            cv2.rectangle(frame, (centroid[0], centroid[1]), (centroid[2], centroid[3]), (0, 255, 0), 2)
            # cv2.rectangle(frame, (centroid[0], centroid[1]),  (centroid[2] - 20, centroid[1] - 20), (0, 255, 0), -1)
            cv2.rectangle(frame, (centroid[0], centroid[1]), (centroid[0] + text_width, centroid[1] + text_height),  (0, 255, 0), -1)
            cv2.putText(frame, text, (centroid[0], centroid[1] + 10)
                , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

            y_max, x_max, channels = frame.shape
        
            if centroid[2] > 500 and centroid[3] > 600: 
                # pass
                logger.info("[INFO] Vehicle is out of the frame")
                if is_raspberry:
                    """ 
                    _summary_ setting traffic lights on window
                    """
                    if GPIO.input(17) == GPIO.HIGH:
                        # speed_limit_violation = True
                        cv2.putText(frame, f"TRAFFIC LIMIT VIOLATION BY object {current_object}", (x_max - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
                        _, buffer = cv2.imencode(".jpg", frame)
                        image = base64.b64encode(buffer).decode("utf-8")
                        asyncio.run(send_violation(image))

            
       
        if conf["display"]:

            cv2.imshow("Smart traffic Light System {}".format(local_ip), frame)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key is pressed, break from the loop
            if key == ord("q"):
                break
        """ _summary_ 
        increment the total number of frames processed thus far and then update the FPS counter
        """
        total_frames += 1
    try:

        cv2.destroyAllWindows()
        # clean up
        logger.info("[INFO] cleaning up...")
        stream.stop()
    except Exception as e:
        logger.error("[ERROR] {}".format(e))
        cv2.destroyAllWindows()
        stream.stop()