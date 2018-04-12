#!/usr/bin/python
import json
import urlparse
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler

data = '{ x: "toto"}'

def some_function():
    print "some_function got called"
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data))

    def do_POST(self):
        print "got post!!"
        content_len = int(self.headers.getheader('content-length', 0))
        print (content_len)
        post_body = self.rfile.read(content_len)
        print (len (post_body))
        print ("---------------------------------------------")
        print (post_body)
        print ("---------------------------------------------")

        xxx = urlparse.parse_qs(post_body)
        print (xxx)
        #test_data = json.loads(post_body)
        #print "post_body(%s)" % (test_data)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        #self.wfile.write(json.dumps(data))
        self.wfile.write("1\tle\til")


httpd = SocketServer.TCPServer(("", 8080), MyHandler)
httpd.serve_forever()
