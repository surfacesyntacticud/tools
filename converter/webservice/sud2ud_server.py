#!/usr/bin/python
import subprocess
import json
import urlparse
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler

grew = "/home/guillaum/.opam/last/bin/grew"

dir = "/home/guillaum/webservice/"
grs = dir + "converter/grs/SUD_to_UD.grs"

def uniqid():
    from time import time
    return hex(int(time()*10000000))[2:]

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)

        id=uniqid()
        sud_file = dir+id+".sud.conll"
        ud_file = dir+id+".ud.conll"
        with open(sud_file, 'w') as f:
            f.write(post_body)

        try:
            subprocess.call([grew, "transform", "-grs", grs, "-i", sud_file, "-o", ud_file])
        except:
            self.send_response(402)
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        file = open(ud_file, "r")
        self.wfile.write(file.read())

httpd = SocketServer.TCPServer(("", 8383), MyHandler)
httpd.serve_forever()
