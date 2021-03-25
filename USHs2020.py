#!python3
#
# Allocates seats for the US House of Representatives for 2020
# for DC and Puerto Rico (optional new states)

import PropAlloc

NumSeats = 435

files = ("US States 2010.txt",
	"US States 2019 Est.txt",
	"US States 2019 Est DC.txt",
	"US States 2019 Est DC PR.txt")

data = []

for infile in files:
	d = []
	f = open(infile)
	for ln in f:
		lnsp = ln.split('\t')
		lnst = [s.strip() for s in lnsp]
		if len(lnst) < 3: continue
		d.append([lnst[0],int(lnst[1]),int(lnst[2])])
	
	states = tuple((s[0] for s in d))
	votes = tuple((s[1] for s in d))
	origseats = tuple((s[2] for s in d))
	
	vts = PropAlloc.AddInitial(d,1)
	res = PropAlloc.HuntingtonHill(vts,NumSeats)
	resseats = tuple((s[2] for s in res))
	rsstdiffs = tuple((s[1] - s[0] for s in zip(origseats,resseats)))
	dx = zip(states,votes,origseats,resseats,rsstdiffs)
	data.append(dx)

for k, dx in enumerate(data):
	print(k)
	for sx in dx:
		if sx[-1] != 0: print(sx[0], sx[-1])
	print()