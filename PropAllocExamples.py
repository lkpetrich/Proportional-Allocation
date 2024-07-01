#!python3
#
# Examples from Wikipedia and Electowiki of various election algorithms
# as tests of the code in PropAlloc.py
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
#
# Note: the Israeli Knesset allocation is not exactly D'Hondt,
# for reasons stated in the Huntington-Hill article


from PropAlloc import HighestAverages, HA_Divisors, AddInitial
from PropAlloc import LargestRemainders, LR_QuotaAdjust
from PropAlloc import AdjustDivisor, AD_Rounding


Votes = {}

Votes["EleW HA - DH SL MSL"] = (('Yellow',47_000,5,4,5), ('White',16_000,2,2,2), 
	('Red',15_900,2,2,2), ('Green',12_000,1,1,1), ('Blue',6_000,0,1,0), 
	('Pink',3_100,0,0,0))

Votes["Wiki DH Old - DH"] = (('A',100,4), ('B',80,3), ('C',30,1), ('D',20,0))

Votes["ElecW DH - DH"] = (('A',340_000,3), ('B',280_000,3), ('C',160_000,1),
	('D',60_000,0), ('E',15_000,0))

Votes["Wiki SL Old - SL"] = (('A',53,3), ('B',24,2), ('C',23,2))

Votes["Elec SL - DH SL"] = (('A',503,18,17), ('B',304,10,11), ('C',193,6,7))

Votes["Wiki DH SL - DH SL"] = (('A',100_000,4,3), ('B',80_000,3,3), 
	('C',30_000,1,1), ('D',20_000,0,1))

Votes["Wiki HH - HH DH"] = (("Likud",985_408,30,30), ("Zionist Union",786_313,24,24), 
	("Joint List",446_583,13,13), ("Yesh Atid",371_602,11,11),
	("Kulanu",315_360,9,10), ("The Jewish Home",283_910,9,8), 
	("Shas",241_613,7,7), ("Yisrael Beiteinu",214_906,6,6), 
	("United Torah Judaism",210_143,6,6), ("Meretz",165_529,5,5))

Votes["Wiki EleW LR - Hare Droop"] = (('Yellow',47_000,5,5), ('White',16_000,2,2), 
	('Red',15_800,1,2), ('Green',12_000,1,1), ('Blue',6_100,1,0), 
	('Pink',3_100,0,0))

Votes["EleW Ham - Hare"] = (("Virginia",630_560,11), ("Massachusetts",475_327,8), 
	("Pennsylvania",432_879,7), ("North Carolina",353_523,6), ("New York",331_589,6), 
	("Maryland",278_514,5), ("Connecticut",236_841,4), ("South Carolina",206_236,3), 
	("New Jersey",179_570,3), ("New Hampshire",141_822,2), ("Vermont",85_533,1), 
	("Georgia",70_835,1), ("Kentucky",68_705,1), ("Rhode Island",68_446,1), 
	("Delaware",55_540,1))

Votes["LbTx 1 - Hare HH Jf Ad Wb"] = (("Alpha",24_000,2,2,2,3,2), ("Beta",56_000,5,6,6,6,6), 
	("Gamma",28_000,2,3,3,3,3), ("Delta",17_000,1,2,2,2,2), ("Epsilon",65_000,6,7,7,6,7), 
	("Zeta",47_000,4,5,5,5,5))

Votes["LbTx 2 - Hare Jf Ad Wb HH"] = (('A',25_010,15,16,15,15,15), ('B',8_760,5,5,5,5,5), 
	('C',11_590,7,7,7,7,7), ('D',9_025,6,5,6,6,6), ('E',15_080,9,9,9,9,9))

Methods = {}
Methods["DH"] = \
	lambda v,n: HighestAverages(HA_Divisors["DHondt"], AddInitial(v), n)
Methods["SL"] = \
	lambda v,n: HighestAverages(HA_Divisors["SainteLague"], AddInitial(v), n)
Methods["MSL"] = \
	lambda v,n: HighestAverages(HA_Divisors["ModifiedSainteLague"], AddInitial(v), n)
Methods["HH"] = \
	lambda v,n: HighestAverages(HA_Divisors["HuntingtonHill"], AddInitial(v,1), n)
Methods["Hare"] = \
	lambda v,n: LargestRemainders(LR_QuotaAdjust["Hare"], v, n)
Methods["Droop"] = \
	lambda v,n: LargestRemainders(LR_QuotaAdjust["Droop"], v, n)
Methods["Jf"] = \
	lambda v,n: AdjustDivisor(AD_Rounding["Jefferson"], v, n)
Methods["Wb"] = \
	lambda v,n: AdjustDivisor(AD_Rounding["Webster"], v, n)
Methods["Ad"] = \
	lambda v,n: AdjustDivisor(AD_Rounding["Adams"], v, n)


def partition(lst, prtlen):
	nprts = len(lst) // prtlen
	return [ lst[k*prtlen:(k+1)*prtlen] for k in range(nprts) ]


def ShowVotes(Name,Vote):
	SrcName, MethodStr = Name.split(" - ")
	MethodList = MethodStr.split(" ")
	
	VoteInput = [VT[:2] for VT in Vote]
	SrcIndex = {}
	for k, VT in enumerate(Vote):
		SrcIndex[VT[0]] = k
	
	SeatOutput = [list(VT[:2]) for VT in Vote]
	
	print(SrcName, " - ", MethodList)
	for k, MethodName in enumerate(MethodList):
		
		SeatTarget = [VT[k+2] for VT in Vote]
		for ix, st in enumerate(SeatTarget):
			SeatOutput[ix].append(st)
		
		NumSeats = sum(SeatTarget)
		res = Methods[MethodName](VoteInput, NumSeats)
		
		for r in res:
			ix = SrcIndex[r[0]]
			SeatOutput[ix].append(r[2])
	
	for SO in SeatOutput: print(partition(SO,2))

print("Header: name, abbreviations of methods")
print("Body: lines of [name, votes]")
print("    then for each method, [target, calculated here]")
for nm,vt in Votes.items(): ShowVotes(nm,vt)