# -*- coding: utf-8 -*-
class RecycleIntIdManager(object):
	def __init__(self, maxIndex = 100000):
		self.currentIndex = 0
		self.maxIndex = maxIndex
		self.sparseQueue = []

	def genid(self):
		if self.sparseQueue:
			return self.sparseQueue.pop()
	
		if self.currentIndex >= self.maxIndex:
			self.currentIndex = 0
		self.currentIndex += 1
		return self.currentIndex
	
	def recycle(self, index):
		self.sparseQueue.append(index)