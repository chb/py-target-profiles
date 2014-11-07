#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
from .targetprofile import *


class TargetProfileTest(unittest.TestCase):
	
	def testParsing(self):
		tp = None
		with open('model/targetprofile_test.json', 'r', encoding="UTF-8") as h:
			tp = TargetProfile.load(h)
		self.assertIsNotNone(tp)
		diag_1 = tp.rules[1]
		self.assertIsNotNone(diag_1)
		self.assertIsInstance(diag_1, TargetProfileDiagnosis)
		self.assertIsInstance(diag_1.diagnosis, TargetProfileInputDiagnosis)
		self.assertEqual('snomedct', diag_1.diagnosis.system)
		self.assertEqual('427685000', diag_1.diagnosis.code)
	
