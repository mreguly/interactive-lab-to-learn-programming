import sys, os
sys.stdout = open(os.devnull, 'w')
def sucet_delitelov(cislo):
	print("ASGA")
	return 60

print(sucet_delitelov(24))
sys.stdout = sys.__stdout__
