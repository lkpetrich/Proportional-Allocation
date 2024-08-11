#!python3
#
# Proportional-allocation systems
#
# These methods are for proportional representation from votes,
# given some total number of seats. These methods may also be used
# for proportional allocation by population.
#
#
# In these methods, Votes is a list of
#   (party, # votes)
# For highest averages, one needs initial numbers of seats:
#   (party, # votes, # initial seats)
#
# For highest averages, these are two convenience functions
# for the initial number of seats:
#
# AddInitial(Votes, Initial=0)
# and adds Initial (default 0) seats to each party
#
# AddRoundedDown(Votes, TotalSeats, MinSeats, MaxSeats)
# and adds the rounded-down proportional number of seats to each
#
# Also in these methods,
#   TotalSeats is the total number of seats to fill
#   MinSeats is each party's minimum number of seats: specified as MinSeats=(value)
#   MaxSeats is each party's maximum number of seats: specified as MaxSeats=(value)
#
# Minimum and maximum values were implemented to make possible "degressive proportionality"
# https://en.wikipedia.org/wiki/Degressive_proportionality
# avoiding too little or too much representation for each party or region.
#
#
# The methods' output is a list of
#   (party, # votes, # seats, direction relative to minimum and maximum, if present)
# That direction:
# -1: too small and forced to minimum, 0: unforced, +1: too large and forced to maximum
#
# Highest averages methods:
#
# HighestAverages(DivisorFunc, Votes, TotalSeats, MaxSeats)
# Uses a divisor function that returns a divisor for a number of seats
#
# HA_Divisors: an associative array
#   Key: name of the divisor function
#   Value: the divisor funcion
# Key (name) -- value (function) of number of seats s
# Adams, Cambridge -- s
# Danish -- s + 1/3
# Webster, SainteLague -- s + 1/2
# ModifiedSainteLague -- 1.4 if s = 0 else (Sainte-Lague)
# Hill, HuntingtonHill -- sqrt(s*(s+1))
# SquareMean -- sqrt(s*(s+1) + 1/2)
# Dean -- s*(s+1)/(s + 1/2)
# Jefferson, DHondt -- s + 1
# Imperiali -- s + 2
#
#
# LargestRemainder(QuotaAdjust, Votes, TotalSeats, MinSeats, MaxSeats)
# LargestRemainders( (same args) )
# Uses a quota adjustment for the total number of seats
# 
#
# LR_QuotaAdjust: an associative array
#   Key: name, Value: quota-adjustment value
# Hamilton, Hare -- 0
# Droop -- 1
# Imperiali -- 2
#
#
# AdjustDivisor(RoundDir, Votes, TotalSeats, MinSeats, MaxSeats)
# AdjustedDivisor( (same args) )
# Uses a roundoff direction (< 0: downward, = 0: nearest, > 0: upward)
#
# AD_Rounding: an associative array
#   Key: name, Value: rounding direction
# Jefferson -- downward (-1)
# Webster -- nearest (0)
# Adams -- upward (1)
#
# Examples is a collection of examples from these Wikipedia articles
# and various referenced articles
#
# http://en.wikipedia.org/wiki/Highest_averages_method - Highest-averages method
# http://en.wikipedia.org/wiki/D%27Hondt_method - D'Hondt method
# http://en.wikipedia.org/wiki/Sainte-Lagu%C3%AB_method - Sainte-Lague method
# http://en.wikipedia.org/wiki/Huntington-Hill_method - Huntington-Hill method
#
# http://en.wikipedia.org/wiki/Largest_remainder_method - Largest-remainder method
#
# Adjusted divisor:
# https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_College_Mathematics_for_Everyday_Life_(Inigo_et_al)/09%3A__Apportionment/9.02%3A_Apportionment_-_Jeffersons_Adamss_and_Websters_Methods
# https://www.pnas.org/content/77/1/1 - The Webster method of apportionment
#

from math import sqrt, floor, ceil


# Add constant initial allocation:
# Default is zero
def AddInitial(Votes, Initial=0):
	return [list(Vote[:2]) + [Initial, 0] for Vote in Votes]


# Add the rounded-down number of votes: (total) / (Hare quota),
# where (Hare quota) = (total) / (number of seats)
def AddRoundedDown(Votes, TotalSeats, *, MinSeats=None, MaxSeats=None):
	IsMin = MinSeats != None
	IsMax = MaxSeats != None
	
	VList = [list(Vote[:2]) + [0, 0] for Vote in Votes]
	
	while True:
		# Count up the votes and the seats for all parties
		# not forced to the minimum or maximum numbers of seats
		VoteSum = 0
		SeatSum = TotalSeats
		for Vote in VList:
			if Vote[3] == 0:
				VoteSum += Vote[1]
			else:
				SeatSum -= Vote[2]
		if SeatSum <= 0: break
		
		Quota = float(VoteSum)/float(SeatSum)
		WentOutOfRange = False
		
		for Vote in VList:
			if Vote[3] == 0:
				IndNumSeats = int(Vote[1]/Quota)
				if IsMin and IndNumSeats < MinSeats:
					WentOutOfRange = True
					IndNumSeats = MinSeats
					Vote[3] = -1
				elif IsMax and IndNumSeats > MaxSeats:
					WentOutOfRange = True
					IndNumSeats = MaxSeats
					Vote[3] = 1
				Vote[2] = IndNumSeats
		
		if not WentOutOfRange: break
	
	return VList

# All methods: shared functions

# For final results, what the functions produce
def SortKeyFinal(a):
	# Seats, total votes, party name
	return (-a[2],-a[1],a[0])


# Highest-averages method

def HighestAverages(DivisorFunc, Votes, TotalSeats, *, MaxSeats=None):
	IsMax = MaxSeats != None
	
	# VList members have party, votes, seats, direction, averages
	VList = [list(Vote[:3]) + [0, 0] for Vote in Votes]
	
	for Vote in VList:
		if IsMax and Vote[2] > MaxSeats:
			Vote[2] = MaxSeats
			Vote[3] = 1
	
	# Available seats
	RemainingSeats = TotalSeats
	for Vote in VList:
		if Vote[3] == 0:
			Vote[4] = Vote[1]/float(DivisorFunc(Vote[2]))
		RemainingSeats -= Vote[2]
	
	if RemainingSeats <= 0:
		return [Vote[:4] for Vote in sorted(VList,key=SortKeyFinal)]
	
	# Any seats remaining?
	while RemainingSeats > 0:
		# Find the highest average by index
		ix = None
		HighAvg = None
		for k, Vote in enumerate(VList):
			if Vote[3] == 0:
				if ix == None:
					ix = k
					HighAvg = Vote[4]
				elif Vote[4] > HighAvg:
					ix = k
					HighAvg = Vote[4]
		
		# All out of range?
		if ix == None: break
		
		# The winner...
		Vote = VList[ix]
		# More than the maximum?
		if IsMax and Vote[2] >= MaxSeats:
			Vote[2] = MaxSeats
			Vote[3] = 1
		else:
			# If not, then a seat to the winner
			Vote[2] += 1
			RemainingSeats -= 1
			Vote[4] = Vote[1]/float(DivisorFunc(Vote[2]))
	
	return [Vote[:4] for Vote in sorted(VList,key=SortKeyFinal)]


def DifferentInitial(DivisorFunc, InitialValue, k):
	if k == 0:
		return InitialValue
	else:
		return DivisorFunc(k)

HA_Divisors = {}

HA_Divisors["Adams"] = lambda k: k + 0.
HA_Divisors["Cambridge"] = HA_Divisors["Adams"]

third = 1./3.
HA_Divisors["Danish"] = lambda k: k + third

HA_Divisors["SainteLague"] = lambda k: k + 0.5
HA_Divisors["Webster"] = HA_Divisors["SainteLague"]

HA_Divisors["ModifiedSainteLague"] = lambda k: \
	DifferentInitial(HA_Divisors["SainteLague"], 1.4, k)

HA_Divisors["HuntingtonHill"] = lambda k: sqrt(k*(k+1.))
HA_Divisors["Hill"] = HA_Divisors["HuntingtonHill"]

HA_Divisors["SquareMean"] = lambda k: sqrt(k*(k+1.) + 0.5)
HA_Divisors["Dean"] = lambda k: k*(k+1.)/(k + 0.5)

HA_Divisors["DHondt"] = lambda k: k + 1.
HA_Divisors["Jefferson"] = HA_Divisors["DHondt"]

HA_Divisors["Imperiali"] = lambda k: k + 1.


# Largest-remainder method

def LargestRemainder(QuotaAdjust, Votes, TotalSeats, *, MinSeats=None, MaxSeats=None):
	IsMin = MinSeats != None
	IsMax = MaxSeats != None
	
	# VList members have party, votes, seats, direction, remainders
	VList = [list(Vote[:2]) + [0, 0, 0] for Vote in Votes]
	
	RemainingSeats = 0
	
	SortKey = lambda a: (-a[4],-a[1],a[0])
	
	while True:
		# Count up the votes and the seats for all parties
		# not forced to the minimum or maximum numbers of seats
		VoteSum = 0
		SeatSum = TotalSeats
		for Vote in VList:
			if Vote[3] == 0:
				VoteSum += Vote[1]
			else:
				SeatSum -= Vote[2]
		if SeatSum <= 0: break
		
		Quota = float(VoteSum)/float(SeatSum + QuotaAdjust)
		WentOutOfRange = False
		
		for Vote in VList:
			if Vote[3] == 0:
				IndNumSeats = int(Vote[1]/Quota)
				if IsMin and IndNumSeats < MinSeats:
					WentOutOfRange = True
					IndNumSeats = MinSeats
					Vote[3] = -1
					Vote[4] = 0
				elif IsMax and IndNumSeats > MaxSeats:
					WentOutOfRange = True
					IndNumSeats = MaxSeats
					Vote[3] = 1
					Vote[4] = 0
				else:
					Vote[4] = Vote[1] - Quota*IndNumSeats
				Vote[2] = IndNumSeats
		
		VList.sort(key=SortKey)
		
		RemainingSeats = SeatSum
		for Vote in VList:
			if Vote[3] == 0:
				RemainingSeats -= Vote[2]
		if RemainingSeats < 0: break
		
		for Vote in VList:
			if Vote[3] == 0:
				if RemainingSeats == 0: break
				if IsMax and Vote[2] >= MaxSeats:
					WentOutOfRange = True
					Vote[2] = MaxSeats
					Vote[3] = 1
					Vote[4] = 0
				else:
					Vote[2] += 1
					RemainingSeats -= 1
		
		if not WentOutOfRange: break
	
	if RemainingSeats < 0:
		return LargestRemainder(QuotaAdjust-1, Votes, TotalSeats, \
			MinSeats=MinSeats, MaxSeats=MaxSeats)
	
	return [Vote[:4] for Vote in sorted(VList,key=SortKeyFinal)]


def LargestRemainders(*args, **kwargs):
	return LargestRemainder(*args, **kwargs)

LR_QuotaAdjust = {"Hamilton": 0, "Hare": 0, "Droop": 1, "Imperiali": 2}


# Adjusted-divisor method
# Tries divisors until one of them gets the right number of seats
# VList members: name, votes, seats, direction
def CountSeatsForDvsr(VList, Dvsr, Rndf, MinSeats, MaxSeats):
	IsMin = MinSeats != None
	IsMax = MaxSeats != None
	
	AllocSeats = 0
	for Vote in VList:
		Seats = Rndf(Vote[1]/Dvsr)
		if IsMin and Seats < MinSeats:
			Seats = MinSeats
			Vote[3] = -1
		elif IsMax and Seats > MaxSeats:
			Seats = MaxSeats
			Vote[3] = 1
		else:
			Vote[3] = 0
		Vote[2] = Seats
		AllocSeats += Seats
	
	return AllocSeats

def AdjustDivisor(RoundDir, Votes, TotalSeats, *, MinSeats=None, MaxSeats=None):
	IsMin = MinSeats != None
	IsMax = MaxSeats != None
	
	# Set the rounding function:
	if RoundDir > 0:
		rndf = ceil
	elif RoundDir < 0:
		rndf = floor
	else:
		rndf = round

	# Members have party, votes, seats, direction
	VList = [list(Vote[:2]) + [0, 0] for Vote in Votes]
	
	# Find the initial divisor
	TotalVotes = 0
	for Vote in VList:
		TotalVotes += Vote[1]
	Dvsr = float(TotalVotes)/float(TotalSeats)
	DvsrSeats = CountSeatsForDvsr(VList, Dvsr, rndf, MinSeats, MaxSeats)
	
	# Find the divisor-value bracket:
	# divisor and number of seats 1 and 2
	# Note: the calculated number of seats decreases with increasing divisor,
	# so Dvsr1 < Dvsr2 and DvsrSeats1 > DvsrSeats2
	if DvsrSeats > TotalSeats:
		Dvsr1 = Dvsr
		DvsrSeats1 = DvsrSeats
		while True:
			Dvsr *= 2
			DvsrSeats = CountSeatsForDvsr(VList, Dvsr, rndf, MinSeats, MaxSeats)
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
			DvsrSeats = CountSeatsForDvsr(VList, Dvsr, rndf, MinSeats, MaxSeats)
			if DvsrSeats == TotalSeats:
				VList.sort(key=SortKeyFinal)
				return VList
			elif DvsrSeats > TotalSeats:
				Dvsr1 = Dvsr
				DvsrSeats1 = DvsrSeats
				break
	else:
		VList.sort(key=SortKeyFinal)
		return VList
	
	# Find the next value with linear interpolation
	while True:
		Dvsr = Dvsr1 + (Dvsr2 - Dvsr1) * \
			( float(TotalSeats - DvsrSeats1) / float(DvsrSeats2 - DvsrSeats1) )
		DvsrSeats = CountSeatsForDvsr(VList, Dvsr, rndf, MinSeats, MaxSeats)
		
		# Interval too small?
		if abs(Dvsr2 - Dvsr1)/(Dvsr1 + Dvsr2) < 1e-8:
			VList.sort(key=SortKeyFinal)
			return VList
		
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
			VList.sort(key=SortKeyFinal)
			return VList

def AdjustedDivisor(*args, **kwargs):
	return AdjustDivisor(*args, **kwargs)

AD_Rounding = {"Jefferson": -1, "Webster": 0, "Adams": 1}


# Examples
Examples = {}

ExampleTargets = {}

# From Wikipedia's Highest-Averages article

# Original: Jefferson, Webster
Examples["WikiHA11"] = (("Yellow", 46_000), ("White", 25_000), ("Red", 12_210), \
	("Green", 8_350), ("Purple", 8_340))

ExampleTargets["WikiHA11"] = (21, {"HA-DHondt": (11,6,2,1,1), \
	"HA-SainteLague": (9,5,3,2,2) } )

# Original: Adams, Webster
Examples["WikiHA12"] = (("Yellow", 55_000), ("White", 17_290), ("Red", 16_600), \
	("Green", 5_560), ("Purple", 5_550))

ExampleTargets["WikiHA12"] = (21, {"HA-Adams": (10,4,3,2,2), \
	"HA-SainteLague": (11,4,4,1,1) } )

# Original: Jefferson, Webster, Huntington-Hill, Adams
Examples["WikiHA13"] = (("Yellow", 47_000), ("White", 16_000), ("Red", 15_900), \
	("Green", 12_000), ("Blue", 6,000), ("Pink", 3_100))

ExampleTargets["WikiHA13"] = (10, {"HA-DHondt": (5,2,2,1,0,0), \
	"HA-SainteLague": (4,2,2,1,1,0), "HA-HuntingtonHill": (4,2,1,1,1,1), \
	"HA-Adams": (3,2,2,1,1,1) } )

# From Wikipedia's D'Hondt and Sainte-Lague articles
Examples["WikiHA2"] = (('A',100_000), ('B',80_000), ('C',30_000), ('D',20_000))

ExampleTargets["WikiHA2"] = (8, \
	{"HA-DHondt": (4,3,1,0), "HA-SainteLague": (3,3,1,1) } )

# From Wikipedia's Huntington-Hill article
Examples["WikiHA3"] = (('A',100_000), ('B',80_000), ('C',30_000))

ExampleTargets["WikiHA3"] = (8, {"HA-HuntingtonHill": (4,3,1) } )

# Israel's Knesset, 2015 election of 20th one
Examples["WikiHAKn"] = (("Likud",985_408), ("Zionist Union",786_313), \
	("Joint List",446_583), ("Yesh Atid",371_602), ("Kulanu",315_360), \
	("The Jewish Home",283_910), ("Shas",241_613), ("Yisrael Beiteinu",214_906), \
	("United Torah Judaism",210_143), ("Meretz",165_529))

ExampleTargets["WikiHAKn"] = (120, {"HA-HuntingtonHill": (30,24,13,11,9,9,7,6,6,5), \
	"HA-DHondt": (30,24,13,11,10,8,7,6,6,5) } )

# From Wikipedia's largest-remainders article
Examples["WikiLR1"] = (("Yellow",47_000), ("White",16_000), ("Red",15_800), \
		("Green",12_000), ("Blue",6_100), ("Pink",3_100))

ExampleTargets["WikiLR1"] = (10, {"LR-Droop": (5, 2, 2, 1, 0, 0) } )

Examples["WikiLR2"] = (('A',1500), ('B',1500), ('C',900), ('D',500), \
	('E',500), ('F',200))

ExampleTargets["WikiLR21"] = (25, {"LR-Hare": (7,7,4,3,3,1) } )

ExampleTargets["WikiLR22"] = (26, {"LR-Hare": (8,8,5,2,2,1) } )


# For debugging
if __name__ == "__main__":
	
	def HADH(vts,num):
		return HighestAverages(HA_Divisors["DHondt"], AddInitial(vts), num)
	
	def HASL(vts,num):
		return HighestAverages(HA_Divisors["SainteLague"], AddInitial(vts), num)
	
	def HAHH(vts,num):
		return HighestAverages(HA_Divisors["HuntingtonHill"], AddInitial(vts,1), num)
	
	def HAAD(vts,num):
		return HighestAverages(HA_Divisors["Adams"], AddInitial(vts,1), num)
	
	def LRHR(vts,num):
		return LargestRemainder(LR_QuotaAdjust["Hare"], vts, num)
	
	def LRDP(vts,num):
		return LargestRemainder(LR_QuotaAdjust["Droop"], vts, num)
	
	MethodList = {"HA-DHondt": HADH, "HA-SainteLague": HASL, \
		"HA-HuntingtonHill": HAHH, "HA-Adams": HAAD, \
		"LR-Hare": LRHR, "LR-Droop": LRDP }
	
	def ExampleEval(exname,etgname=None):
		tgtname = exname if etgname == None else etgname
		ex = Examples[exname]
		tgt = ExampleTargets[tgtname]
		num = tgt[0]
		tvs = tgt[1]
		print(exname, "-", num)
		prt = tuple( (r[0] for r in ex) )
		print(prt)
		prt = tuple( (r[1] for r in ex) )
		print(prt)
		for mth in tvs:
			print(mth)
			print(tvs[mth])
			res = MethodList[mth](ex,num)
			prt = tuple( (r[2] for r in res) )
			print(prt)
		print()

	ExampleEval("WikiHA11")
	ExampleEval("WikiHA12")
	ExampleEval("WikiHA13")	
	ExampleEval("WikiHA2")
	ExampleEval("WikiHA3")
	ExampleEval("WikiHAKn")
	ExampleEval("WikiLR1")
	ExampleEval("WikiLR2","WikiLR21")
	ExampleEval("WikiLR2","WikiLR22")
	
	# Tests of extended features: minimum, maximum numbers of seats
	
	# Test data to use
	TestSet = Examples["WikiHA11"]
	print(TestSet)
	
	# For ordering the results back into the order of the test set:
	TSOrd = {}
	for k, TS in enumerate(TestSet):
		TSOrd[TS[0]] = k
	def MakeTSOrd(res):
		rsord = len(res)*[None]
		for r in res:
			rsord[TSOrd[r[0]]] = r
		return rsord
	
	def dumpout(res): print([r[2:] for r in MakeTSOrd(res)])
	
	print("Add Initial")
	dumpout(AddInitial(TestSet,6))
	
	print("Add Rounded Down")
	dumpout(AddRoundedDown(TestSet,100))
	dumpout(AddRoundedDown(TestSet,100,MaxSeats=30))
	dumpout(AddRoundedDown(TestSet,100,MinSeats=15))
	dumpout(AddRoundedDown(TestSet,100,MinSeats=15,MaxSeats=30))
	
	print("Highest Averages")
	dvsrf = HA_Divisors["SainteLague"]
	dumpout(HighestAverages(dvsrf, AddInitial(TestSet), 100))
	dumpout(HighestAverages(dvsrf, AddInitial(TestSet), 100, MaxSeats=30))	
	dumpout(HighestAverages(dvsrf, AddInitial(TestSet,15), 100))
	dumpout(HighestAverages(dvsrf, AddInitial(TestSet,15), 100, MaxSeats=30))
	
	print("Largest Remainders")
	qtadj = LR_QuotaAdjust["Hare"]
	dumpout(LargestRemainder(qtadj, TestSet, 100))
	dumpout(LargestRemainder(qtadj, TestSet, 100, MaxSeats=30))	
	dumpout(LargestRemainder(qtadj, TestSet, 100, MinSeats=15))
	dumpout(LargestRemainder(qtadj, TestSet, 100, MinSeats=15, MaxSeats=30))
	
	print("Adjusted Divisor")
	dumpout(AdjustedDivisor(-1, TestSet, 100))
	dumpout(AdjustedDivisor(0, TestSet, 100))
	dumpout(AdjustedDivisor(1, TestSet, 100))
	dumpout(AdjustedDivisor(-1, TestSet, 100, MaxSeats=30))
	dumpout(AdjustedDivisor(0, TestSet, 100, MaxSeats=30))
	dumpout(AdjustedDivisor(1, TestSet, 100, MaxSeats=30))
	dumpout(AdjustedDivisor(-1, TestSet, 100, MinSeats=15))
	dumpout(AdjustedDivisor(0, TestSet, 100, MinSeats=15))
	dumpout(AdjustedDivisor(1, TestSet, 100, MinSeats=15))
	dumpout(AdjustedDivisor(-1, TestSet, 100, MinSeats=15, MaxSeats=30))
	dumpout(AdjustedDivisor(0, TestSet, 100, MinSeats=15, MaxSeats=30))
	dumpout(AdjustedDivisor(1, TestSet, 100, MinSeats=15, MaxSeats=30))