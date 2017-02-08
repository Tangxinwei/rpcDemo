# -*- coding: utf-8 -*-
import struct

class Connection(object):
	def __init__(self, sock, owner = None):
		self.sock = sock
		self.data = ''
		self.validDataLen = -1
		self.curDataLen = 0
		self.realSendData = ''
		self.rpcHandler = None
		self.owner = owner

	def setRpcHandler(self, rpcHandler):
		self.rpcHandler = rpcHandler
		rpcHandler.setConnection(self)

	def receiveData(self):
		try:
			data = self.sock.recv(1024)
		except:
			return False
		if not data:
			return False
		self.onReceiveData(data)
		return True

	def onReceiveData(self, data):
		if not self.sock:
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
		try:
			sendLen = self.sock.send(self.realSendData)
			self.realSendData = self.realSendData[sendLen:]
		except:
			return False
		return True

	def close(self):
		if not self.sock:
			return
		try:
			self.sock.close()
		except:
			pass
		finally:
			if self.owner:
				self.owner.removeConnection(self)
				
			if self.rpcHandler:
				self.rpcHandler.setConnection(None)
				self.rpcHandler = None
			self.sock = None
			self.owner = None