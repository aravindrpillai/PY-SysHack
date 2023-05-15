from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import threading
import socket
import json
import time

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            fqdn = socket.getfqdn()
            hostname = socket.gethostname()
            op = '<b>Hello Buddy, the system is all yours</b> <br/><br/>IP: {} <br/> System Name: {} <br/> Fully Qualified System Name : {}'.format(get_ipv4_address(), hostname, fqdn )
            self.wfile.write(op.encode('utf-8'))
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'Hello, API!'}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/cmd':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            result = subprocess.run(['cmd', '/c', 'dir'], stdout=subprocess.PIPE)
            op = result.stdout.decode('utf-8')
            self.wfile.write(op.encode('utf-8'))
        else:
            self.send_error(404)

def start_server(port=8080):
    print("starting server...")
    host = get_ipv4_address()
    server = HTTPServer((host, port), MyRequestHandler)
    print(f'Started server at http://{host}:{port}')
    server.serve_forever()

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


'''
#Main function
'''
if __name__ == '__main__':
    ipv4_poll_thread = threading.Thread(target=poll_and_notify_ipv4_address_change, args=(10,))
    server_thread = threading.Thread(target=start_server, args=(8080,))
    
    ipv4_poll_thread.start()
    server_thread.start()
    