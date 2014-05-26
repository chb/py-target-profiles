#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
from .codifier import Codifier, RxNormCodifier


class RxNormCodifierTest(unittest.TestCase):
	
	def testAbstract(self):
		cod = Codifier()
		with self.assertRaises(Exception):
			cod.codifyConcept('concept')
	
	def testInsulin(self):
		rxn = RxNormCodifier()
		codes = rxn.codifyConcept('insulin', subtype='ingredient')
		
		self.assertGreater(len(codes), 50)		# currently 53
		self.assertIsNotNone(codes['847205'])
		self.assertIsNotNone(codes['412453'])
		self.assertIsNotNone(codes['108814'])
		self.assertIsNotNone(codes['213442'])
		self.assertIsNotNone(codes['247512'])
		self.assertIsNotNone(codes['106892'])
		self.assertIsNotNone(codes['847257'])
		self.assertIsNotNone(codes['108822'])
	
	def testDoxazosin(self):
		rxn = RxNormCodifier()
		codes = rxn.codifyConcept('doxazosin', subtype='ingredient')
		
		self.assertGreater(len(codes), 15)		# currently 16
		self.assertIsNotNone(codes['104367'])
		self.assertIsNotNone(codes['197626'])
		self.assertIsNotNone(codes['197628'])
		self.assertIsNotNone(codes['205544'])
		self.assertIsNotNone(codes['389131'])
		self.assertIsNotNone(codes['389166'])
		self.assertIsNotNone(codes['636360'])
		self.assertIsNotNone(codes['1242404'])
		
