# -*- coding: utf-8 -*-
from common import RPCHandler
from common import TCPServer
from common import LogManager
import ServerRepo
import logging
from common import MyTelnetServer
import thread
class ServerEntityRpcHandler(RPCHandler.RPCHandler):
	logger = LogManager.LogManager.getLogger('ServerEntity')
	def __init__(self):
		super(ServerEntityRpcHandler, self).__init__()

class GameServerBase(object):
	logger = LogManager.LogManager.getLogger('GameServerBase')
	def __init__(self, ip, port):
		ServerRepo.gameServer = self
		self._doSetEntityClass()
		self.tcpServer = TCPServer.TCPServer(ip, port, self.handler_new_connection, self.handler_close_connection)
		self.logger.info('telnet server start (%s:%s)' % (ip, port + 100))
		self.telnetServer = MyTelnetServer.MyTelnetServer((ip, port + 100), MyTelnetServer.MyTelnetHandler)
		thread.start_new_thread(self.telnetServer.serve_forever, ())

	def _doSetEntityClass(self):
		self.entityClass = None

	def handler_new_connection(self, connection):
		self.logger.info('handler_new_connection')
		connection.setRpcHandler(self.entityClass())

	def handler_close_connection(self, connection):
		self.logger.info('handler_close_connection')
		serverEntityRpcHandler = connection.rpcHandler

	def run(self):
		while True:
			self.tcpServer.tick()

