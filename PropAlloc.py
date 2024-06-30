#!python3
#
# Proportional-allocation systems
#
# These are for allocation or apportionment
# of legislature seats for each political party in proportion to
# the number of votes that each party has received,
# or else the number of seats for each jurisdiction in proportion to
# its population.
#
#
# All these methods take a list of (party, # votes, ...)
# and return a list of (party, # votes, # seats, direction of departure)
#
#
# For highest-averages methods:
#
# AddInitial(Votes, Initial=0)
# Votes: list of (party, # votes, ...)
# Initial: initial number
# Returns: list of (party, # votes, initial number)
#
# AddRoundedDown(Votes, NumSeats, MinSeats=0, MaxSeats=None)
# Votes: list of (party, # votes, ...)
# NumSeats: how many seats to fill
# MinSeats (optional, explicit keyword): each party's minimum number of seats
# MaxSeats (optional, explicit keyword): each party's maximum number of seats
# Returns: list of (party, # votes, # seats, direction)
# where the direction is
# -1 - less than the minimum but rounded up
# 0 - between the minimum and the maximum inclusive
# 1 - greater than the maximum but rounded down
#
#
# Highest averages:
#
# HighestAverages(DivisorFunc, Votes, NumSeats, MaxSeats=None)
# Divisor function: returns a divisor value for its arg, the number of seats
# Votes: list of (party, # votes, initial number of seats, ...)
# The initial number of seats must be present even if it is zero.
# NumSeats: how many seats to fill
# MaxSeats (optional, explicit keyword): each party's maximum number of seats
#
# HA_Divisors: a collection of divisor functions, for number of seats s
# Arg: name of the method
#
# Adams: s
# Danish: 3s + 1
# SainteLague: 2s + 1 -- Webster-Sainte-Laguë
# DHondt: s + 1 -- Jefferson-D'Hondt
# Imperiali -- s + 2
# ModifiedSainteLague: 1.4 if s = 0 else (Sainte-Lague for s)
# HuntingtonHill: sqrt(s*(s+1))
#
#
# LargestRemainder(QuotaAdjust, Votes, NumSeats)
# Uses a quota adjustment for the total number of seats
#
# LR_QA: a collection of quota 
# LR_Hare -- 0
# LR_Droop -- 1
# LR_Imperiali -- 2
#
#
# AdjustDivisor(RoundDir, Votes, NumSeats)
# Uses a roundoff direction (< 0: downward, = 0: nearest, > 0: upward)
#
# Jefferson, Webster, Adams
# AD_Jefferson -- downward (-1)
# AD_Webster -- nearest (0)
# AD_Adams -- upward (1)
#
# Sources:
#
# Highest-averages method
# http://en.wikipedia.org/wiki/Highest_averages_method
# https://electowiki.org/wiki/Highest_averages_method
#
# Jefferson-D'Hondt method
# http://en.wikipedia.org/wiki/D%27Hondt_method
# https://electowiki.org/wiki/D%27Hondt_method
#
# Webster-Sainte-Laguë method
# http://en.wikipedia.org/wiki/Sainte-Lagu%C3%AB_method
#
# Huntington-Hill method
# http://en.wikipedia.org/wiki/Huntington-Hill_method
#
# Imperiali quota - Wikipedia
# https://en.wikipedia.org/wiki/Imperiali_quota
#
# Largest-remainder method
# http://en.wikipedia.org/wiki/Largest_remainders_method
# https://electowiki.org/wiki/Largest_remainder_method
#
# Hamilton's method - electowiki
# https://electowiki.org/wiki/Hamilton_method
#
# Adjusted-divisor method
# 9.2: Apportionment - Jefferson’s, Adams’s, and Webster’s Methods - Mathematics LibreTexts
# https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_College_Mathematics_for_Everyday_Life_(Inigo_et_al)/09%3A__Apportionment/9.02%3A_Apportionment_-_Jeffersons_Adamss_and_Websters_Methods
# The Webster method of apportionment
# https://www.pnas.org/content/77/1/1
#
# Degressive proportionality
# http://en.wikipedia.org/wiki/Degressive_proportionality

from math import sqrt, floor, ceil


# Add constant initial allocation:
# Default is zero
def AddInitial(Votes, Initial=0):
	return [list(Vote[:2]) + [Initial] for Vote in Votes]

# Add the rounded-down number of votes: (total) / (Hare quota),
# where (Hare quota) = (total) / (number of seats)
def AddRoundedDown(Votes, NumSeats, *, MinSeats=0, MaxSeats=None):
	
	# Maximum number of seats present?
	IsMax = MaxSeats != None

	# Name, number of votes, number of seats, direction
	# Direction: -1: too small, 0: in range, 1: too large
	VoteSeats = [list(Vote[:2]) + [0,0] for Vote in Votes]
	
	# Previous number of in-range members:
	PrevNumIRMems = len(VoteSeats)

	while True:
		
		# Find the quota to use
		# Count only the in-range entries
		SeatSum = NumSeats
		QuotaSum = 0
		for VS in VoteSeats:
			if VS[3] == 0:
				QuotaSum += VS[1]
			else:
				SeatSum -= VS[2]
		
		# If no in-range ones, then use this result:
		if SeatSum <= 0: return VoteSeats
		
		# Find the rounded-down number of seats
		# for every in-range one
		Quota = QuotaSum/float(SeatSum)
		QuotaRcp = 1/Quota
		for VS in VoteSeats:
			if VS[3] != 0: continue
			VS[2] = int(QuotaRcp*VS[1])
			if VS[2] < MinSeats:
				VS[2] = MinSeats
				VS[3] = -1
			elif IsMax and VS[2] > MaxSeats:
				VS[2] = MaxSeats
				VS[3] = 1
		
		# How many in-range members?
		NumIRMems = 0
		for VS in VoteSeats:
			if VS[3] == 0: NumIRMems += 1
		
		# If none, then one cannot continue
		if NumIRMems == 0: return VoteSeats
		
		# If no change, then accept the result
		if NumIRMems == PrevNumIRMems: return VoteSeats
		PrevNumIRMems = NumIRMems
		
		
# All methods: shared functions

# For final results, what the functions produce
def SortKeyFinal(a):
	# Seats, total votes, party name
	return (-a[2],-a[1],a[0])


# Highest-averages method

# Args: divisor function, votes (name, votes, init seats), number of seats
# Named optional: MaxSeats: maximum number of seats
def HighestAverages(DivisorFunc, Votes, NumSeats, *, MaxSeats=None):
	
	# Maximum number of seats present?
	IsMax = MaxSeats != None
	
	# Name, number of votes, number of seats, direction, average
	VoteSeats = [list(Vote[:3]) + [0,0] for Vote in Votes]
	
	# Sort order: highest to lowest
	# Average vote, total vote, name
	SortKeyHA = lambda a: (-a[4],-a[1],a[0])
	
	# Find the remaining seats
	# and the initial averages
	# for not over the limit:
	RemainingSeats = NumSeats
	for VS in VoteSeats:
		if IsMax and VS[2] > MaxSeats:
			VS[2] = MaxSeats
			VS[3] = 1
			VS[4] = 0
		else:
			VS[4] = VS[1]/float(DivisorFunc(VS[2]))
		RemainingSeats -= VS[2]
	
	# Seats still available?
	while RemainingSeats > 0:
		VoteSeats.sort(key=SortKeyHA)
		
		SeatAvail = False
		for VS in VoteSeats:
			# Don't add a seat if over the limit
			if VS[3] != 0: continue
			# If not at the limit, add the seat
			# Otherwise, mark it as above the limit
			SeatAvail = True
			if IsMax and VS[2] >= MaxSeats:
				VS[3] = 1
				VS[4] = 0
				continue
			else:
				VS[2] += 1
				VS[4] = VS[1]/float(DivisorFunc(VS[2]))
				RemainingSeats -= 1
			break
		# No seats could be added
		if not SeatAvail: break
	
	VoteSeats.sort(key=SortKeyFinal)
	return [Vote[:4] for Vote in VoteSeats]


def Divisor_Linear(s, d0, d1=1):
	return d0 + d1*s

def Divisor_DifferentInitial(DivisorFunc, InitialValue, s):
	if s == 0:
		return InitialValue
	else:
		return DivisorFunc(s)

# Methods all tend toward s + k + O(1/s) for large s;
# Will be sorted by the value of k
HA_Divisors = {}
# k = 0
HA_Divisors["Adams"] = lambda s: Divisor_Linear(s,0)
# k = 1/3
HA_Divisors["Danish"] = lambda s: Divisor_Linear(s,1,3)
# k = 1/2
HA_Divisors["SainteLague"] = lambda s: Divisor_Linear(s,1,2)
HA_Divisors["ModifiedSainteLague"] = \
	lambda s: Divisor_DifferentInitial(lambda sx: Divisor_Linear(sx,1,2), 1.4, s)
HA_Divisors["HuntingtonHill"] = lambda s: sqrt(s*(s+1))
HA_Divisors["Dean"] = lambda s: s*(s+1)/(2*s+1)
HA_Divisors["SquareMean"] = lambda s: sqrt(0.5*(s**2 + (s+1)**2))
# k = 1
HA_Divisors["DHondt"] = lambda s: Divisor_Linear(s,1)
# k = 2
HA_Divisors["Imperiali"] = lambda s: Divisor_Linear(s,2)

# Largest-remainder method

def LargestRemainders(QuotaAdjust, Votes, NumSeats, *, MinSeats=0, MaxSeats=None):
	
	# Maximum number of seats present?
	IsMax = MaxSeats != None

	# Name, number of votes, number of seats, direction, remainder
	# Direction: -1: too small, 0: in range, 1: too large
	VoteSeats = [list(Vote[:2]) + [0,0,0] for Vote in Votes]
	
	# Sort order: highest to lowest
	# Remainder, total, name
	SortKeyLR = lambda a: (-a[4],-a[1],a[0])
	
	# Previous number of in-range members:
	PrevNumIRMems = len(VoteSeats)

	while True:
		
		# Find the quota to use
		# Count only the in-range entries
		SeatSum = NumSeats
		QuotaSum = 0
		for VS in VoteSeats:
			if VS[3] == 0:
				QuotaSum += VS[1]
			else:
				SeatSum -= VS[2]
		
		# If no in-range ones, then use this result:
		if SeatSum <= 0: return VoteSeats
		
		# Find the rounded-down number of seats
		# and also the remainders
		# for every in-range one
		Quota = QuotaSum/float(SeatSum + QuotaAdjust)
		QuotaRcp = 1/Quota
		for VS in VoteSeats:
			if VS[3] != 0: continue
			VS[2] = int(QuotaRcp*VS[1])
			if VS[2] < MinSeats:
				VS[2] = MinSeats
				VS[3] = -1
				VS[4] = 0
			elif IsMax and VS[2] > MaxSeats:
				VS[2] = MaxSeats
				VS[3] = 1
				VS[4] = 0
			else:
				VS[4] = VS[1] - Quota*VS[2]
		
		RemainingSeats = NumSeats
		for VS in VoteSeats:
			if VS[3] == 0:
				RemainingSeats -= VS[2]
		
		VoteSeats.sort(key=SortKeyLR)
		
		for VS in VoteSeats:
			if VS[3] != 0: continue
			if RemainingSeats > 0:
				if IsMax and VS[2] >= MaxSeats:
					VS[2] = MaxSeats
					VS[3] = 1
					VS[4] = 0
				else:
					VS[2] += 1
				RemainingSeats -= 1
		
		# How many in-range members?
		NumIRMems = 0
		for VS in VoteSeats:
			if VS[3] == 0: NumIRMems += 1
		
		# If none, then one cannot continue
		if NumIRMems <= 0: break
		
		# If no change, then accept the result
		if NumIRMems == PrevNumIRMems: break
		PrevNumIRMems = NumIRMems
	
	# Finally
	VoteSeats.sort(key=SortKeyFinal)
	return [VS[:4] for VS in VoteSeats]

LR_QuotaAdjust = {}
LR_QuotaAdjust["Hare"] = 0
LR_QuotaAdjust["Droop"] = 1
LR_QuotaAdjust["Imperiali"] = 2


# Adjusted-divisor method
# Tries divisors until one of them gets the right number of seats
# VList members: name, votes, initial seats, calculated seats
def CountSeatsForDivisor(VoteSeats, Divisor, RoundFunc, MinSeats, MaxSeats):
	
	# Maximum number of seats present?
	IsMax = MaxSeats != None
	
	AllocatedSeats = 0
	DvsrRecip = 1./Divisor
	for VS in VoteSeats:
		Seats = RoundFunc(DvsrRecip*VS[1])
		if Seats < MinSeats:
			Seats = MinSeats
			SeatDir = -1
		elif IsMax and Seats > MaxSeats:
			Seats = MaxSeats
			SeatDir = 1
		else:
			SeatDir = 0
		VS[2] = Seats
		VS[3] = SeatDir
		AllocatedSeats += Seats
	
	return AllocatedSeats


def AdjustDivisor(RoundDir, Votes, NumSeats, *, MinSeats=0, MaxSeats=None):
	
	# Maximum number of seats present?
	IsMax = MaxSeats != None
	
	# Set the rounding function:
	if RoundDir > 0:
		RoundFunc = ceil
	elif RoundDir < 0:
		RoundFunc = floor
	else:
		RoundFunc = round

	# Members have party, votes, calculated seats, direction
	VoteSeats = [list(Vote[:2]) + [0,0] for Vote in Votes]
	TotalVotes = 0
	for VS in VoteSeats:
		TotalVotes += VS[1]
	
	# Find the initial divisor
	Divisor = float(TotalVotes)/float(NumSeats)
	DvsrSeats = CountSeatsForDivisor(VoteSeats, Divisor, RoundFunc, \
		MinSeats, MaxSeats)
	
	# Minimum and maximum departures from range
	DirMin = 1
	DirMax = -1
	for VS in VoteSeats:
		DirMin = min(DirMin,VS[3])
		DirMax = max(DirMax,VS[3])
	
	# Find the divisor-value bracket:
	# divisor and number of seats 1 and 2
	# Note: the calculated number of seats decreases with increasing divisor,
	# so Dvsr1 < Dvsr2 and DvsrSeats1 > DvsrSeats2
	
	if DvsrSeats > NumSeats:
		# Cannot have fewer seats?
		if DirMax == -1:
			VoteSeats.sort(key=SortKeyFinal)
			return VoteSeats
						
		# Find the lower bound
		Dvsr1 = Divisor
		DvsrSeats1 = DvsrSeats
		while True:
			# Increase the divisor
			Divisor *= 2
			DvsrSeats = CountSeatsForDivisor(VoteSeats, Divisor, RoundFunc, \
				MinSeats, MaxSeats)
			# Return if successfully bracketed
			if DvsrSeats == NumSeats:
				VoteSeats.sort(key=SortKeyFinal)
				return VoteSeats
			elif DvsrSeats < NumSeats:
				Dvsr2 = Divisor
				DvsrSeats2 = DvsrSeats
				break
			
			# Are all elements at minimum?
			DirMax = 1
			for VS in VoteSeats: DirMax = max(DirMax,VS[3])
			if DirMax == -1: break
				
	elif DvsrSeats < NumSeats:
		# Cannot have more seats?
		if DirMin == 1:
			VoteSeats.sort(key=SortKeyFinal)
			return VoteSeats

		# Find the upper bound
		Dvsr2 = Divisor
		DvsrSeats2 = DvsrSeats
		while True:
			# Decrease the divisor
			Divisor /= 2
			DvsrSeats = CountSeatsForDivisor(VoteSeats, Divisor, RoundFunc, \
				MinSeats, MaxSeats)
			# Return if successfully bracketed
			if DvsrSeats == NumSeats:
				VoteSeats.sort(key=SortKeyFinal)
				return VoteSeats
			elif DvsrSeats > NumSeats:
				Dvsr1 = Divisor
				DvsrSeats1 = DvsrSeats
				break
			
			# Are all elements at maximum?
			DirMin = 1
			for VS in VoteSeats: DirMin = min(DirMin,VS[3])
			if DirMin == 1: break
			
	else:
		# Equal 
		VoteSeats.sort(key=SortKeyFinal)
		return VoteSeats

	
	# Find the next value with linear interpolation
	while True:
		Divisor = Dvsr1 + (Dvsr2 - Dvsr1) * \
			( float(NumSeats - DvsrSeats1) / float(DvsrSeats2 - DvsrSeats1) )
		DvsrSeats = CountSeatsForDivisor(VoteSeats, Divisor, RoundFunc, \
			MinSeats, MaxSeats)
		
		# Interval too small?
		if abs(Dvsr2 - Dvsr1)/(Dvsr1 + Dvsr2) < 1e-8:
			VoteSeats.sort(key=SortKeyFinal)
			return VoteSeats
		
		if DvsrSeats > NumSeats:
			# Divisor too small
			# Replace the lower bound
			Dvsr1 = Divisor
			DvsrSeats1 = DvsrSeats
		elif DvsrSeats < NumSeats:
			# Divisor too large
			# Replace the upper bound
			Dvsr2 = Divisor
			DvsrSeats = DvsrSeats
		else:
			# Equal
			VoteSeats.sort(key=SortKeyFinal)
			return VoteSeats
		

AD_Rounding = {}
AD_Rounding["Jefferson"] = -1
AD_Rounding["Webster"] = 0
AD_Rounding["Adams"] = 1
