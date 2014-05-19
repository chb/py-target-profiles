#!/usr/bin/python3
# -*- coding: utf-8 -*-



class Parser(object):
	""" A target-profiles parser.
	"""
	
	def __init__(self, inpath):
		self.inpath = inpath
	
	
	def parse(self):
		""" Parses the receiver's file.
		
		:returns: A JSON encodable structure, never None
		"""
		
		print("Now parse: {}".format(self.inpath))
		return {}
	
