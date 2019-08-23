#!/usr/bin/python
import subprocess
import json
import urlparse
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler

dir = "/home/guillaum/webservice/"
grew = "/home/guillaum/.opam/last/bin/grew"
grs = "/home/guillaum/webservice/SUD/grs/UD_to_SUD.grs"

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
        with open(ud_file, 'w') as f:
            f.write(post_body)

        try:
            subprocess.call([grew, "transform", "-grs", grs, "-i", ud_file, "-o", sud_file])
        except:
            self.send_response(402)
            return


        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        file = open(sud_file, "r")
        self.wfile.write(file.read())

httpd = SocketServer.TCPServer(("", 8181), MyHandler)
httpd.serve_forever()
