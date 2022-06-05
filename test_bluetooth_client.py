from device.BluetoothClient import BluetoothClient


bluetooth_client = BluetoothClient()
nearby_devices = bluetooth_client.nearby_devices()
print(nearby_devices)
bluetooth_client.rfcom_client("Hello")

