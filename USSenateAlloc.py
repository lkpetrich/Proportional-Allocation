#!python3
#
# Allocates seats for the US Senate
#
# Args:
# Input data file (3 columns: state, population, actual/estimated Rep count)

import sys
from PropAlloc import HighestAverages, HA_Divisors, AddInitial

if len(sys.argv) <= 1:
	print("Needs:")
	print("US-state data file: (name, population, actual/estimated Rep count)")
	print("(optional) average number of Senators per state (default: 2)")
	print("(optional) maximum number of Senators per state (default: no limit)")
	sys.exit()
infile = sys.argv[1]
RelNumSeats = int(sys.argv[2]) if len(sys.argv) > 2 else 2
MaxSeats = int(sys.argv[3]) if len(sys.argv) > 3 else None


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


NumSeats = RelNumSeats*len(States)
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
	print(n,' '.join(StatesPerNum[n]))
