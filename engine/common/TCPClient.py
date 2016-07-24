# -*- coding: utf-8 -*-
import socket
import Connection
import sys
import select
import RPCHandler

class TCPClient(object):
	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#sock.setblocking(0)
		self.sock = sock
		self.connection = None
		self.saveFileFlag = False
	
	def connect(self, ip, port):
		try:
			self.sock.connect((ip, port))
			self.connection = Connection.Connection(self.sock, self, RPCHandler.ClientHandler())
			return True
		except:
			import sys
			print sys.exc_info()
			self.sock = None
			return False

	def tick(self, timeout = 0.01):
		if not self.connection:
			return
		inputs = [self.sock]
		outputs = [self.sock]
		try:
			readable, writeable, exceptonal = select.select(inputs, outputs, inputs, timeout)
		except:
			return
		if not (readable or writeable or exceptonal):
			return True

		if readable:
			if not self.connection.receiveData():
				self.close()
				return False

		if writeable and self.connection:
			self.connection.onSendData()

		if exceptonal:
			self.close()
			return False
		return True

	def close(self):
		if self.connection:
			self.connection.close()
			self.connection = None

	def callMethod(self, methodName, paramDict):
		self.connection.rpcHandler.callMethod(methodName, paramDict)

if __name__ == '__main__':
	import sys
	sys.path.append('../../3rdpart')
	client = TCPClient()
	if client.connect('127.0.0.1', 8080):
		print 'connect success'
	else:
		print 'connect failed'
	client.callMethod('echoTest', {'s' : 'hello'})
	while client.tick():
		pass