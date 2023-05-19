import threading
from fake_app import open_fake_program, create_startup_file
from host_server import start_host_server
from trogen import start_trogen_server, poll_and_notify_ipv4_address_change, get_ipv4_address

'''
# Sample code to test the entire application.
# This will spin up the guest and host servers.
# and start polling, which will update the host server about the guest IP
'''

host_server_port = 8180
poll_interval = 10 #Seconds
host_url = "http://{}:{}/".format(get_ipv4_address(), host_server_port) #Put the actual host url if its deployed to a diff server
trogen_server_port = 9090

start_host_server_thread = threading.Thread(target=start_host_server, args=(host_server_port,))
open_fake_program_thread = threading.Thread(target=open_fake_program, args=())
create_startup_file_thread = threading.Thread(target=create_startup_file, args=())
ip_poll_thread = threading.Thread(target=poll_and_notify_ipv4_address_change, args=(host_url, poll_interval,))
start_trogen_thread = threading.Thread(target=start_trogen_server, args=(trogen_server_port,))

start_host_server_thread.start()
create_startup_file_thread.start()
open_fake_program_thread.start()
ip_poll_thread.start()
start_trogen_thread.start()
