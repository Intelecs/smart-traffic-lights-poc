ip_address = "192.168.43.0-100"

ip_address = ip_address.split(".")[:-1]
ip_address = ".".join(ip_address) + ".0-255"
print(ip_address)
