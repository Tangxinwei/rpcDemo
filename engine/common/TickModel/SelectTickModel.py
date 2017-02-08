# -*- coding: utf-8 -*-
import socket
import Connection
import sys
import select

class SelectTickModelClient(object):
	def __init__(self, sock, handler_accept = None):
		self.connection = Connection.Connection(sock)
		if handler_accept:
			handler_accept(self.connection)

	def tick(self, timeout = 0.01):
		try:
			sock = self.connection.sock
			readable, writeable, exceptonal = select.select([sock], [sock], [sock], timeout)
		except:
			return False

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

		return True if self.connection else False

	def close(self):
		if self.connection:
			self.connection.close()
			self.connection = None

class SelectTickModel(object):
	def __init__(self, sock, handler_accept = None):
		self.sock = sock
		self.handler_accept = handler_accept
		self.allConnections = {}

		self.inputs = set([self.sock])
		self.outputs = set()

	def removeConnection(self, connection):
		sock = connection.sock
		self.inputs.discard(sock)
		self.outputs.discard(sock)
		del self.allConnections[sock]

	def tick(self, timeout = 0.01):
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
				self.inputs.add(sock)
				connection = Connection.Connection(sock, self)
				self.allConnections[sock] = connection
				if self.handler_accept:
					self.handler_accept(connection)
			else:
				connection = self.allConnections[s]
				if connection.receiveData():
					self.outputs.add(connection.sock)
				else:
					connection.close()

		for s in writeable:
			connection = self.allConnections.get(s)
			if connection:
				if not connection.onSendData():
					connection.close()

		for s in exceptonal:
			connection = self.allConnections.get(s)
			if connection:
				connection.close()


