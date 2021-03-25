#!/usr/bin/env python
#
# Allocates seats for the US House of Representatives using different algorithms
#
# Args:
# Input data file (3 columns: state, population, actual Rep count)
# Number of seats
# 1790: 105
# 2010: 435

import sys
import PropAlloc

infile = sys.argv[1]
NSeats = int(sys.argv[2])

d = []
f = open(infile)
for ln in f:
	lnsp = ln.split('\t')
	lnst = [s.strip() for s in lnsp]
	if len(lnst) < 3: continue
	d.append([lnst[0],int(lnst[1]),int(lnst[2])])

indx = {}
for k,ln in enumerate(d):
	indx[ln[0]] = k

Votes = PropAlloc.AddInitial(d,1)

Methods = (PropAlloc.HuntingtonHill, PropAlloc.DHondt, PropAlloc.SainteLague, \
	PropAlloc.Danish, PropAlloc.ModifiedSainteLague, PropAlloc.Imperiali, \
	PropAlloc.LargestRemainderHare, PropAlloc.LargestRemainderDroop, \
	PropAlloc.LargestRemainderImperiali)

for Method in Methods:
	res = Method(Votes,NSeats)
	for r in res:
		d[indx[r[0]]].append(r[2])

print('\t'.join(("State", "Pop", "Actual", "Hunt-Hill", "D'Hondt", "Sainte-Lague", \
	"Danish", "Mod SL", "Imperiali", "LR Hare", "LR Droop", "LR Imperiali")))
for ln in d:
	print('\t'.join([str(s) for s in ln]))