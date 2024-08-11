# Proportional-Allocation
For doing proportional allocation and representation.

Implements:
- Highest averages (D'Hondt, Sainte-Laguë, Huntington-Hill, etc.)
- Largest remainders (Hare, Droop, Imperiali)
- Adjusted divisor (Jefferson, Webster, Adams)
Has the options of minimum and maximum numbers of seats.
Also includes initial numbers of seats for highest-averages, both constant and a rounded-down approximation.

## How to Use

All of these files run on the command line.

EUParlAlloc.py
- Returns:
  - Allocation for each EU member nation using various algorithms to try to reverse-engineer the EU's algorithm

GeneralAlloc.py
- Args:
  - Tab-delimited data file with each row having (party) (number of votes)
  - Total number
- Returns:
  - Allocation for each party using various algorithms

USHouseAlloc.py
- Args:
  - Tab-delimited data file with each row having (state) (population) (actual or estimated number of Reps)
  - (optional) total number of Reps (default: calculated from the actual/estimated number)
  - (optional) maximum number of Reps in each state (default: no maximum)
- Returns:
  - Allocation of US House using various algorithms, compared to the actual/estimated allocation

USSenateAlloc.py
- Args:
  - Tab-delimited data file with each row having (state) (population) (actual or estimated number of Reps)
  - (optional) average number of Senators per state (default: 2)
  - (optional) maximum number of Senators in each state (default: no maximum)
- Returns:
  - Allocation of US House using the Huntington-Hill algorithm, used for the House

## Source files
- PropAlloc.py -- in Python. File contains instructions on how to use it.
- GeneralAlloc.py -- reads in a file and runs some proportional-allocation algorithms on it.
- USHouseAlloc.py -- for the US House of Representatives.
- USSenateAlloc.py -- for the US Senate, experiments in proportional allocation
- EUParlAlloc.py - for the European Parliament.
- Proportional Allocation.nb -- in Mathematica.

Data for USHouseAlloc.py -- population data from US Census data and estimates
- US States 1790.txt -- seats: 105
- US States 2010.txt -- seats: 435
- US States 2020.txt -- census results
- US States 2020 DC.txt -- census results with Washington DC added (presumed 1 seat)
- US States 2020 PR.txt -- census results with Puerto Rico added (presumed 4 seats)
- US States 2020 DC PR.txt -- census results with DC and Puerto Rico added (presumed total 5 seats)

Data for USSenateAlloc.py -- this file along with population data
- USStateAbbrevs.txt -- two-letter abbreviations for US states and territories

Data for EUParlAlloc.py -- election of the European Parliament
- EU Parliament.txt -- in 2024

Data for GeneralAlloc.py
- Votes - Absurd Parties.txt
- Votes - Colors.txt
- Votes - Ice Cream Flavors.txt
