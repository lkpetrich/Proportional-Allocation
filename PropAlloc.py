#!python3
#
# Proportional-allocation systems
#
# These methods are for proportional representation from votes,
# given some total number of seats. These methods may also be used
# for proportional allocation by population.
#
#
# In these methods, Votes is a list of (party, # votes, initial # seats)
#
# AddInitial(Votes, Initial=0) takes a list of (party, # votes)
# and adds Initial (default 0) seats to each
#
# AddRoundedDown(Votes, Seats) takes a list of (party, # votes)
# and adds the rounded-down proportional number of seats to each
#
#
# All these methods are called with (Votes, TotalSeats) unless indicated otherwise
#
#
# Highest averages:
# D'Hondt, Sainte-Lague, Modified S-L, Huntington-Hill, Imperiali, Danish
#
# HighestAverages(DivisorFunc, Votes, TotalSeats)
# Uses a divisor function that returns a divisor for a number of seats
#
# HA_DHondt -- s + 1
# HA_SainteLague -- 2s + 1
# HA_ModifiedSainteLague -- 1.4 if s = 0 else (Sainte-Lague)
# HA_Danish -- 3s + 1
# HA_Imperiali -- s + 2
# HA_HuntingtonHill -- sqrt(s*(s+1))
# for s seats
#
#
# LargestRemainder(QuotaAdjust, Votes, TotalSeats)
# Uses a quota adjustment for the total number of seats
#
# LR_Hare -- 0
# LR_Droop -- 1
# LR_Imperiali -- 2
#
#
# AdjustDivisor(RoundDir, Votes, TotalSeats)
# Uses a roundoff direction (< 0: downward, = 0: nearest, > 0: upward)
#
# Jefferson, Webster, Adams
# AD_Jefferson -- downward (-1)
# AD_Webster -- nearest (0)
# AD_Adams -- upward (1)
#
#
# http://en.wikipedia.org/wiki/Highest_averages_method - Highest-averages method
# http://en.wikipedia.org/wiki/D%27Hondt_method - D'Hondt method
# http://en.wikipedia.org/wiki/Sainte-Lagu%C3%AB_method - Sainte-Lague method
# http://en.wikipedia.org/wiki/Huntington-Hill_method - Huntington-Hill method
# http://en.wikipedia.org/wiki/Largest_remainder_method - Largest-remainder method
# https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_College_Mathematics_for_Everyday_Life_(Inigo_et_al)/09%3A__Apportionment/9.02%3A_Apportionment_-_Jeffersons_Adamss_and_Websters_Methods
# https://www.pnas.org/content/77/1/1 - The Webster method of apportionment
#

from math import sqrt, floor, ceil


# Add constant initial allocation:
# Default is zero
def AddInitial(Votes, Initial=0):
	return [list(Vote[:2]) + [Initial] for Vote in Votes]


# Add the rounded-down number of votes: (total) / (Hare quota),
# where (Hare quota) = (total) / (number of seats)
def AddRoundedDown(Votes, Seats, MaxSeats=None):
	Quota = sum((Vote[1] for Vote in Votes))/float(Seats)
	return [list(Vote[:2]) + [int(Vote[1]/Quota)] for Vote in Votes]

# All methods: shared functions

# For final results, what the functions produce
def SortKeyFinal(a):
	# Seats, total votes, party name
	return (-a[2],-a[1],a[0])


# Highest-averages method

def HighestAverages(DivisorFunc, Votes, TotalSeats, MaxSeats=None):
	IsMax = MaxSeats != None
	
	# VList members have party, votes, seats, averages
	# Adjust for maximum seats if present
	MxStCeil = lambda V: min(V,MaxSeats) if IsMax else V
	VtProc = lambda Vote: [Vote[0], Vote[1], MxStCeil(Vote[2])]
	VList = [VtProc(Vote) for Vote in Votes]
	VList = [Vote + [Vote[1]/DivisorFunc(Vote[2])] for Vote in VList]
	RemainingSeats = TotalSeats
	for Vote in VList: RemainingSeats -= Vote[2]
	
	# Sort order: highest to lowest
	# Average vote, total vote, name
	SortKeyHA = lambda a: (-a[3],-a[1],a[0])
	# Seats available overall?
	while RemainingSeats > 0:
		VList.sort(key=SortKeyHA)
		SeatAvail = False
		for Vote in VList:
			# Don't add a seat if at the individual limit
			if IsMax and Vote[2] >= MaxSeats: continue
			SeatAvail = True
			Vote[2] += 1
			Vote[3] = Vote[1]/float(DivisorFunc(Vote[2]))
			RemainingSeats -= 1
			break
		# No seats could be added
		if not SeatAvail: break
	
	VList.sort(key=SortKeyFinal)
	return [Vote[:3] for Vote in VList]

def DifferentInitial(DivisorFunc, InitialValue, k):
	if k == 0:
		return InitialValue
	else:
		return DivisorFunc(k)

def Divisor_Linear(k, d1, d0=1):
	return d0 + d1*k

def Divisor_DHondt(k): return Divisor_Linear(k,1,1)

def Divisor_SainteLague(k): return Divisor_Linear(k,2,1)

def Divisor_ModifiedSainteLague(k):
	return DifferentInitial(Divisor_SainteLague, 1.4, k)

def Divisor_Danish(k): return Divisor_Linear(k,3,1)

def Divisor_Imperiali(k): return Divisor_Linear(k,1,2)

def Divisor_HuntingtonHill(k): return sqrt(k*(k+1))

def HA_DHondt(Votes, TotalSeats, MaxSeats=None):
	return HighestAverages(Divisor_DHondt, Votes, TotalSeats, MaxSeats)

def HA_SainteLague(Votes, TotalSeats, MaxSeats=None):
	return HighestAverages(Divisor_SainteLague, Votes, TotalSeats, MaxSeats)

def HA_ModifiedSainteLague(Votes, TotalSeats, MaxSeats=None):
	return HighestAverages(Divisor_ModifiedSainteLague, Votes, TotalSeats, MaxSeats)

def HA_Danish(Votes, TotalSeats, MaxSeats=None):
	return HighestAverages(Divisor_Danish, Votes, TotalSeats, MaxSeats)

def HA_Imperiali(Votes, TotalSeats, MaxSeats=None):
	return HighestAverages(Divisor_Imperiali, Votes, TotalSeats, MaxSeats)

def HA_HuntingtonHill(Votes, TotalSeats, MaxSeats=None):
	return HighestAverages(Divisor_HuntingtonHill, Votes, TotalSeats, MaxSeats)


# Largest-remainder method

def LargestRemainder(QuotaAdjust, Votes, TotalSeats, MaxSeats=None):
	IsMax = MaxSeats != None
	
	# VList members have party, votes, seats, remainders
	VList = [list(Vote[:3]) for Vote in Votes]
	TotalVote = sum((Vote[1] for Vote in VList))
	Quota = TotalVote/float(TotalSeats + QuotaAdjust)
	
	# Sort order: highest to lowest
	# Remainder, total, name
	SortKeyLR = lambda a: (-a[3],-a[1],a[0])
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
	
	VList.sort(key=SortKeyLR)
	
	# Bump up the number of seats for the parties with the highest remainders
	k = 0
	while RemainingSeats > 0:
		VList[k][2] += 1
		RemainingSeats -= 1
		# Next party; wrap around if necessary
		k += 1
		if k >= len(VList): k = 0
	
	VList.sort(key=SortKeyFinal)
	return [Vote[:3] for Vote in VList]
	
def LR_Hare(Votes, TotalSeats, MaxSeats=None):
	return LargestRemainder(0, Votes, TotalSeats, MaxSeats)
	
def LR_Droop(Votes, TotalSeats, MaxSeats=None):
	return LargestRemainder(1, Votes, TotalSeats, MaxSeats)
	
def LR_Imperiali(Votes, TotalSeats, MaxSeats=None):
	return LargestRemainder(2, Votes, TotalSeats, MaxSeats)

# Adjusted-divisor method
# Tries divisors until one of them gets the right number of seats
# VList members: name, votes, initial seats, calculated seats
def CountSeatsForDvsr(VList, Dvsr, Rndf):
	AllocSeats = 0
	for Vote in VList:
		Seats = max(Rndf(Vote[1]/Dvsr), Vote[2])
		AllocSeats += Seats
		Vote[3] = Seats
	
	return AllocSeats

def AdjDvsrOutput(VList):
	VLOut = [ [Vote[0], Vote[1], Vote[3]] for Vote in VList]
	VLOut.sort(key=SortKeyFinal)
	return VLOut

def AdjustDivisor(RoundDir, Votes, TotalSeats, MaxSeats=None):
	# Set the rounding function:
	if RoundDir > 0:
		rndf = ceil
	elif RoundDir < 0:
		rndf = floor
	else:
		rndf = round

	# Members have party, votes, initial seats, calculated seats
	VList = [list(Vote[:3]) + [0] for Vote in Votes]
	TotalVotes = 0
	for Vote in VList:
		TotalVotes += Vote[1]
	
	# Find the initial divisor
	Dvsr = float(TotalVotes)/float(TotalSeats)
	DvsrSeats = CountSeatsForDvsr(VList, Dvsr, rndf)
	
	# Find the divisor-value bracket:
	# divisor and number of seats 1 and 2
	# Note: the calculated number of seats decreases with increasing divisor,
	# so Dvsr1 < Dvsr2 and DvsrSeats1 > DvsrSeats2
	if DvsrSeats > TotalSeats:
		Dvsr1 = Dvsr
		DvsrSeats1 = DvsrSeats
		while True:
			Dvsr *= 2
			DvsrSeats = CountSeatsForDvsr(VList, Dvsr, rndf)
			if DvsrSeats == TotalSeats:
				VList.sort(key=SortKeyFinal)
				return VList
			elif DvsrSeats < TotalSeats:
				Dvsr2 = Dvsr
				DvsrSeats2 = DvsrSeats
				break	
	elif DvsrSeats < TotalSeats:
		Dvsr2 = Dvsr
		DvsrSeats2 = DvsrSeats
		while True:
			Dvsr /= 2
			DvsrSeats = CountSeatsForDvsr(VList, Dvsr, rndf)
			if DvsrSeats == TotalSeats:
				VList.sort(key=SortKeyFinal)
				return VList
			elif DvsrSeats > TotalSeats:
				Dvsr1 = Dvsr
				DvsrSeats1 = DvsrSeats
				break
	else: 
		return AdjDvsrOutput(VList)
	
	# Find the next value with linear interpolation
	while True:
		Dvsr = Dvsr1 + (Dvsr2 - Dvsr1) * \
			( float(TotalSeats - DvsrSeats1) / float(DvsrSeats2 - DvsrSeats1) )
		DvsrSeats = CountSeatsForDvsr(VList, Dvsr, rndf)
		
		# Interval too small?
		if abs(Dvsr2 - Dvsr1)/(Dvsr1 + Dvsr2) < 1e-8:
			return AdjDvsrOutput(VList)
		
		if DvsrSeats > TotalSeats:
			# Dvsr too small
			# Replace the lower bound
			Dvsr1 = Dvsr
			DvsrSeats1 = DvsrSeats
		elif DvsrSeats < TotalSeats:
			# Dvsr too large
			# Replace the upper bound
			Dvsr2 = Dvsr
			DvsrSeats = DvsrSeats
		else:
			return AdjDvsrOutput(VList)


def AD_Jefferson(Votes, TotalSeats, MaxSeats=None):
	return AdjustDivisor(-1, Votes, TotalSeats, MaxSeats)

def AD_Webster(Votes, TotalSeats, MaxSeats=None):
	return AdjustDivisor(0, Votes, TotalSeats, MaxSeats)

def AD_Adams(Votes, TotalSeats, MaxSeats=None):
	return AdjustDivisor(1, Votes, TotalSeats, MaxSeats)

# For debugging
if __name__ == "__main__":
	
	# Example from a Wikipedia article
	print("Highest-Averages D'Hondt")
	VotesDH = (('A',100), ('B',80), ('C',30), ('D',20))
	print("Target: A:4, B;3, C:1, D:0")
	res = HA_DHondt(AddInitial(VotesDH), 8)
	for r in res: print(r)
	
	print
	
	# Example from a Wikipedia article
	print("Highest-Averages Sainte-Lague")
	VotesSL = (('A',53), ('B',24), ('C',23))
	print("Target: A:3, B:2, C:2")
	res = HA_SainteLague(AddInitial(VotesSL), 7)
	for r in res: print(r)
	
	print
	
	# Example from the Wikipedia article on highest-averages
	VotesHA = (('Yellow',47000), ('White',16000), ('Red',15900), \
		('Green',12000), ('Blue',6000), ('Pink',3100))
	
	print("Highest-Averages D'Hondt")
	print("Target: Yellow:5, White:2, Red:2, Green:1, Blue:0, Pink:0")
	res = HA_DHondt(AddInitial(VotesHA), 10)
	for r in res: print(r)
	
	print
	
	print("Highest-Averages Sainte-Lague")
	print("Target: Yellow:4, White:2, Red:2, Green:1, Blue:1, Pink:0")
	res = HA_SainteLague(AddInitial(VotesHA), 10)
	for r in res: print(r)
	
	print
	
	print("Highest-Averages Modified Sainte-Lague")
	print("Target: Yellow:5, White:2, Red:2, Green:1, Blue:0, Pink:0")
	res = HA_ModifiedSainteLague(AddInitial(VotesHA), 10)
	for r in res: print(r)
	
	print
	
	print("Highest-Averages Imperiali")
	res = HA_Imperiali(AddInitial(VotesHA), 10)
	for r in res: print(r)
	
	print
	
	print("Highest-Averages Danish")
	res = HA_Danish(AddInitial(VotesHA), 10)
	for r in res: print(r)
	
	print
	
	print("Rounded down, then d'Hondt")
	res = HA_DHondt(AddRoundedDown(VotesHA, 10), 10)
	for r in res: print(r)
	
	print("Adjusted-Divisor Jefferson")
	res = AD_Jefferson(AddInitial(VotesHA), 10)
	for r in res: print(r)
	
	print
	
	print("Adjusted-Divisor Webster")
	res = AD_Webster(AddInitial(VotesHA), 10)
	for r in res: print(r)
	
	print
	
	print("Adjusted-Divisor Adams")
	res = AD_Adams(AddInitial(VotesHA), 10)
	for r in res: print(r)
	
	print
	
	# Example from the Wikipedia article on largest-remainder
	VotesLR = (('Yellow',47000), ('White',16000), ('Red',15800), \
		('Green',12000), ('Blue',6100), ('Pink',3100))
	
	print("Largest-Remainder Hare")
	print("Target: Yellow:5, White:2, Red:1, Green:1, Blue:1, Pink:0")
	res = LR_Hare(AddInitial(VotesLR), 10)
	for r in res: print(r)
	
	print
	
	print("Largest-Remainder Droop")
	res = LR_Droop(AddInitial(VotesLR), 10)
	print("Target: Yellow:5, White:2, Red:2, Green:1, Blue:0, Pink:0")
	for r in res: print(r)
	
	print
	
	print("Largest-Remainder Imperiali")
	res = LR_Imperiali(AddInitial(VotesLR), 10)
	for r in res: print(r)
	
	print
	