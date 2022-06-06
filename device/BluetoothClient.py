import os, sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import subprocess
from typing import List

import bluetooth
from dataclasses import dataclass
from utils.utils import get_logger
import socket

try:
    subprocess.Popen(["sudo", "hciconfig", "hci0", "piscan"])
except Exception as e:
    pass

uuid: str = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


@dataclass
class BluetoothClient:
    logger = get_logger(name=__name__)
    is_ble: bool = False
    is_server_connected: bool = False
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def get_mac_address(self) -> bool:
        mac_address = bluetooth.read_local_bdaddr()
        self.logger.info("Mac address: %s", mac_address[0])
        return mac_address[0]

    def nearby_devices(self) -> List[str]:
        nearby_devices = bluetooth.discover_devices(lookup_names=True, flush_cache=True)
        self.logger.info("Found %d devices", len(nearby_devices))
        return nearby_devices

    def start_bluetooth(self) -> None:
        self.logger.info("Starting bluetooth...")

    def connect(self) -> None:
        self.logger.info("Connecting to....",)
        while True:
            try:
                self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                _sock = socket.fromfd(self.server_socket.fileno(), 31, 1, 3)
                _sock.settimeout(5)
                self.server_sock.bind(("", bluetooth.PORT_ANY))
                self.server_sock.listen(1)
                bluetooth.advertise_service(
                    self.server_sock,
                    "Smart Trafic Server",
                    service_id=uuid,
                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                    profiles=[bluetooth.SERIAL_PORT_PROFILE],
                )
                break
            except Exception as e:
                self.logger.error(e)
                # self.server_sock.close()
                self.logger.info("Waiting for connection...")
                continue

    def rfcom_server(self):

        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        self.logger.info("Waiting for connection...")
        # self.connect()

        port = self.server_sock.getsockname()[1]
        self.logger.info("Listening on port %d", port)

        self.logger.info("Waiting for connection on %d", port)

        client_sock, client_info = None, None
        client_sock, client_info = self.server_sock.accept()
        self.logger.info("Accepted connection from %s", client_info)

        while True:
            try:

                data = client_sock.send("Hello")
                time.sleep(0.1)
                if not data:
                    continue
                self.logger.info("Received [%s]", data)
            except Exception as e:
                self.logger.error(
                    f"An error occurred while receiving data: {e}, {client_info}",
                    exc_info=True,
                )
                client_sock.close()
                self.server_sock.close()
                self.connect()
                continue
                # time.sleep(1)
                # return

    def rfcom_client(self, data: str):
        self.logger.info("Starting client...")

        service_matches = bluetooth.find_service(uuid=uuid)

        if len(service_matches) == 0:
            self.logger.info("Couldn't find the service")
            return

        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        self.logger.info('Connecting to "%s" on %s:%s' % (name, host, port))

        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((host, port))

        received = sock.recv(1024)
        self.logger.info("Sending data...")
        self.logger.info("Sent [%s]", received)
        sock.close()
