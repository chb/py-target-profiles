#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from codifier.codifier import GlobalCodifier


def codify(inpath, outpath):
	""" Codifies the given JSON-formatted input file and writes the result to
	the given outpath.
	"""
	profile = None
	with open(inpath, 'r') as h:
		profile = json.load(h)
	
	# codify all conditions found in the profile
	i = 1
	globe = GlobalCodifier()
	for condition in profile:
		print('-->  Codifying {} of {}'.format(i, len(profile)))
		codes = globe.codifyConcept(
			condition.get('value'),
			type=condition.get('type'),
			subtype=condition.get('subtype')
		)
		if codes is not None and len(codes) > 0:
			condition['codes'] = codes
		i += 1
	
	# write
	with open(outpath, 'w') as h:
		json.dump(profile, h, indent=4)
	print('->  Written to {}'.format(outpath))


if '__main__' == __name__:
	codify('output/NCTsamples.json', 'output/NCTsamples-codified.json')
