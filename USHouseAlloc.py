#!python3
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

Methods = (PropAlloc.HA_HuntingtonHill, PropAlloc.HA_DHondt, PropAlloc.HA_SainteLague, \
	PropAlloc.HA_Danish, PropAlloc.HA_ModifiedSainteLague, PropAlloc.HA_Imperiali, \
	PropAlloc.LR_Hare, PropAlloc.LR_Droop, \
	PropAlloc.LR_Imperiali, PropAlloc.AD_Jefferson, \
	PropAlloc.AD_Webster, PropAlloc.AD_Adams)

for Method in Methods:
	res = Method(Votes,NSeats)
	for r in res:
		d[indx[r[0]]].append(r[2])

print('\t'.join(("State", "Pop", "Actual", "Hunt-Hill", "D'Hondt", "Sainte-Lague", \
	"Danish", "Mod SL", "Imperiali", "LR Hare", "LR Droop", "LR Imperiali", \
	"AD Jefferson", "AD Webster", "AD Adams")))
for ln in d:
	print('\t'.join([str(s) for s in ln]))