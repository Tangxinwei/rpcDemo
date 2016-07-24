# -*- coding: utf-8 -*-
import socket
import Connection
import RPCHandler
import sys
import select

class TCPServer(object):
	def __init__(self, ip, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setblocking(0)
		sock.bind((ip, port))
		sock.listen(0)
		self.sock = sock
		self.allConnections = {}

		self.inputs = [self.sock]
		self.outputs = []

	def run(self):
		while True:
			self.tick()

	def tick(self, timeout = 0.001):
		try:
			readable, writeable, exceptonal = select.select(self.inputs, self.outputs, self.inputs, timeout)
		except:
			return
		if not (readable or writeable or exceptonal):
			return

		for s in readable:
			if s is self.sock:
				sock, _ = self.sock.accept()
				sock.setblocking(0)
				self.inputs.append(sock)
				connection = Connection.Connection(sock, self, RPCHandler.ServerHandler())
				connection.isInInput = True
				connection.isInOutput = False
				self.allConnections[sock] = connection
			else:
				connection = self.allConnections[s]
				if connection.receiveData():
					if not connection.isInOutput:
						connection.isInOutput = True
						self.outputs.append(s)
				else:
					if connection.isInInput:
						connection.isInInput = False
						self.inputs.remove(s)
					if connection.isInOutput:
						connection.isInOutput = False
						self.outputs.remove(s)
					del self.allConnections[s]
					connection.close()

		for s in writeable:
			connection = self.allConnections.get(s)
			if connection:
				connection.onSendData()

		for s in exceptonal:
			connection = self.allConnections.get(s)
			if not connection:
				continue
			if connection.isInInput:
				connection.isInInput = False
				self.inputs.remove(s)
			if connection.isInOutput:
				connection.isInOutput = False
				self.outputs.remove(s)
			
			del self.allConnections[s]
			connection.close()

if __name__ == '__main__':
	import sys
	sys.path.append('../../3rdpart')
	server = TCPServer('0.0.0.0', 8080)

	server.run()

