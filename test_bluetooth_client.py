from device.BluetoothClient import BluetoothClient


bluetooth_client = BluetoothClient()
nearby_devices = bluetooth_client.nearby_devices()
print(nearby_devices)

mac_address = bluetooth_client.get_mac_address()
print(mac_address)

while True:
    try:
        bluetooth_client.rfcom_server()
    except Exception as e:
        print(e)
        continue
