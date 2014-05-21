#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from pyparsing import *


def _str_strip(s, l, t):
	return t[0].strip() if t is not None and len(t) > 0 else ''


class PyParser(object):
	""" A target-profiles parser leveraging pyparsing.
	"""
	
	# snippets
	snp_begin = CaselessKeyword("Patient") ^ CaselessKeyword("Patient's")
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
	snp_quantity = Group((snp_lte | snp_lt | snp_gte | snp_gt | snp_eq)('delim') + snp_values('value'))
	snp_range = Group(snp_quantity('from') + CaselessKeyword('and') + snp_quantity('to'))
	snp_value = snp_range('range') | snp_quantity('quantity')
	
	# common keywords
	snp_of = CaselessKeyword('of')
	snp_acthist = (CaselessKeyword('historical') | CaselessKeyword('active'))('qualifier')
	snp_within = CaselessKeyword('within') + Group(snp_numeric + snp_units_time)('within')
	snp_end = SkipTo(snp_within | Literal('.') | StringEnd()).setParseAction(_str_strip)
	
	# gender + age
	expr_gender = CaselessKeyword('gender must be') + (CaselessKeyword('female') | CaselessKeyword('male'))('gender')
	expr_age = CaselessKeyword('age must be') + snp_value
	
	# other
	subj_main = Regex(r'must(\s+not)?\s+have').setParseAction(lambda s,l,t: ['not' not in t[0]])('include')
	
	expr_allergy = CaselessKeyword('allergy to') + originalTextFor(snp_main)('allergy')
	
	tail_calc = snp_of + snp_value
	mid_calc = SkipTo(tail_calc).setParseAction(_str_strip)
	expr_calculated = CaselessKeyword('calculated') + mid_calc('calculation') + tail_calc
	expr_measured = CaselessKeyword('measured') + mid_calc('measurement') + tail_calc
	
	expr_diag = snp_acthist + CaselessKeyword('diagnosis') + snp_of + snp_end('diagnosis')
	expr_treat = snp_acthist + CaselessKeyword('procedure') + snp_of + snp_end('procedure')
	expr_proc = snp_acthist + CaselessKeyword('treatment') + snp_of + snp_end('procedure')
	expr_lab = CaselessKeyword('laboratory value') + snp_of + originalTextFor(snp_main)('lab') + snp_value		# no active|historical ?
	
	tail_dc = CaselessKeyword('drug class') + snp_end('prescription_drug_class')
	tail_di = CaselessKeyword('ingredient') + snp_end('prescription_ingredient')
	tail_dm = CaselessKeyword('mechanism of action') + snp_end('prescription_mechanism_of_action')
	expr_drug = snp_acthist + CaselessKeyword('prescription with') + (tail_dc ^ tail_di ^ tail_dm)
	
	# one expression to rule them all
	expr_main = subj_main + Or([expr_allergy, expr_calculated, expr_measured, expr_diag, expr_treat, expr_proc, expr_lab, expr_drug]) + Optional(snp_within)
	main_pattern = snp_begin + Group(Or([expr_gender, expr_age, expr_main]))('condition')
	
	
	def __init__(self, inpath=None):
		self.inpath = inpath
		self.parser = PyParser.main_pattern
	
	
	def parseFile(self):
		""" Parses the receiver's file.
		
		:returns: A JSON encodable structure
		"""
		
		print("Now parse: {}".format(self.inpath))
		return {}
	
	def parseProfile(self, profile):
		""" Parses a complete target profile.
		
		:returns: A list of statements
		"""
		stmts = []
		sentences = re.split("\n+", profile)		# ok for now, should be built into parser
		if sentences and len(sentences) > 0:
			for sentence in sentences:
				stmts.append(self.parseStatement(sentence.strip()))
		return stmts
	
	def parseStatement(self, stmt):
		""" Parses a single target profile statement.
		"""
		
		print(stmt)
		tokens = self.parser.parseString(stmt)
		print(tokens.dump())
		print()
		
		return {}

