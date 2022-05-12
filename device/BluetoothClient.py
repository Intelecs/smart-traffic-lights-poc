import bluetooth
from dataclasses import dataclass
from utils.utils import get_logger



@dataclass
class BluetoothClient:
    logger = get_logger(name=__name__)
    is_ble: bool = False

    def get_mac_address(self) -> bool:
        mac_address = bluetooth.read_local_bdaddr()
        self.logger.info("Mac address: %s", mac_address)
        # return mac_address
    
    def start_bluetooth(self) -> None:
        self.logger.info("Starting bluetooth...")


