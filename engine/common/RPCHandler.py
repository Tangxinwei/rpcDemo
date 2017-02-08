# -*- coding: utf-8 -*-
from rpc_decorator import *
import json

class RPCHandler(object):
	def __init__(self):
		self.connection = None

	def setConnection(self, connection):
		self.connection = connection

	def close(self):
		if not self.connection:
			return
		try:
			self.connection.close()
		except:
			pass
		self.connection = None

	def callMethod(self, methodName, paramDict):
		from entity_message_pb2 import EntityMessage
		jsonStr = json.dumps(paramDict)
		message = EntityMessage()
		message.methodName = methodName
		message.paramDict = jsonStr
		self.connection.send(message.SerializeToString())

	def onReceiveData(self, data):
		from entity_message_pb2 import EntityMessage
		message = EntityMessage()
		message.ParseFromString(data)
		func = getattr(self, message.methodName, None)
		if func:
			paramDict = json.loads(message.paramDict)
			func(self, paramDict)

class ServerHandler(RPCHandler):
	@rpc_decorator(Str('s'), )
	def echoTest(self, echoStr):
		print 'receive echo:', echoStr
		self.callMethod('echoTest', {'s' : 'receive data ok'})

class ClientHandler(RPCHandler):
	@rpc_decorator(Str('s'), )
	def echoTest(self, echoStr):
		print 'receive echo:', echoStr
		#self.close()
