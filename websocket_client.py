from utils.utils import get_logger
import socket
import nmap
# import asyncio
import websocket
import rel 

logger = get_logger(name=__name__)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 8000))
local_ip = sock.getsockname()[0]
sock.close()

print(local_ip)
nmap_scanner = nmap.PortScanner()
scan_range = nmap_scanner.scan(hosts="192.168.100.0-100", arguments="-p 8000 --open")

ip_address = None
if len(scan_range) > 0:
    ip_address = list(scan_range["scan"].keys())[0]
    print(ip_address)


def on_message(ws, message):
    received_message = str(message)
    print(received_message)
    ws.send("Hello World! 1")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


if __name__ == "__main__":
    server = websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        "ws://" + ip_address + ":8000/ws",
        on_message=on_message,
        on_close=on_close,
        on_open=on_open,
        on_error=on_error,
    )

    

    ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)
    rel.dispatch()
