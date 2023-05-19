'''
Below are some sample code to hack the host.
NOTE : if you need an output, make sure in your code you sent the output to variable 'result'
'''

#To list out all the files and folders from a folder
import os
folder = "C:/windows"
folders = []
for root, dirnames, filenames in os.walk(folder):
    folders.extend(dirnames)
    break
result = folders



#To get the ip address
import socket
hostname = socket.gethostname()
addresses = socket.getaddrinfo(hostname, None, socket.AF_INET)
ipv4_address = None
for address in addresses:
    if address[0] == socket.AF_INET:
        ipv4_address = address[4][0]
        break
result = ipv4_address



#To make a beep
import winsound
winsound.Beep(1000, 2000)
result = None


#To execute a cmd command
import subprocess
command = "net stat"
result = subprocess.check_output(command, shell=True, universal_newlines=True).strip()