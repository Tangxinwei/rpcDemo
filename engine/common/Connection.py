# -*- coding: utf-8 -*-
class Connection(object):
	def __init__(self, sock):
		self.sock = sock
		self.data = ''

	def onReceiveData(self, data):
		pass

	def send(self, data):
		self.sock.send(data)

	def close(self):
		try:
			self.sock.close()
		except:
			pass
		self.sock = None