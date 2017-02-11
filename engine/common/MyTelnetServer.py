# -*- coding:utf-8 -*-
from telnetsrv.threaded import TelnetHandler, command
import SocketServer
import MyInteractiveConsole
import io
import code
import sys

class MyTelnetHandler(TelnetHandler):
	# What prompt to display
	PROMPT = ">>>"
	# What prompt to use for requesting more input
	CONTINUE_PROMPT = "..."
	def __init__(self, request, client_address, server):
		self.interactiveConsole = code.InteractiveConsole()
		TelnetHandler.__init__(self, request, client_address, server)
		
	def handler_input_line(self, line):
		if line == 'quit' or line == 'exit':
			self.cmdEXIT(None)
			return True

		outputStream = io.BytesIO()
		errStream = io.BytesIO()
		preOut = sys.stdout
		preErr = sys.stderr
		sys.stdout = outputStream
		sys.stderr = errStream
		if self.interactiveConsole.push(line):
			self.write(outputStream.getvalue())
			self.write(errStream.getvalue())
			if self.DOECHO:
				self.write(self.CONTINUE_PROMPT)
		else:
			self.write(outputStream.getvalue())
			self.write(errStream.getvalue())
			if self.DOECHO:
				self.write(self.PROMPT)
		sys.stdout = preOut
		sys.stderr = preErr
		return True

class MyTelnetServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	allow_reuse_address = True

if __name__ == '__main__':
	import sys
	sys.path.append('../../3rdpart')
	server = MyTelnetServer(('0.0.0.0', 8080), MyTelnetHandler)
	server.serve_forever()