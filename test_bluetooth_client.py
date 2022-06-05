from device.BluetoothClient import BluetoothClient


bluetooth_client = BluetoothClient()
nearby_devices = bluetooth_client.nearby_devices()
print(nearby_devices)

mac_address = bluetooth_client.get_mac_address()
print(mac_address)
bluetooth_client.rfcom_client("Hello")

