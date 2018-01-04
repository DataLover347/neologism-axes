import io
import glob

def combineFiles():
	newFileName = input("Please input the new combined file name (omit '.txt'): ")
	newFileName = newFileName+".txt"
	fileList = glob.glob('*.txt')
	open(newFileName, "w").close()
	print(fileList)
	for f in fileList:
		with open(f, encoding="utf-16le", errors='replace') as fi:
			old_data = fi.read()
			with open(newFileName, "a", encoding='utf-16le', errors='replace') as fil:
				fil.write(old_data.strip())

combineFiles()