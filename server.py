import os,sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn
from inference.kash.plate_ocr import get_plate_number
from device.MQTTclient import MQTTclient
from utils.utils import get_logger

app = Starlette(debug=True)

logger = get_logger(name=__name__)

mqtt_client = MQTTclient(
    host="axwsbhnc43ml1-ats.iot.eu-west-1.amazonaws.com",
    root_ca_path="certs/AmazonRootCA1.pem",
    private_key_path="certs/JunctionNodeA/7be9635fcee9f1b70a0f2f0e33f2468703e849d8388d73cce9d1c29b5fa77124-private.pem.key",
    certificate_path="certs/JunctionNodeA/7be9635fcee9f1b70a0f2f0e33f2468703e849d8388d73cce9d1c29b5fa77124-certificate.pem.crt",
)

mqtt_client.__setup__()

@app.route('/violations', methods=['POST']) 
async def homepage(request):
    
    try:
        data = await request.json()
        image = data['image']
        plate_number = get_plate_number(image)
        print('plate number: ', plate_number)
        plate_number = "RRT 111"
        payload = {
            "plateNumber": plate_number
        }
        mqtt_client.__publish__("traffic/A/violations", payload)
    except Exception as e:
        logger.error(f"Error processing a payload {e}")
        return JSONResponse({'error': 'Invalid request'})
    return JSONResponse({'message': 'Hello World!'})

@app.route('/traffic', methods=['POST'])
async def traffic(request):
    try:
        data = await request.json()

        logger.info(f'Received data {data}')
        return JSONResponse({'message': ''})
        
    except Exception as e:
        logger.error(f"Error processing a payload {e}")
        return JSONResponse({'error': 'Invalid request'})
    return JSONResponse({'message': 'Hello World!'})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)