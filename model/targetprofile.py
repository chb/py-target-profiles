#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json


class TargetProfile(object):
	""" Class representing one target profile.
	"""
	rule_classes = {}
	
	@classmethod
	def register(cls, klass):
		""" Register a TargetProfileRule to handle rules of a given type.
		"""
		if klass is None:
			raise Exception("I need a class")
		for_type = klass.for_type
		if not for_type:
			raise Exception("I need a class with a type name")
		if for_type in cls.rule_classes:		# could check if class is different to fail gracefully on double-imports
			raise Exception("I have already registered {} for {}".format(cls.rule_classes[for_type]), for_type)
		cls.rule_classes[for_type] = klass
	
	
	def __init__(self, json_arr):
		self.rules = []
		if json_arr is not None:
			if not isinstance(json_arr, list):
				raise Exception("Only supporting JSON formats whose root is a list, is {}".format(type(json_arr)))
			for js in json_arr:
				klass = self.__class__.rule_classes.get(js.get('type')) or TargetProfileRule
				self.rules.append(klass(js))
	
	
	# Mark: Parsing
	
	@classmethod
	def load(cls, json_handle):
		""" Load a target profile from a file handle pointing at a JSON file.
		"""
		return cls(json.load(json_handle))
	
	@classmethod
	def loads(cls, json_string):
		""" Load a target profile from a JSON string.
		"""
		return cls(json.loads(json_string))


class TargetProfileRule(object):
	""" Abstract base class for target profile model representations.
	"""
	for_type = None
	
	def __init__(self, json_dict):
		self.type = None
		self.description = None
		self.include = True
		
		if json_dict is not None:
			self.type = json_dict.get('type')
			self.description = json_dict.get('description')
			self.include = json_dict.get('include')
	

class TargetProfilePatientState(TargetProfileRule):
	""" Describe a patient's state.
	"""
	for_type = 'state'


class TargetProfileAge(TargetProfileRule):
	""" Limit a patient's age.
	"""
	for_type = 'age'


class TargetProfileDiagnosis(TargetProfileRule):
	""" Require or exclude based on a diagnosis.
	"""
	for_type = 'diagnosis'
	
	def __init__(self, json_dict):
		super().__init__(json_dict)
		self.diagnosis = None
		
		if json_dict is not None:
			inp_1 = json_dict['inputs'][0] if json_dict.get('inputs') and len(json_dict['inputs']) > 0 else None
			if inp_1 is not None:
				self.diagnosis = TargetProfileInputDiagnosis(inp_1)


class TargetProfileMeasurement(TargetProfileRule):
	""" Describe or exclude a patient metric.
	"""
	for_type = 'measurement'


class TargetProfileAllergy(TargetProfileRule):
	""" Handle allergies.
	"""
	for_type = 'allergy'


class TargetProfileMedicalScore(TargetProfileRule):
	""" Handle medical scores.
	"""
	for_type = 'score'


TargetProfile.register(TargetProfilePatientState)
TargetProfile.register(TargetProfileAge)
TargetProfile.register(TargetProfileDiagnosis)
TargetProfile.register(TargetProfileMeasurement)
TargetProfile.register(TargetProfileAllergy)
TargetProfile.register(TargetProfileMedicalScore)


class TargetProfileInput(object):
	""" Superclass for all input objects of a target profile criterion.
	The JSON representation for these is still in flux, so this will change
	A LOT.
	"""
	def __init__(self, json_dict):
		self.description = json_dict.get('description') if json_dict is not None else None
	

class TargetProfileInputDiagnosis(TargetProfileInput):
	def __init__(self, json_dict):
		super().__init__(json_dict)
		self.system = json_dict.get('system') if json_dict is not None else None
		self.code  = json_dict.get('code') if json_dict is not None else None

