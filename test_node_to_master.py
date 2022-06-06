import asyncio
from utils.utils import get_logger
import requests
import socket

logger = get_logger(name=__name__)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
local_ip = sock.getsockname()[0]
sock.close()


async def violation_api(image):
    url = f"http://{local_ip}:8000/violations"
    headers = {'Content-Type': 'application/json'}
    data = {
        "right": image
    }
    try:
        requests.post(url, json=data, headers=headers)
        logger.info(f"Violation sent to {url}")
    except Exception as e:
        logger.error(f"Error sending violation to {url}")
        logger.error(e)

async def send_signal(image):
    asyncio.ensure_future(violation_api(image))
    await asyncio.sleep(0)

if __name__ == '__main__':
    while True:
        asyncio.ensure_future(send_signal("RED"))