#!python3
#
# Allocates seats for the European Parliament using different algorithms
# in an attempt to reverse-engineer the algorithm
#
# Returns:
# header line
# list of (name, votes, allocation in each of the algorithms)
#
# D'Hondt 0 -- seat bonus independent of the allocation
# D'Hondt 1 -- seat bonus included as initial counts in the allocation
#
# Apportionment in the European Parliament - Wikipedia
# https://en.wikipedia.org/wiki/Apportionment_in_the_European_Parliament
#

import sys
from PropAlloc import AddInitial, HighestAverages, HA_Divisors

infile = "EU Parliament.txt"
MaxSeats = 96
MinSeats = 6

Members = []
f = open(infile)
for ln in f:
	lnsp = ln.split('\t')
	lnst = [s.strip() for s in lnsp]
	if len(lnst) < 3: continue
	Members.append([lnst[0],int(lnst[1]),int(lnst[2])])

# Calculate the total number of seats from the actual individual numbers:
NumSeats = 0
for m in Members:
	NumSeats += m[2]

indx = {}
for k,ln in enumerate(Members):
	indx[ln[0]] = k


Votes0 = AddInitial(Members,0)
NumSeats0 = NumSeats - MinSeats*len(Votes0)
MaxSeats0 = MaxSeats - MinSeats
res0 = HighestAverages(HA_Divisors["DHondt"], Votes0, NumSeats0, MaxSeats=MaxSeats0)
for r in res0:
	Members[indx[r[0]]].append(r[2]+MinSeats)

Votes1 = AddInitial(Members,MinSeats)
NumSeats1 = NumSeats
MaxSeats1 = MaxSeats
res1 = HighestAverages(HA_Divisors["DHondt"], Votes1, NumSeats1, MaxSeats=MaxSeats1)
for r in res1:
	Members[indx[r[0]]].append(r[2])

print('\t'.join(("Member", "Pop", "Actual", "D'Hondt 0", "D'Hondt 1")))
for ln in Members:
	print('\t'.join([str(s) for s in ln]))