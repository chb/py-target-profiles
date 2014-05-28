#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from .UMLS.rxnorm import RxNormLookup
from .UMLS.umls import UMLSLookup


class Codifier(object):
	""" Abstract base class for implementations that codify concepts.
	"""
	
	def codifyConcept(self, concept, leaves=True, **kwargs):
		""" Takes a concept name and returns codes describing this concept.
		
		:param str concept: The string name of the concept
		:param bool leaves: Whether or not all leaf concepts (i.e. further
			down in hierarchy) should also be returned
		:returns: A dictionary full of code:name pairs
		"""
		raise Exception('Cannot use abstract Codifier class')


class GlobalCodifier(Codifier):
	""" Decides which Codifier subclass to use for a given job.
	"""
	
	def codifyConcept(self, concept, leaves=True, **kwargs):
		codifier = None
		if 'prescription' == kwargs.get('type'):
			codifier = RxNormCodifier()
		
		if codifier is not None:
			return codifier.codifyConcept(concept, leaves=leaves, **kwargs)
		return None


class RxNormCodifier(Codifier):
	""" Codify drug concepts.
	"""
	
	def __init__(self):
		self.lookup = RxNormLookup()
	
	def codifyConcept(self, concept, leaves=True, **kwargs):
		""" Takes a concept name which is interpreted in the medication realm,
		searches RxNorm for matching entries and returns a dictionary with
		codes and their meaning.
		
		This implementation also looks for a `subtype` parameter which can be:
			- ingredient: the concept is an ingredient
		
		:param str concept: The string name of the concept
		:param bool leaves: Whether or not all leaf concepts (i.e. further
			down in hierarchy) should also be returned
		:returns: A dictionary full of code:name pairs
		"""
		if not concept:
			return None
		
		# get the best concept
		is_ingredient = 'ingredient' == kwargs.get('subtype')
		lim_tty = ['IN'] if is_ingredient else None
		best = self.lookup.rxcui_for_name(concept, lim_tty)
		if not best:
			return None
		
		# walk relations; we want SCD and SBD (and possibly BPCK and GPCK) rxcui concepts
		codes = {}
		if is_ingredient:
			for rxcui, rela in self.lookup.lookup_related(best, relation='ingredient_of'):
				for rxcui2, rela2 in self.lookup.lookup_related(rxcui, relation='constitutes'):
					codes[rxcui2] = self.lookup.lookup_rxcui_name(rxcui2)
		else:
			codes = {best: self.lookup.lookup_rxcui_name(best)}
		
		return codes


class UMLSCodifier(Codifier):
	""" Codify to UMLS concepts.
	"""
	
	def __init__(self):
		self.lookup = UMLSLookup()
	
	def codifyConcept(self, concept, leaves=True, **kwargs):
		raise Exception('Implement UMLSLookup.lookup_code_for_name')

