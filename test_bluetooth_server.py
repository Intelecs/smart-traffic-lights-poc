# from device.BluetoothClient import BluetoothClient


# bluetooth_client = BluetoothClient()

# nearby_devices = bluetooth_client.nearby_devices()
# print(nearby_devices)

# mac_address = bluetooth_client.get_mac_address()
# print(mac_address)

# is_server_connected = False
# while not is_server_connected:
#     try:
#         bluetooth_client.rfcom_server()
#         is_server_connected = True
#     except Exception as e:
#         print(e)
#         is_server_connected = False


#!/usr/bin/env python3
"""PyBluez simple example rfcomm-server.py

Simple demonstration of a server application that uses RFCOMM sockets.

Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $
"""

import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)






def open_socket():
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)
    try:
        while True:
            print("Starting Server")
            data = client_sock.recv(1024)
            if not data:
                continue
            print("Received", data)
    except Exception as e:
        client_sock.close()
        server_sock.close()
        open_socket()

open_socket()


# server_sock.close()
# print("All done.")