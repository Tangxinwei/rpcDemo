# -*- coding: utf-8 -*-
import libevent
import socket
import Connection
import sys
import IdManager

class TCPServer(object):
	def __init__(self, ip, port, maxClient = 0):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((ip, port))
		sock.setblocking(0)
		sock.listen(maxClient)
		base = libevent.Base()
		event = libevent.Event(base, sock.fileno(), libevent.EV_READ | libevent.EV_PERSIST, self.onAccept, None)
		event.add(-1)
		self.sock = sock
		self.event = event
		self.base = base
		self.allConnections = {}
		self.allTimer = {}
		self.timerIdGen = IdManager.RecycleIntIdManager()

	def onTimerTimeOut(self, _, timerId):
		try:
			timer, func, args = self.allTimer[timerId]
			del self.allTimer[timerId]
			self.timerIdGen.recycle(timerId)
			func(*args)
		except:
			sys.excepthook(*sys.exc_info())

	def delayExec(self, delayTime, func, *args):
		timerId = self.timerIdGen.genid()
		timer = libevent.Timer(self.base, self.onTimerTimeOut, timerId)
		timer.add(delayTime)
		self.allTimer[timerId] = (timer, func, args)

	def delayExecRepeat(self, delayTime, func, *args):
		def onTimeOut():
			if func(*args):
				self.delayExec(delayTime, onTimeOut)
		self.delayExec(delayTime, onTimeOut)

	def run(self):
		self.base.dispatch()

	def deleteConnection(self, fileno):
		if fileno in self.allConnections:
			connection, event = self.allConnections[fileno]
			del self.allConnections[fileno]
			connection.close()
			event.delete()

	def onAccept(self, event, fileno, eventNumber, userData):
		clientSock, _ = self.sock.accept()
		clientSock.setblocking(0)
		connection = Connection.Connection(clientSock)
		clientEvent = libevent.Event(self.base, clientSock.fileno(), libevent.EV_READ | libevent.EV_TIMEOUT | libevent.EV_PERSIST,\
			self.onClientDataReceive, connection)
		clientEvent.add(-1)
		self.allConnections[clientSock.fileno()] = (connection, clientEvent)
	

	def onClientDataReceive(self, event, fileno, eventNumber, connection):
		if eventNumber == libevent.EV_TIMEOUT:
			self.deleteConnection(fileno)
		else:
			data = ''
			while True:
				ndata = ''
				try:
					ndata = connection.sock.recv(4096)
				except:
					pass
				if not ndata:
					break
				data += ndata
			if not data:
				self.deleteConnection(fileno)
			else:
				connection.onReceiveData(data)
				connection.send(data)

if __name__ == '__main__':
	import time
	def fun():
		print 'exec', time.time()
		return True
	server = TCPServer('0.0.0.0', 14002)
	server.delayExecRepeat(0.01, fun)
	print time.time()
	server.run()

