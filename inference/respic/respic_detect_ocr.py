import numpy as np
import cv2
import torch
import easyocr
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

def img_processing(image, local_path: str = None):
    if local_path is None:
        raise ValueError("Please spcify the location of the model")
    model = torch.hub.load('ultralytics/yolov5','custom', path=local_path, force_reload=True, source='local', pretrained =False)
    results = model(image)

    plateNo = results.xyxy[0][0][:4]
    roi = []
    for bound in plateNo:
        roi.append(int(bound))


    marks = image[roi[1]:roi[3],roi[0]:roi[2]]
    
    return marks

def ocr(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray)
    shape = (np.asarray(result).shape)
    text = ""

    if result:
        if result[0][-1] > 0.5:
            if shape == (1,3):
                text = result[0][-2]
            else:
                text = result[0][-2]+result[1][-2]

        else:
            gray = cv2.resize( gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            gray = cv2.medianBlur(gray, 3)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
            result = reader.readtext(thresh)
            print(result)
            if shape == (1,3):
                text = result[0][-2]
            else:
                text = result[0][-2]+result[1][-2]

    elif not result:
        gray = cv2.resize( gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        gray = cv2.medianBlur(gray, 3)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        result = reader.readtext(thresh)
        print(result)
        if shape == (1,3):
            text = result[0][-2]
        else:
            text = result[0][-2]+result[1][-2]
    return text

def plate_ocr(image_path, model_path):
    image = cv2.imread(image_path)
    image = img_processing(image, local_path=model_path)
    text = ocr(image)
    print(text)
    return text
