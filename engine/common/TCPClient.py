# -*- coding: utf-8 -*-
import RPCHandler
from TickModel import SelectTickModel
import socket

class TCPClient(object):
	def connect(self, ip, port, handler_accept = None):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((ip, port))
			self.tickModel = SelectTickModel.SelectTickModelClient(sock, handler_accept)
			return True
		except:
			import sys
			print sys.exc_info()
		return False

	def tick(self, timeout = 0.01):
		if not self.tickModel.tick(timeout):
			self.close()
			return False
		return True
		
	def close(self):
		if self.tickModel:
			self.tickModel.close()
			self.tickModel = None

	def callMethod(self, methodName, paramDict):
		self.tickModel.connection.rpcHandler.callMethod(methodName, paramDict)

if __name__ == '__main__':
	import sys
	sys.path.append('../../3rdpart')
	client = TCPClient()
	if client.connect('127.0.0.1', 8080, lambda connection: connection.setRpcHandler(RPCHandler.ClientHandler())):
		print 'connect success'
	else:
		print 'connect failed'
	client.callMethod('echoTest', {'s' : 'hello'})
	while client.tick():
		pass