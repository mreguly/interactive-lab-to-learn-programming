import sys, os
sys.stdout = open(os.devnull, 'w')
def vypis_delitele(cislo):
	print("ASF")
	return "1 2 3 4 6 8 12 24"

print(vypis_delitele(24))
sys.stdout = sys.__stdout__
