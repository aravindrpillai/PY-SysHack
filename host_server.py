from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import sqlite3
import socket
import json

'''
# This is the HOST server.
# This will be deployed on the host server and the url will be configured in the trogen.pyfile (poll_ip()) 
# trogen.py will hit the POST service to push the guest IP info
# Use the GET method to list all the affected guest informations
'''
def commit_data(ip, sys_name, sys_full_name):
    conn = sqlite3.connect('my_app_db')
    cursor = conn.cursor()
    #cursor.execute('DROP TABLE IF EXISTS record')
    cursor.execute('CREATE TABLE IF NOT EXISTS record (id INTEGER PRIMARY KEY, ip_address TEXT, sys_name TEXT, sys_full_name TEXT, exposed_at TEXT)')
    cursor.execute("DELETE FROM record where sys_name = ? and sys_full_name = ?", (sys_name, sys_full_name))
    cursor.execute("INSERT INTO record (ip_address, sys_name, sys_full_name, exposed_at) VALUES (?, ?, ?, ?)", (ip, sys_name, sys_full_name, str(datetime.now())))
    conn.commit()

def read_data():
    conn = sqlite3.connect('my_app_db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM record")
    rows = cursor.fetchall()
    thead = '''
    <tr>
    <td width='50px'><b>ID</b></td>
    <td width='250px'><b>IP Address</b></td>
    <td width='300px'><b>System Name</b></td>
    <td width='300px'><b>System Full Name</b></td>
    <td width='300px'><b>Exposed At</b></td>
    </tr>'''
    tbody = ""
    for row in rows:
        tbody += "<tr>"
        tbody += "<td>"+str(row[0])+"</td>"
        tbody += "<td>{}</td>".format(row[1])
        tbody += "<td>"+row[2]+"</td>"
        tbody += "<td>"+row[3]+"</td>"
        tbody += "<td>"+row[4]+"</td>"
        tbody += "</tr>"
    table = "<table border='1px'>"+thead+tbody+"</table>"
    conn.close()

    return table


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = read_data().encode('utf-8')
        self.wfile.write(response)
        
    def do_POST(self):
        message = None
        try:
            content_length = int(self.headers['Content-Length'])
            request = self.rfile.read(content_length).decode('utf-8')
            parsed_request = json.loads(request)
            commit_data(parsed_request["ip_address"], parsed_request["sys_name"], parsed_request["sys_full_name"])
            self.send_response(200)
            status = True
        except Exception as e_0:
            message = str(e_0)
            self.send_response(400)
            status = False
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_json = json.dumps({"status":status, "message":message})
        self.wfile.write(response_json.encode('utf-8'))


if __name__ == '__main__':
    print("starting host server...")
    hostname = socket.gethostname()
    addresses = socket.getaddrinfo(hostname, None, socket.AF_INET)
    ipv4_address = None
    for address in addresses:
        if address[0] == socket.AF_INET:
            ipv4_address = address[4][0]
            break
    port = 8081
    server = HTTPServer((ipv4_address, port), MyRequestHandler)
    print(f'Started server at http://{ipv4_address}:{port}')
    server.serve_forever()