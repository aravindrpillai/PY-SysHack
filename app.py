from ui import create_window
from startup_folder import create_startup_file
from poll_ip import poll_and_notify_ipv4_address_change
from server import start_server
import threading


ui_thread = threading.Thread(target=create_window, args=())
start_up_file_thread = threading.Thread(target=create_startup_file, args=())
server_thread = threading.Thread(target=start_server, args=(8080,))
ip_poll_thread = threading.Thread(target=poll_and_notify_ipv4_address_change, args=(10,))


ui_thread.start()
start_up_file_thread.start()
ip_poll_thread.start()
server_thread.start()