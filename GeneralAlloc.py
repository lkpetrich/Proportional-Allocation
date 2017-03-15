#!/usr/bin/env python
#
# Does various proportional-allocation algorithms
#
# Args:
# Input data file (2 columns: party, votes)
# Number of seats

import sys
import PropAlloc

infile = sys.argv[1]
NSeats = int(sys.argv[2])

d = []
f = open(infile)
for ln in f:
	lnsp = ln.split('\t')
	lnst = [s.strip() for s in lnsp]
	if len(lnst) < 2: continue
	d.append([lnst[0],int(lnst[1])])

indx = {}
for k,ln in enumerate(d):
	indx[ln[0]] = k

Votes0 = PropAlloc.AddInitial(d,0)
Votes1 = PropAlloc.AddInitial(d,1)

Methods = (PropAlloc.HuntingtonHill, PropAlloc.Imperiali, PropAlloc.DHondt, \
	PropAlloc.SainteLague, PropAlloc.Danish, PropAlloc.ModifiedSainteLague, \
	PropAlloc.LargestRemainderHare, PropAlloc.LargestRemainderDroop, \
	PropAlloc.LargestRemainderImperiali)

for Method in Methods:
	if Method == PropAlloc.HuntingtonHill:
		Votes = Votes1
	else:
		Votes = Votes0
	res = Method(Votes,NSeats)
	for r in res:
		d[indx[r[0]]].append(r[2])

for ln in d:
	print '\t'.join([str(s) for s in ln])