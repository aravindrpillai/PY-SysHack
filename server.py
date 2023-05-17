from http.server import BaseHTTPRequestHandler, HTTPServer
from poll_ip import get_ipv4_address
import socket
import json
import textwrap

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        fqdn = socket.getfqdn()
        hostname = socket.gethostname()
        op = '<b>Hello Buddy, the system is all yours</b> <br/><br/>IP: {} <br/> System Name: {} <br/> Fully Qualified System Name : {}'.format(get_ipv4_address(), hostname, fqdn )
        self.wfile.write(op.encode('utf-8'))
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        code = self.rfile.read(content_length).decode('utf-8')
        formatted_code = ""
        for line in code.splitlines():
            formatted_code += ('\n'+textwrap.indent(line, '    '))
        function_code = f'def runMe():\n{formatted_code}\n    return result'
        print(function_code)
        exec(function_code, locals())
        output_json = eval("runMe()")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_json = json.dumps(output_json)
        self.wfile.write(response_json.encode('utf-8'))



def start_server(port=8080):
    print("starting server...")
    host = get_ipv4_address()
    server = HTTPServer((host, port), MyRequestHandler)
    print(f'Started server at http://{host}:{port}')
    server.serve_forever()



# if __name__ == '__main__':
#     server_thread = threading.Thread(target=start_server, args=(8080,))
#     server_thread.start()
