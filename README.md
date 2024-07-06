# Proportional-Allocation
For doing proportional allocation and representation
Implements:
- Highest averages (D'Hondt, Sainte-Laguë, Huntington-Hill, etc.0
- Largest remainders (Hare, Droop, Imperiali)
- Adjusted divisor (Jefferson, Webster, Adams)
Has the options of minimum and maximum numbers of seats.
Also includes initial numbers of seats for highest-averages, both constant and a rounded-down approximation.

Source files:
- PropAlloc.py -- in Python. File contains instructions on how to use it.
- GeneralAlloc.py -- reads in a file and runs some proportional-allocation algorithms on it.
- USHouseAlloc.py -- for the US House of Representatives.
- EUParlAlloc.py - for the European Parliament.
- Proportional Allocation.nb -- in Mathematica.

Data for USHouseAlloc.py -- from US Census data and estimates
- US States 1790.txt -- seats: 105
- US States 2010.txt -- seats: 435
- US States 2020.txt -- census results
- US States 2020 DC.txt -- census results with Washington DC added (presumed 1 seat)
- US States 2020 PR.txt -- census results with Puerto Rico added (presumed 4 seats)
- US States 2020 DC PR.txt -- census results with DC and Puerto Rico added (presumed total 5 seats)

Data for EUParlAlloc.py -- election of the European Parliament
- EU Parliament.txt -- in 2024

Data for GeneralAlloc.py
- Votes - Absurd Parties.txt
- Votes - Colors.txt
- Votes - Ice Cream Flavors.txt
