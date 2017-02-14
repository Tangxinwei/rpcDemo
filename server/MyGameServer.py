# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.join('..', 'engine'))
sys.path.append(os.path.join('..', '3rdpart'))
from common.rpc_decorator import *
from gameserver import GameServerBase
class ServerEntity(GameServerBase.ServerEntityRpcHandler):
	def __init__(self):
		super(ServerEntity, self).__init__()
	@rpc_decorator(Str('s'), )
	def echoTest(self, echoStr):
		print 'receive echo:', echoStr
		self.callMethod('echoTest', {'s' : 'receive data ok'})

class MyGameServer(GameServerBase.GameServerBase):
	def _doSetEntityClass(self):
		self.entityClass = ServerEntity

if __name__ == '__main__':
	gameServer = MyGameServer('0.0.0.0', 8080)
	gameServer.run()

