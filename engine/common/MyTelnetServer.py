# -*- coding:utf-8 -*-
from telnetsrv.threaded import TelnetHandler, command
import SocketServer
class MyTelnetHandler(TelnetHandler):
	def handler_input_line(self, line):
		print line
		return True

class TelnetServer(SocketServer.TCPServer):
	allow_reuse_address = True

if __name__ == '__main__':
	import sys
	sys.path.append('../../3rdpart')
	server = TelnetServer(('0.0.0.0', 8080), MyTelnetHandler)
	server.serve_forever()