#!python3
#
# Allocates seats for the US Senate
#
# Args:
# Input data file (3 columns: state, population, actual/estimated Rep count)

import sys
from math import sqrt
from PropAlloc import HighestAverages, HA_Divisors, AddInitial

if len(sys.argv) <= 1:
	print("Needs:")
	print("US-state data file: (name, population, actual/estimated Rep count)")
	print("(optional) algorithm code: 0 (1: sqr(HH), -1: sqrt(pops))")
	print("(optional) average number of Senators per state (default: 2)")
	print("(optional) maximum number of Senators per state (default: no limit)")
	sys.exit()

argn = 1
infile = sys.argv[argn]
argn += 1
AlgoCode = int(sys.argv[argn]) if len(sys.argv) > argn else 0
argn += 1
RelNumSeats = int(sys.argv[argn]) if len(sys.argv) > argn else 2
argn += 1
MaxSeats = int(sys.argv[argn]) if len(sys.argv) > argn else None


# The data on states
States = []
with open(infile) as f:
	for ln in f:
		lnsp = ln.split('\t')
		lnst = [s.strip() for s in lnsp]
		if len(lnst) < 3: continue
		States.append([lnst[0],int(lnst[1]),int(lnst[2])])


# Abbreviations of the states
stfile = "USStateAbbrevs.txt"
StAbbrevs = []
with open(stfile) as f:
	for ln in f:
		lnsp = ln.split('\t')
		lnst = [s.strip() for s in lnsp]
		if len(lnst) < 2: continue
		StAbbrevs.append(lnst)

# Full name to abbreviation
NameToAbbrev = {}
for st, ab in StAbbrevs:
	NameToAbbrev[st] = ab

# Will bake Huntington-Hill into the code,
# since that is used by the House.

# Use the square of that divisor if selected
def HHSquare(s): return s*(s+1)
dvsrf = HHSquare if AlgoCode > 0 else HA_Divisors["HuntingtonHill"]

# Use the square root of the populations if selected
if AlgoCode < 0:
	for k in range(len(States)):
		States[k][1] = sqrt(1.*States[k][1])

NumSeats = RelNumSeats*len(States)
res = HighestAverages(dvsrf, AddInitial(States,1), NumSeats, MaxSeats=MaxSeats)
StatesPerNum = {}
for r in res:
	if r[2] not in StatesPerNum:
		StatesPerNum[r[2]] = []
	StatesPerNum[r[2]].append(NameToAbbrev[r[0]])

for n in StatesPerNum:
	StatesPerNum[n].sort()

for n in sorted(StatesPerNum.keys(),reverse=True):
	print(n,' '.join(StatesPerNum[n]))
