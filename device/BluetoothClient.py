import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import subprocess
from typing import List

import bluetooth
from dataclasses import dataclass
from utils.utils import get_logger

try:
    subprocess.Popen(['sudo', 'hciconfig', 'hci0', 'piscan'])
except Exception as e:
    pass

uuid: str = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

@dataclass
class BluetoothClient:
    logger = get_logger(name=__name__)
    is_ble: bool = False

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

    def rfcom_server(self):

        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", bluetooth.PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]
        self.logger.info("Listening on port %d", port)

        
        bluetooth.advertise_service(
            server_sock,
            "Smart Trafic",
            service_id=uuid,
            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE],
        )

        self.logger.info("Waiting for connection on %d", port)

        client_sock, client_info = server_sock.accept()
        self.logger.info("Accepted connection from %s", client_info)

        try:
            while True:
                try:
                    
                    data = client_sock.recv(1024)
                    if not data:
                        break
                    self.logger.info("received [%s]", data)
                except Exception as e:
                    self.logger.error(f"An error occurred while receiving data: {e}")
                    continue
        except Exception as e:
            self.logger.info(f"Disconnected {e}", exc_info=True)
            client_sock.close()
            server_sock.close()

        
        
        self.logger.info("Finished")

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

        self.logger.info("Connecting to \"%s\" on %s:%s" % (name, host, port))

        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((host, port))

        self.logger.info("Sending data...")
        sock.send(data.encode())

        self.logger.info("Waiting for data...")



