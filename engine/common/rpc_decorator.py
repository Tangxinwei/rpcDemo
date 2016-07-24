# -*- coding: utf-8 -*-
class RPCParams(object):
	def __init__(self, key, default):
		self.key = key
		self.default = default

	def getValue(self, initDict):
		return initDict.get(self.key, self.default)

class Int(RPCParams):
	def __init__(self, key, default = 0):
		super(Int, self).__init__(key, default)

class Str(RPCParams):
	def __init__(self, key, default = ''):
		super(Str, self).__init__(key, default)

class List(RPCParams):
	def __init__(self, key, default = []):
		super(List, self).__init__(key, default)

class Dict(RPCParams):
	def __init__(self, key, default = {}):
		super(Dict, self).__init__(key, default)

class rpcCall(object):
	def __init__(self, func, argParams):
		self.realFunc = func
		self.argParams = argParams

	def __call__(self, entity, callDict):
		try:
			params = []
			for argParam in self.argParams:
				params.append(argParam.getValue(callDict))
			self.realFunc(entity, *params)
		except:
			import traceback
			traceback.print_exc()


def rpc_decorator(*args):
	def innerFunc(func):
		return rpcCall(func, args)
	return innerFunc