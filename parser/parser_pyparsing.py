#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from pyparsing import *


def _str_strip(s, l, t):
	""" Strip token whitespace. """
	return t[0].strip() if t is not None and len(t) > 0 else ''

def _within(s, l, t):
	""" Return ISO-8601 representation for durations. """
	return "P{}{}".format(round(t[0][0]), t[0][1][:1].upper())


class PyParser(object):
	""" A target-profiles parser leveraging pyparsing.
	"""
	
	# snippets
	snp_begin = CaselessKeyword("Patient") ^ CaselessKeyword("Patient's")
	snp_must = Regex(r'must(\s+not)?\s+have').setParseAction(lambda s,l,t: ['not' not in t[0]])('include')
	snp_main = Group(OneOrMore(Word(alphanums + "/'\"-_")))
	
	# numbers, units and ranges
	snp_numeric = Combine(Word(nums) + Optional('.' + Word(nums))).setParseAction(lambda s,l,t: [ float(t[0]) ])
	snp_lt = (CaselessKeyword('<') ^ CaselessKeyword('less than')).setParseAction(replaceWith('lt'))
	snp_lte = (CaselessKeyword('<=') ^ CaselessKeyword('at most') ^ CaselessKeyword('no more than')).setParseAction(replaceWith('lte'))
	snp_gt = (CaselessKeyword('>') ^ CaselessKeyword('greater than')).setParseAction(replaceWith('gt'))
	snp_gte = (CaselessKeyword('>=') ^ CaselessKeyword('at least') ^ CaselessKeyword('no less than')).setParseAction(replaceWith('gte'))
	snp_eq = (CaselessKeyword('=') ^ CaselessKeyword('exactly')).setParseAction(replaceWith('eq'))
	
	snp_units = Word(alphas, alphanums + '%/^')
	snp_units_time = Or([CaselessKeyword('years'), CaselessKeyword('months')])
	snp_values = Group(snp_numeric('number') + Optional(snp_units)('unit'))
	snp_quantity = Group((snp_lte | snp_lt | snp_gte | snp_gt | snp_eq)('comparator') + snp_values('value'))
	snp_range = Group(snp_quantity('from') + CaselessKeyword('and') + snp_quantity('to'))
	snp_value = snp_range('range') | snp_quantity('quantity')
	
	# common keywords
	snp_of = CaselessKeyword('of')
	snp_acthist = (CaselessKeyword('historical') | CaselessKeyword('active'))('qualifier')
	snp_within = CaselessKeyword('within past') + Group(snp_numeric + snp_units_time).setParseAction(_within)('within')
	snp_end = SkipTo(snp_within | Literal('.') | StringEnd()).setParseAction(_str_strip)
	
	# gender + age
	expr_gender = CaselessKeyword('gender must be') + (CaselessKeyword('female') | CaselessKeyword('male'))('gender')
	expr_age = CaselessKeyword('age must be') + snp_value('age')
	
	# expressions
	expr_allergy = CaselessKeyword('allergy to') + originalTextFor(snp_main)('allergy')
	
	tail_calc = snp_of + snp_value
	mid_calc = SkipTo(tail_calc).setParseAction(_str_strip)
	expr_calculated = CaselessKeyword('calculated') + mid_calc('calculation') + tail_calc
	expr_measured = CaselessKeyword('measured') + mid_calc('measurement') + tail_calc
	
	expr_diag = snp_acthist + CaselessKeyword('diagnosis') + snp_of + snp_end('diagnosis')
	expr_treat = snp_acthist + CaselessKeyword('procedure') + snp_of + snp_end('procedure')
	expr_proc = snp_acthist + CaselessKeyword('treatment') + snp_of + snp_end('procedure')
	expr_lab = CaselessKeyword('laboratory value') + snp_of + originalTextFor(snp_main)('lab') + snp_value		# no active|historical ?
	
	tail_dc = CaselessKeyword('drug class') + snp_end('prescription:drug_class')
	tail_di = CaselessKeyword('ingredient') + snp_end('prescription:ingredient')
	tail_dm = CaselessKeyword('mechanism of action') + snp_end('prescription:mechanism_of_action')
	expr_drug = snp_acthist + CaselessKeyword('prescription with') + (tail_dc ^ tail_di ^ tail_dm)
	
	# one expression to rule them all
	expr_main = snp_must + Or([expr_allergy, expr_calculated, expr_measured, expr_diag, expr_treat, expr_proc, expr_lab, expr_drug]) + Optional(snp_within)
	main_pattern = snp_begin + Group(Or([expr_gender, expr_age, expr_main]))('condition')
	
	
	def __init__(self, inpath=None):
		self.inpath = inpath
		self.parser = PyParser.main_pattern
	
	
	def parseFile(self):
		""" Parses the receiver's file.
		
		:returns: A JSON encodable target profile
		"""
		with open(self.inpath, 'r') as handle:
			raw = handle.read()
		return self.parseProfile(raw)
	
	def parseProfile(self, profile):
		""" Parses a complete target profile.
		
		Still missing:
		  - converting the "within" specification to ISO-8601
		  - if-else support
		
		:returns: A list of statements
		"""
		stmts = []
		for tok, start, end in self.parser.scanString(profile):
			#print("{}\n\n".format(tok.dump()))		# DEBUG
			res = self._jsonPropertiesFromToken(tok)
			res['description'] = profile[start:end]
			stmts.append(res)
		
		return stmts
	
	def parseStatement(self, stmt):
		""" Parses a single target profile statement, raising an Exception if
		it doesn't validate.
		"""
		
		tokens = self.parser.parseString(stmt)
		print(tokens.dump())
		print()
		
		return tokens
		
	def _jsonPropertiesFromToken(self, token):
		""" Checks which subject key has been found in the token and returns an
		appropriate dictionary.
		"""
		cond = token.condition
		res = {
			'include': cond.include,
		}
		
		# extract type, special handling for "age" (will get range or quantity later) and "gender"
		if 'age' in cond:
			res['type'] = 'age'
			res['include'] = True
		elif 'gender' in cond:
			res['type'] = 'gender'
			res['value'] = cond.gender
			res['include'] = True
		else:
			for sub in ['diagnosis', 'procedure', 'calculation', 'lab', 'allergy', 'prescription:drug_class', 'prescription:ingredient', 'prescription:mechanism_of_action']:
				if sub in cond:
					res['type'] = sub
					res['value'] = cond[sub]
		
		# extract ranges and quantities
		if 'range' in cond:
			res['range'] = self._jsonForRange(cond.range)
		if 'quantity' in cond:
			res['quantity'] = self._jsonForQuantity(cond.quantity)
		
		# qualifiers
		if cond.qualifier:
			res['qualifier'] = cond.qualifier
		if cond.within:
			res['within'] = cond.within
		
		return res
	
	def _jsonForQuantity(self, token):
		""" Returns JSON for a token that must represent a quantity.
		"""
		if not token:
			return None
		
		d = {
			'number': token.value.number,
			'unit': token.value.unit
		}
		if token.comparator:
			d['comparator'] = token.comparator
		return d
	
	def _jsonForRange(self, token):
		""" Returns JSON for a token that must represent a range.
		"""
		if not token:
			return None
		
		return {
			'from': self._jsonForQuantity(token['from']),
			'to': self._jsonForQuantity(token.to)
		}

