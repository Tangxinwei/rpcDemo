# -*- coding: utf-8 -*-
import socket
import Connection
import sys
import select

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
			self.connection = Connection.Connection(self.sock, self)
			return True
		except:
			import sys
			print sys.exc_info()
			self.sock = None
			return False

	def tick(self):
		if not self.connection:
			return
		inputs = [self.sock]
		outputs = [self.sock]
		readable, writeable, exceptonal = select.select(inputs, outputs, inputs, 0.01)
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

	def onReceiveData(self, connection, data):
		pass

	def close(self):
		if self.connection:
			self.connection.close()
			self.connection = None

if __name__ == '__main__':
	client = TCPClient()
	if client.connect('127.0.0.1', 8080):
		print 'connect success'
	else:
		print 'connect failed'
	while client.tick():
		pass