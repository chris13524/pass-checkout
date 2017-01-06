#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse, parse_qs
import requests
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

PORT_NUMBER = 8989

class myHandler(BaseHTTPRequestHandler):
	
	def do_POST(self):
		# process request
		length = int(self.headers.getheader('content-length'))
		field_data = self.rfile.read(length)
		fields = parse_qs(field_data)

		# retrieve parameters
		url = fields["url"][0]
		prop = fields["prop"][0]
		value = fields["value"][0]

		# make proxy POST
		r = requests.post(url, data={prop: value})
		print r.status_code

		# make response to client
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("OK\n\n")
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
