#!/usr/bin/env python
#
# Proportional-allocation systems
#
# These are for proportional representation from votes,
# given some total number of seats
#
# Highest averages:
# D'Hondt, Sainte-Lague, Modified S-L, Huntington-Hill, Imperiali, Danish
#
# Largest remainders:
# Hare, Droop, Imperiali
#
# In these methods, Votes is a list of (party, # votes, initial # seats)
#
# AddInitial(Votes, Initial=0) takes a list of (party, # votes)
# and adds Initial (default 0) seats to each
#
# AddRoundedDown(Votes, Seats) takes a list of (party, # votes)
# and adds the rounded-down proportional number of seats to each
#
# http://en.wikipedia.org/wiki/Highest_averages_method - Highest-averages method
# http://en.wikipedia.org/wiki/D%27Hondt_method - D'Hondt method
# http://en.wikipedia.org/wiki/Sainte-Lagu%C3%AB_method - Sainte-Lague method
# http://en.wikipedia.org/wiki/Huntington-Hill_method - Huntington-Hill method
# http://en.wikipedia.org/wiki/Largest_remainder_method - Largest-remainder method
#

from math import sqrt


# Add constant initial allocation:
# Default is zero
def AddInitial(Votes, Initial=0):
	return [list(Vote[:2]) + [Initial] for Vote in Votes]


# Add the rounded-down number of votes: (total) / (Hare quota),
# where (Hare quota) = (total) / (number of seats)
def AddRoundedDown(Votes, Seats):
	Quota = sum((Vote[1] for Vote in Votes))/float(Seats)
	return [list(Vote[:2]) + [int(Vote[1]/Quota)] for Vote in Votes]

# All methods: shared functions

def SortFinalCompare(a,b):
	# Seats
	rc = - cmp(a[2],b[2])
	if rc != 0: return rc
	# Total votes
	rc = - cmp(a[1],b[1])
	if rc != 0: return rc
	# Party name
	return cmp(a[0],b[0])


# Highest-averages method

# Sort order: highest to lowest
def HASortCompare(a,b):
	# Average
	rc = - cmp(a[3],b[3])
	if rc != 0: return rc
	# Total votes
	rc = - cmp(a[1],b[1])
	if rc != 0: return rc
	# Party name
	return cmp(a[0],b[0])

def HighestAverages(DivisorFunc, Votes, TotalSeats):
	# VList members have party, votes, seats, averages
	VList = [list(Vote[:3]) for Vote in Votes]
	VList = [Vote + [Vote[1]/DivisorFunc(Vote[2])] for Vote in VList]
	RemainingSeats = TotalSeats
	for Vote in VList: RemainingSeats -= Vote[2]
	while RemainingSeats > 0:
		VList.sort(HASortCompare)
		MaxVote = VList[0]
		MaxVote[2] += 1
		MaxVote[3] = MaxVote[1]/float(DivisorFunc(MaxVote[2]))
		RemainingSeats -= 1
	
	VList.sort(SortFinalCompare)
	return [Vote[:3] for Vote in VList]

def DifferentInitial(DivisorFunc, InitialValue, k):
	if k == 0:
		return InitialValue
	else:
		return DivisorFunc(k)

def LinearDivisor(k, d1, d0=1):
	return d0 + d1*k

def DHondtDivisor(k): return LinearDivisor(k,1,1)

def SainteLagueDivisor(k): return LinearDivisor(k,2,1)

def ModifiedSainteLagueDivisor(k):
	return DifferentInitial(SainteLagueDivisor, 1.4, k)

def DanishDivisor(k): return LinearDivisor(k,3,1)

def ImperialiDivisor(k): return LinearDivisor(k,1,2)

def HuntingtonHillDivisor(k): return sqrt(k*(k+1))

def DHondt(Votes, TotalSeats):
	return HighestAverages(DHondtDivisor, Votes, TotalSeats)

def SainteLague(Votes, TotalSeats):
	return HighestAverages(SainteLagueDivisor, Votes, TotalSeats)

def ModifiedSainteLague(Votes, TotalSeats):
	return HighestAverages(ModifiedSainteLagueDivisor, Votes, TotalSeats)

def Imperiali(Votes, TotalSeats):
	return HighestAverages(ImperialiDivisor, Votes, TotalSeats)

def Danish(Votes, TotalSeats):
	return HighestAverages(DanishDivisor, Votes, TotalSeats)

def HuntingtonHill(Votes, TotalSeats):
	return HighestAverages(HuntingtonHillDivisor, Votes, TotalSeats)


# Largest-remainder method

# Sort order: highest to lowest
def LRSortCompare(a,b):
	# Remainder
	rc = - cmp(a[3],b[3])
	if rc != 0: return rc
	# Total votes
	rc = - cmp(a[1],b[1])
	if rc != 0: return rc
	# Party name
	return cmp(a[0],b[0])

def LargestRemainder(QuotaAdjust, Votes, TotalSeats):
	# VList members have party, votes, seats, remainders
	VList = [list(Vote[:3]) for Vote in Votes]
	TotalVote = sum((Vote[1] for Vote in VList))
	Quota = TotalVote/float(TotalSeats + QuotaAdjust)
	
	# Find the remainders
	for Vote in VList:
		Seats = int(Vote[1]/Quota)
		Seats = max(Seats, Vote[2])
		Rmdr = Vote[1] - Quota*Seats
		Vote[2] = Seats
		Vote.append(Rmdr)
	
	RemainingSeats = TotalSeats
	for Vote in VList: RemainingSeats -= Vote[2]
	
	if RemainingSeats < 0:
		# Bump up the quota and try again
		return LargestRemainder(Votes, QuotaAdjust-1, TotalSeats)
	
	VList.sort(LRSortCompare)
	
	# Bump up the number of seats for the parties with the highest remainders
	k = 0
	while RemainingSeats > 0:
		VList[k][2] += 1
		RemainingSeats -= 1
		# Next party; wrap around if necessary
		k += 1
		if k >= len(VList): k = 0
	
	VList.sort(SortFinalCompare)
	return [Vote[:3] for Vote in VList]
	
def LargestRemainderHare(Votes, TotalSeats):
	return LargestRemainder(0, Votes, TotalSeats)
	
def LargestRemainderDroop(Votes, TotalSeats):
	return LargestRemainder(1, Votes, TotalSeats)
	
def LargestRemainderImperiali(Votes, TotalSeats):
	return LargestRemainder(2, Votes, TotalSeats)


# For debugging
if __name__ == "__main__":
	
	# Example from a Wikipedia article
	print "D'Hondt"
	VotesDH = (('A',100), ('B',80), ('C',30), ('D',20))
	print "Target: A:4, B;3, C:1, D:0"
	res = DHondt(AddInitial(VotesDH), 8)
	for r in res: print r
	
	print
	
	# Example from a Wikipedia article
	print "Sainte-Lague"
	VotesSL = (('A',53), ('B',24), ('C',23))
	print "Target: A:3, B:2, C:2"
	res = SainteLague(AddInitial(VotesSL), 7)
	for r in res: print r
	
	print
	
	# Example from the Wikipedia article on highest-averages
	VotesHA = (('Yellow',47000), ('White',16000), ('Red',15900), \
		('Green',12000), ('Blue',6000), ('Pink',3100))
	
	print "D'Hondt"
	print "Target: Yellow:5, White:2, Red:2, Green:1, Blue:0, Pink:0"
	res = DHondt(AddInitial(VotesHA), 10)
	for r in res: print r
	
	print
	
	print "Sainte-Lague"
	print "Target: Yellow:4, White:2, Red:2, Green:1, Blue:1, Pink:0"
	res = SainteLague(AddInitial(VotesHA), 10)
	for r in res: print r
	
	print
	
	print "Modified Sainte-Lague"
	print "Target: Yellow:5, White:2, Red:2, Green:1, Blue:0, Pink:0"
	res = ModifiedSainteLague(AddInitial(VotesHA), 10)
	for r in res: print r
	
	print
	
	print "Imperiali"
	res = Imperiali(AddInitial(VotesHA), 10)
	for r in res: print r
	
	print
	
	print "Danish"
	res = Danish(AddInitial(VotesHA), 10)
	for r in res: print r
	
	print
	
	print "Rounded down, then d'Hondt"
	res = DHondt(AddRoundedDown(VotesHA, 10), 10)
	for r in res: print r
	
	print
	
	# Example from the Wikipedia article on largest-remainder
	VotesLR = (('Yellow',47000), ('White',16000), ('Red',15800), \
		('Green',12000), ('Blue',6100), ('Pink',3100))
	
	print "Highest-Remainder Hare"
	print "Target: Yellow:5, White:2, Red:1, Green:1, Blue:1, Pink:0"
	res = LargestRemainderHare(AddInitial(VotesLR), 10)
	for r in res: print r
	
	print
	
	print "Highest-Remainder Droop"
	res = LargestRemainderDroop(AddInitial(VotesLR), 10)
	print "Target: Yellow:5, White:2, Red:2, Green:1, Blue:0, Pink:0"
	for r in res: print r
	
	print
	
	print "Highest-Remainder Imperiali"
	res = LargestRemainderImperiali(AddInitial(VotesLR), 10)
	for r in res: print r
	
	print
	