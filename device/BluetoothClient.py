import bluetooth
from dataclasses import dataclass
from utils.utils import get_logger
from bleak import BleakScanner



@dataclass
class BluetoothClient:
    logger = get_logger(name=__name__)
    is_ble: bool = False

    async def get_mac_address(self) -> str:
        devices = await BleakScanner.discover()
        for device in devices:
            print(await device)
            
        # mac_address = bluetooth.read_local_bdaddr()
        # logger.info("Mac address: %s", mac_address)
        # return mac_address
    
    def start_bluetooth(self) -> None:
        self.logger.info("Starting bluetooth...")


