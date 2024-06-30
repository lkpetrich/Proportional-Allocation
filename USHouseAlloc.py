#!python3
#
# Allocates seats for the US House of Representatives using different algorithms
#
# Args:
# Input data file (3 columns: state, population, actual/estimated Rep count)
# Number of seats (optional: default is actual count)
# Maximum number of seats per state (optional: default is none)
# Returns:
# header line
# list of (name, votes, allocation in each of the algorithms)
#
# Actual numbers of seats:
# 1790: House 105 Senate 30
# 2020: House 435 Senate 100

import sys
from PropAlloc import HighestAverages, HA_Divisors, AddInitial
from PropAlloc import LargestRemainders, LR_QuotaAdjust
from PropAlloc import AdjustDivisor, AD_Rounding

if len(sys.argv) <= 1:
	print("Needs a US-state data file: (name, population, actual/estimated Rep count)")
	sys.exit()
infile = sys.argv[1]
NumSeats = int(sys.argv[2]) if len(sys.argv) > 2 else None
MaxSeats = int(sys.argv[3]) if len(sys.argv) > 3 else None

States = []
f = open(infile)
for ln in f:
	lnsp = ln.split('\t')
	lnst = [s.strip() for s in lnsp]
	if len(lnst) < 3: continue
	States.append([lnst[0],int(lnst[1]),int(lnst[2])])

if NumSeats == None:
	NumSeats = 0
	for st in States: NumSeats += st[2]

Votes = [st[:2] for st in States]

indx = {}
for k,ln in enumerate(States):
	indx[ln[0]] = k

MethodList = (
	("HA Hunt-Hill", \
		lambda v, n, m: HighestAverages(HA_Divisors["HuntingtonHill"], \
			AddInitial(v,1), n, MaxSeats=m)),
	("HA Sainte-Lague", \
		lambda v, n, m: HighestAverages(HA_Divisors["SainteLague"], \
			AddInitial(v,1), n, MaxSeats=m)),
	("HA D'Hondt", \
		lambda v, n, m: HighestAverages(HA_Divisors["DHondt"], \
			AddInitial(v,1), n, MaxSeats=m)),
	("LR Hamilton", \
		lambda v, n, m: LargestRemainders(LR_QuotaAdjust["Hare"], \
			v, n, MinSeats=1, MaxSeats=m)),
	("AD Jefferson", \
		lambda v, n, m: AdjustDivisor(AD_Rounding["Jefferson"], \
			v, n, MinSeats=1, MaxSeats=m)),
	("AD Webster", \
		lambda v, n, m: AdjustDivisor(AD_Rounding["Webster"], \
			v, n, MinSeats=1, MaxSeats=m)),
	("AD Adams", \
		lambda v, n, m: AdjustDivisor(AD_Rounding["Adams"], \
			v, n, MinSeats=1, MaxSeats=m))
)

MethodNames = []
for MethodName, Method in MethodList:
	MethodNames.append(MethodName)
	res = Method(Votes,NumSeats,MaxSeats)
	for r in res:
		States[indx[r[0]]].append(r[2])

print('\t'.join(["State", "Pop", "Actual"] + MethodNames))
for st in States:
	print('\t'.join([str(s) for s in st]))