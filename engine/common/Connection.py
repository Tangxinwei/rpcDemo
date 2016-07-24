# -*- coding: utf-8 -*-
import struct

class Connection(object):
	def __init__(self, sock, owner, rpcHandler):
		self.sock = sock
		self.data = ''
		self.validDataLen = -1
		self.curDataLen = 0
		self.owner = owner
		self.realSendData = ''
		self.rpcHandler = rpcHandler
		rpcHandler.setConnection(self)

	def receiveData(self):
		data = self.sock.recv(1024)
		if not data:
			return False
		self.onReceiveData(data)
		return True

	def onReceiveData(self, data):
		if not self.owner:
			return
		
		self.data += data
		self.curDataLen += len(data)
		data = self.onCheckData()
		while data is not None:
			if self.rpcHandler:
				self.rpcHandler.onReceiveData(data)
			data = self.onCheckData()
		
	def onCheckData(self):
		if self.validDataLen == -1 and self.curDataLen >= 4:
			self.validDataLen = struct.unpack('<I', self.data[0:4])[0]
			self.data = self.data[4:]
			self.curDataLen -= 4
		
		if self.validDataLen != -1 and self.validDataLen <= self.curDataLen:
			data = self.data[0:self.validDataLen]
			self.data = self.data[self.validDataLen:]
			self.curDataLen -= self.validDataLen
			self.validDataLen = -1
			return data
		return None

	def send(self, data):
		self.realSendData += struct.pack('<I', len(data)) + data

	def onSendData(self):
		if self.sock:
			sendLen = self.sock.send(self.realSendData)
			self.realSendData = self.realSendData[sendLen:]
		

	def close(self):
		if not self.sock:
			return
		try:
			self.sock.close()
			self.owner = None
		except:
			pass
		finally:
			self.rpcHandler.setConnection(None)
			self.sock = None