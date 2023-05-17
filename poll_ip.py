import socket
import time

"""
#Return the IPv4 address of the machine.
"""
def get_ipv4_address():
    hostname = socket.gethostname()
    addresses = socket.getaddrinfo(hostname, None, socket.AF_INET)
    ipv4_address = None
    for address in addresses:
        if address[0] == socket.AF_INET:
            ipv4_address = address[4][0]
            break
    return ipv4_address


'''
#Function to poll and notify if there is a change in IPV4
#If there is a chnage, this will inform the host about the new IP update
'''
def poll_and_notify_ipv4_address_change(interval=60):
    current_address = None
    while True:
        new_address = get_ipv4_address()
        print(new_address)
        if new_address != current_address:
            print(f'IPv4 address changed from {current_address} to {new_address}')
            current_address = new_address
        time.sleep(interval)