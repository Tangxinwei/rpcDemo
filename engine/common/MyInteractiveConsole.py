# -*- coding:utf-8 -*-
import code
class MyInteractiveConsole():
	def __init__(self, outputStream, errStream):
		self.outputStream = outputStream
		self.errStream = errStream
		self.interactiveConsole = code.InteractiveConsole()
	
	def push(self, line):
		import sys
		preOut = sys.stdout
		preErr = sys.stderr
		sys.stdout = self.outputStream
		sys.stderr = self.errStream
		flag = self.interactiveConsole.push(line)
		sys.stdout = preOut
		sys.stderr = preErr
		self.errStream.flush()
		self.outputStream.flush()
		return flag

if __name__ == '__main__':
	out = open('out.txt', 'wb')
	err = open('err.txt', 'wb')
	a = MyInteractiveConsole(out, err)
	while True:
		import sys
		sys.stdout.write('>>>')
		s = raw_input()
		if a.push(s):
			pass
		else:
			pass