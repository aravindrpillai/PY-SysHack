import os
folders = []
for root, dirnames, filenames in os.walk("C:\\"):
    folders.extend(dirnames)
    break
result = folders


import socket
hostname = socket.gethostname()
addresses = socket.getaddrinfo(hostname, None, socket.AF_INET)
ipv4_address = None
for address in addresses:
    if address[0] == socket.AF_INET:
        ipv4_address = address[4][0]
        break
result = ipv4_address


import winsound
winsound.Beep(1000, 2000)