#!/usr/bin/python
import json
import urlparse
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler

dir = "/home/guillaum/webservice/"

def uniqid():
    from time import time
    return hex(int(time()*10000000))[2:]

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)

        id=uniqid()
        sud_file = dir+id+".sud.conll"
        f = open(sud_file, 'w')
        f.write(post_body)
        f.close()

        subprocess.run(["wc", sud_file, ">", "xxx"]) # Run command

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("1\tle\til\n")


httpd = SocketServer.TCPServer(("", 8080), MyHandler)
httpd.serve_forever()
