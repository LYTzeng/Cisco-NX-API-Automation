'''
作為HTTP接收端，此程式碼在 server 上執行
'''
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from base64 import decodebytes
from urllib import parse
import json
import argparse

PORT = 8000
parser = argparse.ArgumentParser(description='HTTP Port Number')
parser.add_argument('port', metavar='N', type=int)
args = parser.parse_args()
PORT = args.port

class ReqHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        body = json.dumps(parse.parse_qs(decodebytes(post_body).decode('utf-8')))
        print(body)

Handler = ReqHandler
httpd = TCPServer(('', PORT), Handler)

print('Serving at port ', PORT)
httpd.serve_forever()
