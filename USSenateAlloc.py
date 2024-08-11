#!python3
#
# Allocates seats for the US Senate
#
# Args:
# Input data file (3 columns: state, population, actual/estimated Rep count)

import sys
from PropAlloc import HighestAverages, HA_Divisors, AddInitial

if len(sys.argv) <= 1:
	print("Needs a US-state data file: (name, population, actual/estimated Rep count)")
	sys.exit()
infile = sys.argv[1]


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
# since that is used by the House

def DumpRes(NumSeats, MaxSeats=None):
	res = HighestAverages(HA_Divisors["HuntingtonHill"], \
		AddInitial(States,1), NumSeats, MaxSeats=MaxSeats)
	StatesPerNum = {}
	for r in res:
		if r[2] not in StatesPerNum:
			StatesPerNum[r[2]] = []
		StatesPerNum[r[2]].append(NameToAbbrev[r[0]])
	
	for n in StatesPerNum:
		StatesPerNum[n].sort()
	
	for n in sorted(StatesPerNum.keys(),reverse=True):
		print(n,StatesPerNum[n])

DumpRes(2*len(States))
print()
DumpRes(2*len(States),4)