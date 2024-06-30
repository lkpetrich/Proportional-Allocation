#!python3
#
# Does various proportional-allocation algorithms
#
# Args:
# Input data file (2 columns: name, votes)
# Number of seats
# Returns:
# header line
# list of (name, votes, allocation in each of the algorithms)

import sys
from PropAlloc import HighestAverages, HA_Divisors, AddInitial
from PropAlloc import LargestRemainders, LR_QuotaAdjust
from PropAlloc import AdjustDivisor, AD_Rounding

infile = sys.argv[1]
NumSeats = int(sys.argv[2])

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

MethodList = (
	("HA Adams", \
		lambda v, n: HighestAverages(HA_Divisors["Adams"], AddInitial(v,1), n)),
	("HA Dean", \
		lambda v, n: HighestAverages(HA_Divisors["Dean"], AddInitial(v,1), n)),
	("HA Hunt-Hill", \
		lambda v, n: HighestAverages(HA_Divisors["HuntingtonHill"], AddInitial(v,1), n)),
	("HA Danish", \
		lambda v, n: HighestAverages(HA_Divisors["SainteLague"], AddInitial(v), n)),
	("HA Sainte-Lague", \
		lambda v, n: HighestAverages(HA_Divisors["SainteLague"], AddInitial(v), n)),
	("HA Modified SL", \
		lambda v, n: HighestAverages(HA_Divisors["ModifiedSainteLague"], AddInitial(v), n)),
	("HA SquareMean", \
		lambda v, n: HighestAverages(HA_Divisors["SquareMean"], AddInitial(v), n)),
	("HA D'Hondt", \
		lambda v, n: HighestAverages(HA_Divisors["DHondt"], AddInitial(v), n)),
	("HA Imperiali", \
		lambda v, n: HighestAverages(HA_Divisors["Imperiali"], AddInitial(v), n)),
	("LR Hare", \
		lambda v, n: LargestRemainders(LR_QuotaAdjust["Hare"], v, n)),
	("LR Droop", \
		lambda v, n: LargestRemainders(LR_QuotaAdjust["Droop"], v, n)),
	("LR Imperiali", \
		lambda v, n: LargestRemainders(LR_QuotaAdjust["Imperiali"], v, n)),
	("AD Jefferson", \
		lambda v, n: AdjustDivisor(AD_Rounding["Jefferson"], v, n)),
	("AD Webster", \
		lambda v, n: AdjustDivisor(AD_Rounding["Webster"], v, n)),
	("AD Adams", \
		lambda v, n: AdjustDivisor(AD_Rounding["Adams"], v, n)),
)

Names = ["Party", "Votes"]
for Name, Method in MethodList:
	Names.append(Name)
	res = Method(d,NumSeats)
	for r in res:
		d[indx[r[0]]].append(r[2])

print('\t'.join(Names))
for ln in d:
	print('\t'.join([str(s) for s in ln]))