#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
from .parser_pyparsing import PyParser


_profile_1 = """```Return all```"""
_result_1 = "Return all"

_profile_2 = """Here's a profile:
```
Patient must have profile
Patient must not have no profile
```
Here's some more text
"""
_result_2 = """
Patient must have profile
Patient must not have no profile
"""

_profile_3 = """Here's a profile:
```
Patient must have profile
```

Some text in between, then the profile continues:
```
Patient must not have no profile
```
Here's some more text."""
_result_3 = """
Patient must have profile

Patient must not have no profile
"""


class PyParserTest(unittest.TestCase):
	
	def testFormat(self):
		p = PyParser()
		found = p.findProfileContent(_profile_1)
		self.assertEqual(_result_1, found)
		
		found = p.findProfileContent(_profile_2)
		self.assertEqual(_result_2, found)
		
		found = p.findProfileContent(_profile_3)
		self.assertEqual(_result_3, found)
		
