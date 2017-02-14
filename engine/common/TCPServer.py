# -*- coding: utf-8 -*-
import RPCHandler
from TickModel import SelectTickModel
import socket

class TCPServer(object):
	def __init__(self, ip, port, handler_accept = None, handler_close = None):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setblocking(0)
		sock.bind((ip, port))
		sock.listen(0)
		self.tickModel = SelectTickModel.SelectTickModel(sock, handler_accept, handler_close)

	def run(self):
		while True:
			self.tick()

	def tick(self, timeout = 0.01):
		self.tickModel.tick(timeout)

if __name__ == '__main__':
	import sys
	sys.path.append('../../3rdpart')
	server = TCPServer('0.0.0.0', 8080, lambda connection: connection.setRpcHandler(RPCHandler.ServerHandler()))
	server.run()

