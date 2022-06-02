import os,sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from typing import List

import bluetooth
from dataclasses import dataclass
from utils.utils import get_logger



@dataclass
class BluetoothClient:
    logger = get_logger(name=__name__)
    is_ble: bool = False

    def get_mac_address(self) -> bool:
        mac_address = bluetooth.read_local_bdaddr()
        self.logger.info("Mac address: %s", mac_address[0])
        return mac_address[0]
    
    def near_by_devices(self) -> List[str]:
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        self.logger.info("Found %d devices", len(nearby_devices))
        return nearby_devices
    
    def start_bluetooth(self) -> None:
        self.logger.info("Starting bluetooth...")


