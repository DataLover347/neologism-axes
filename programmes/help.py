import io
import csv

# newFileName="hangry_2016_only_comb_clean_new.txt"
# open(newFileName, "w").close()
# with open("hangry_2016_only_comb_clean.txt", encoding="utf-16le", errors='ignore') as fi:
# 	old_data = fi.read()
# 	with open(newFileName, "a", encoding='utf-16le', errors='ignore') as fil:
# 		fil.write(old_data.strip())


FileName="lightsaber_2012_only_comb_dirty.csv"
in_file = open(FileName, "r", encoding='utf-16le', errors='replace')		##for files made by hand (e.g. _comb), remove encoding
reader = csv.reader(in_file)
for row in reader:
	print(row)
	if(row==NUL)