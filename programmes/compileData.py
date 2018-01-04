## Creates files with all data except one word and combines it with that one word per year ##
## Located in directory containing ANSI data files in word_YYYY_only_sr/sub/comb_clean.txt format ##

import io
import glob
import string

# Converts all files to ANSI encoding and appends "Ansi" on end of file name
# Use once, then comment out call and use rest of program on new files
def convertUniToAnsi():
	fileList = glob.glob("*.txt")
	for file in fileList:
		newFileName = file[:-4]+"Ansi.txt"
		with open(file, encoding="utf-16le", errors='replace') as f:
			old_data = f.read()
		open(newFileName, "w").close()
		with open(newFileName, "a", errors='ignore') as f:
			f.write(old_data.strip())

# convertUniToAnsi()


# Compiles list of all files in directory that contain data of a given word (i.e. the file name starts with the word)
def getWordFileList(word):
	srFileNames =  word+"_201[0-9]_only_??_cleanAnsi.txt"
	subFileNames = word+"_201[0-9]_only_???_cleanAnsi.txt"
	combFileNames = word+"_201[0-9]_only_????_cleanAnsi.txt"
	srFileList = glob.glob(srFileNames)
	subFileList = glob.glob(subFileNames)
	combFileList = glob.glob(combFileNames)
	return (srFileList+subFileList+combFileList)

# Compiles list of all other files in directory that are not in the list returned by getWordFileList()
def getNonWordFileList(wordFileList):
	allFiles = glob.glob("*.txt")
	for wordFile in wordFileList:
		allFiles.remove(wordFile)
	return allFiles

# For a given file, doubles the file contents
def doubleWordFile(fileName):
	with open(fileName, errors='replace') as f:
		data = f.read()
	return (data.strip()+" "+data.strip())

# For all files given by getNonWordFileList(), returns the compilation of all contents
def compileNonWordFiles(NonWordFileList):
	data = ""
	for file in NonWordFileList:
		with open(file, errors='replace') as f:
			data = data+f.read().strip()
	return data.strip()

# Creates the new data file containing all non-word data plus a duplicate of the word file for each year
def createNewFiles():
	neologisms = ['dab', 'ship', 'bromance', 'photobomb', 'hangry', 'yolo', 'lightsaber', 'bae', 'hipster', 'troll']
	controls = ['run', 'save', 'bird', 'friendship', 'green']
	
	for n in neologisms:
		wordFileList = getWordFileList(n)
		nonWordData = compileNonWordFiles(getNonWordFileList(wordFileList))
		# for each word file, write a new file containing the word file duplicated plus contents of all non-word files
		for file in wordFileList:
			# name the file in format "wordYYYYWOnlyData.txt"
			newFileName = file.partition("_")[0]+file.partition("_")[2].partition("_")[0]+"WOnlyData.txt"
			newFileName = "WOnlyData/"+newFileName
			open(newFileName, "w").close()
			# write in contents
			with open(newFileName, "a", errors='ignore') as f:
				f.write(doubleWordFile(file)+" "+nonWordData)
	
	for c in controls:
		wordFileList = getWordFileList(c)
		nonWordData = compileNonWordFiles(getNonWordFileList(wordFileList))
		# for each word file, write a new file containing the word file duplicated plus contents of all non-word files
		for file in wordFileList:
			# name the file in format "wordYYYYWOnlyData.txt"
			newFileName = file.partition("_")[0]+file.partition("_")[2].partition("_")[0]+"WOnlyData.txt"
			newFileName = "WOnlyData/"+newFileName
			open(newFileName, "w").close()
			# write in contents
			with open(newFileName, "a", errors='ignore') as f:
				f.write(doubleWordFile(file)+" "+nonWordData)

createNewFiles()