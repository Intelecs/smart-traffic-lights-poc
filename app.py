from device.BluetoothClient import BluetoothClient
import asyncio


if __name__ == "__main__":
    bluetooth_client = BluetoothClient()
    asyncio.run(bluetooth_client.get_mac_address())