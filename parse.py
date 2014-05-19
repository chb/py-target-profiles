#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from parser.parser import Parser


def parse(inpath, outpath):
	""" Parses the target profile at the given inpath and writes JSON to the
	given outpath.
	"""
	parser = Parser(inpath)
	
	# parse profile
	print('-->  Parsing {}'.format(inpath))
	try:
		parsed = parser.parse()
	except Exception as e:
		print('xx>  Failed to parse {}: {}'.format(inpath, e))
		return
	
	# write JSON
	with open(outpath, 'w') as h:
		json.dump(parsed, h)
	print('-->  Written to {}'.format(outpath))


def main(outdir):
	""" Parses all target profiles found in the submodule and puts the JSON
	representations into the directory specified by `outdir`.
	"""
	for subdir, dirs, files in os.walk('target-profiles/target-profiles'):
		for company in dirs:
			for sbdr, drs, fls in os.walk(os.path.join(subdir, company)):
				for f in fls:
					if 'NCT' == f[:3] and '.md' == f[-3:]:
						outpath = os.path.join(outdir, f.replace('.md', '.json'))
						parse(os.path.join(sbdr, f), outpath)


if '__main__' == __name__:
	outdir = 'output'
	if not os.path.isdir(outdir):
		os.mkdir(outdir)
	
	main(outdir)
