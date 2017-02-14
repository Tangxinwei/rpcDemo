# -*- coding: utf-8 -*-
import logging
class LogManager(object):
	allLogger = {}
	@classmethod
	def getLogger(cls, name):
		logger = cls.allLogger.get(name)
		if logger:
			return logger
		logger = logging.getLogger(name)
		logger.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		formatter = logging.Formatter(name + '%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')
		ch.setFormatter(formatter)
		logger.addHandler(ch)
		cls.allLogger[name] = logger
		return logger