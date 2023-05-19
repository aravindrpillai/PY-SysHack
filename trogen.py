from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import textwrap
import requests
import socket
import time
import json

def get_ipv4_address():
    hostname = socket.gethostname()
    addresses = socket.getaddrinfo(hostname, None, socket.AF_INET)
    ipv4_address = None
    for address in addresses:
        if address[0] == socket.AF_INET:
            ipv4_address = address[4][0]
            break
    return ipv4_address


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        fqdn = socket.getfqdn()
        hostname = socket.gethostname()
        op = '<b>Hello Buddy, the system is all yours now</b> <br/><br/>IP: {} <br/> System Name: {} <br/> Fully Qualified System Name : {}'.format(get_ipv4_address(), hostname, fqdn )
        self.wfile.write(op.encode('utf-8'))
        
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        code = self.rfile.read(content_length).decode('utf-8')
        formatted_code = ""
        for line in code.splitlines():
            formatted_code += ('\n'+textwrap.indent(line, '    '))
        function_code = f'def runMe():\n{formatted_code}\n    return result'
        exec(function_code, locals())
        output_json = eval("runMe()")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_json = json.dumps(output_json)
        self.wfile.write(response_json.encode('utf-8'))

'''
#Function to start the server on the guest machine
'''
def start_server(port=8080):
    print("starting server...")
    host = get_ipv4_address()
    server = HTTPServer((host, port), MyRequestHandler)
    print(f'Started server at http://{host}:{port}')
    server.serve_forever()

'''
#Function to poll and notify if there is a change in IPV4
#If there is a chnage, this will inform the host about the new IP update
'''
def poll_and_notify_ipv4_address_change(interval=60):
    url = "http://host_server_url:8081/"
    current_address = None
    while True:
        new_address = get_ipv4_address()
        print(new_address)
        if new_address != current_address:
            print(f'IPv4 address changed from {current_address} to {new_address}')
            current_address = new_address
            headers = {'Content-Type': 'application/json'}
            fqdn = socket.getfqdn()
            hostname = socket.gethostname()
            data = {
                "ip_address":new_address,
                "sys_name":hostname,
                "sys_full_name":fqdn
            }
            response = requests.post(url, data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("successfully informed")
            else:
                print('Error:', response.status_code)
                return None
        time.sleep(interval)


if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server, args=(8080,))
    ip_poll_thread = threading.Thread(target=poll_and_notify_ipv4_address_change, args=(10,))
    ip_poll_thread.start()
    server_thread.start()

