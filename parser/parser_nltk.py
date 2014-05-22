#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import nltk


class Parser(object):
	""" A target-profiles parser.
	"""
	
	grammar = r'''
		MUST:
			{<MD><RB>?<VB>}
		NBAR:
			{<NN.*|JJ>*<NUM>*<NN.*>+}  # Nouns and Adjectives, terminated with Nouns
		
		NP:
			{<NBAR>}			# An NBAR is also a NP
			{<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
	'''
	
	# define components
	comp_quant = r'(([\d\.]+)\s*(.+))'
	comp_quali = r'(<=|<|>=|>|=|less than|greater than|at most|at least|no less than|no more than|exactly)'
	comp_value = r'({} {})'.format(comp_quali, comp_quant)
	
	# gender
	spec_gender = r'(male|female)'
	
	proc_treat_diag = '((historical|active) (procedure|treatment|diagnosis) of)'
	diagnosis = '((historical|active) diagnosis of)'
	presc = '(active prescription (of|(with drug class)))'
	allergy = '(allergy to)'
	
	pattern_tokenizer = r'Patient(\'s)?|\s*(gender must be)|\s*(age must be)|\s*(must( not)? have)|\s*({})|\s*({})|.+'.format(proc_treat_diag, comp_value)
	pattern_tagger = [
		(r'^Patient(\'s)?', 'SUBJ'),
		(r'\s*gender must', 'GEND'),
		(r'\s*age must', 'AGE'),
		(r'\s*must have', 'MUSTHAVE'),
		(r'\s*must not have', 'MUSTNOT'),
		
		(r'.*', '-')
	]
	
	def __init__(self, inpath=None):
		self.inpath = inpath
		# self.chunker = nltk.RegexpParser(Parser.grammar)
		self.tokenizer = nltk.RegexpTokenizer(Parser.pattern_tokenizer, flags=re.VERBOSE)
		self.tagger = nltk.RegexpTagger(Parser.pattern_tagger)
	
	
	def parseFile(self):
		""" Parses the receiver's file.
		
		:returns: A JSON encodable structure, never None
		"""
		
		print("Now parse: {}".format(self.inpath))
		return {}
	
	def parseProfile(self, profile):
		""" Parses a complete target profile.
		"""
		return {}
	
	def parseStatement(self, stmt):
		""" Parses a single target profile statement.
		"""
		sentences = nltk.sent_tokenize(stmt)
		if sentences and len(sentences) > 0:
			for sentence in sentences:
				print(sentence)
				tokens = self.tokenizer.tokenize(sentence)
				# tokens = nltk.word_tokenize(sentence)
				print("Tokens: {}".format(tokens))
				# tagged = nltk.pos_tag(tokens)
				# print("Tagged: {}".format(tagged))
				# tree = self.chunker.parse(tagged)
				# print("Tree:   {}".format(tree))
				tags = self.tagger.tag(tokens)
				print("Tags:   {}".format(tags))
				print()
		
		return {}
	
	def _tokenize(self, text, pattern):
		""" Tokenize the given text with the given pattern.
		"""
		pass
	
