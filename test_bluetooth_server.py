from device.BluetoothClient import BluetoothClient


bluetooth_client = BluetoothClient()

nearby_devices = bluetooth_client.nearby_devices()
print(nearby_devices)

mac_address = bluetooth_client.get_mac_address()
print(mac_address)

bluetooth_client.rfcom_server()

# is_server_connected = False
# while not is_server_connected:
#     try:
#         bluetooth_client.rfcom_server()
#         is_server_connected = True
#     except Exception as e:
#         print(e)
#         is_server_connected = False
