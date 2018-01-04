## For all CSV files in the directory, converts the first column contents to a text file ##
## Located in directory containing CSV files in the word_only format ##

import io
import csv
import glob
csv.field_size_limit(100000000)  ##deals with large cell field sizes

# Compiles list of all CSV files in directory and loops through them
fileList = glob.glob('*.csv')
for f in fileList:
	# reads file
	in_file = open(f, "r", encoding='utf-16le', errors='ignore')
	reader = csv.reader(in_file)

	# creates output file that is the same as the original file name but now is a text file
	newFileName = f[:-3]+"txt"
	open(newFileName, "w").close()
	print("New file created: "+newFileName)

	# for each row in the input file, write the first column's contents, and separate each comment with a space
	for row in reader:
		with open(newFileName, "a", encoding='utf-16le', errors='ignore') as f:
			f.write(row[0]+" ")

	# close the file
	in_file.close()