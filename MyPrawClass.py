# chcp 65001
import praw
import time
import datetime
import csv
import os
import re
import collections

class RedditDataGatherer:
	
	# Connects to reddit script app
	reddit = praw.Reddit(client_id='HjEoIkx_K-VyDA', client_secret='kGsqsKpRvr-OcjSSDfVWUR1pOpI',
							password='E&MForum1', user_agent='testscript by /u/fakebot3', username='PiLover3_14159')


	""" Gathers neccessary file names and keywords """

	# Asks for a file name; opens the file, cleans out any contents if the file already existed, and then closes the file
	def getTextFileName(self):
		fileInput = input("Please name the output text file (name only, do not add '.txt'): ")
		fileName = str(fileInput+".txt")
		open(fileName, "w").close()
		return fileName

	# Asks for a file name; opens the file, cleans out any contents if the file already existed, and then closes the file
	def getCSVFileName(self):
		fileInput = input("Please name the output CSV file (name only, do not add '.csv'): ")
		fileName = str(fileInput+".csv")
		open(fileName, "wb").close()
		return fileName

	# Asks for a keyword
	def getKeyword(self):
		return input("Please enter your search word: ")


	"""  Define functions for The Search  """
	"""
		The Search is defined as:
		1) Find subreddits that have the keyword in their contents
		2) Get the top 10 submissions of those list of subreddits.
		3) Access the comments in all of these submissions.
	"""

	# (1) Creates a list of all subreddits that contain the keyword in their contents.
	def getSubredditsByKeyword(self, keyword):
		return self.reddit.subreddits.search_by_topic(str(keyword))

	# (2) Creates a ListGenerator of all submissions of a given subreddit that contain the keyword.
	def getSubmissionIDByKeyword(self, subreddit, keyword):
		return self.reddit.subreddit(subreddit).search(keyword)

	# (3) Accesses all comments of a given submission.
	def accessSubmission(self, submissionID):
		return self.reddit.submission(id=submissionID)

	# Convert UTC time to epoch for searching purposes.
	def utc_to_epoch(self):
		day = input("Day (dd): ")
		month = input("Month (mm): ")
		year = input("Year (YYYY): ")
		hour = input("Hour (HH): ")
		minute = input("Minute (MM): ")
		second = input("Second (SS): ")
		date_time = str(day+"."+month+"."+year+" "+hour+":"+minute+":"+second)
		pattern = "%d.%m.%Y %H:%M:%S"
		try:
			print(int(time.mktime(time.strptime(date_time, pattern))))
		except ValueError:
			print("Please match the format dd.mm.YYYY HH:MM:SS.")
			exit()


	"""  Functions to read comments and write them to a text file  """

	# Writes to a file each top-level comment retrieved by The Search,.
	def getAllTopComments(self):
		fileName = self.getTextFileName()
		keyword = self.getKeyword()

		# The Search
		mySRList = self.getSubredditsByKeyword(keyword)
		for i in range(len(mySRList)):
			myLG = self.getSubmissionIDByKeyword(str(mySRList[i]), keyword)
			try:
				for j in range(10):			##could be problematic if there are not 10 submissions in the subreddit##
					while(os.path.getsize(str("C:\\Users\\btayl\\OneDrive\\Documents\\SFI Internship 2017\\PRAW\\"+fileName)) < 100000):   ##while file is less than 100KB
						submission = self.accessSubmission(str(myLG.next()))
						submission.comments.replace_more(limit=0)
						# writes comments to file
						for top_level_comment in submission.comments:
							with open(fileName, "a", encoding='utf-16le') as f:
								f.write(top_level_comment.body+" ")

			# raised by ListGenerator (in accessSubmission())
			except StopIteration:
				pass

			else:
				f.close()

			# always close the file
			finally:
				f.close()

	# Writes to csv file all comments retrieved by The Search and their epoch date, sorted sorted top-down (i.e. first- then second- then third- level, etc.).
	def getAllCommentsSortedTD(self):
		fileName = self.getCSVFileName()
		keyword = self.getKeyword()
		# print("Please input a start date to search.")
		startDateTime = 1420095600
		# print("\nPlease input an end date to search.")
		endDateTime = 1451631599

		# The Search
		mySRList = self.getSubredditsByKeyword(keyword)
		for i in range(len(mySRList)):
			myLG = self.getSubmissionIDByKeyword(str(mySRList[i]), keyword)
			try:
				for j in range(10):			##could be problematic if there are not 10 submissions in the subreddit##
					while(os.path.getsize(str("C:\\Users\\btayl\\OneDrive\\Documents\\SFI Internship 2017\\PRAW\\"+fileName)) < 100000):   ##while file is less than 100KB
						submission = self.accessSubmission(str(myLG.next()))
						if( (submission.created > startDateTime) and (submission.created < endDateTime) ):
							submission.comments.replace_more(limit=0)
							for comment in submission.comments.list():
								with open(fileName, "a", encoding='utf-16le') as f:
									f.write(top_level_comment.body+" ")

			#raised by ListGenerator (accessSubmission)
			except StopIteration:
				pass

			#always close the file
			finally:
				f.close()
	
	# Writes to csv file all comments retrieved by The Search and their epoch date, sorted first with replies (i.e. by top-level and then their replies).
	def getAllCommentsSortedFwRWithDate(self):
		fileName = self.getCSVFileName()
		keyword = self.getKeyword()
		# print("Please input a start date to search.")
		startDateTime = 1420095600
		# print("\nPlease input an end date to search.")
		endDateTime = 1451631599

		# The Search
		mySRList = self.getSubredditsByKeyword(keyword)
		for i in range(len(mySRList)):
			myLG = self.getSubmissionIDByKeyword(str(mySRList[i]), keyword)
			try:
				for j in range(10):			##could be problematic if there are not 10 submissions in the subreddit##
					while(os.path.getsize(str("C:\\Users\\btayl\\OneDrive\\Documents\\SFI Internship 2017\\PRAW\\"+fileName)) < 100000):   ##while file is less than 100KB
						submission = self.accessSubmission(str(myLG.next()))
						if( (submission.created > startDateTime) and (submission.created < endDateTime) ):
							submission.comments.replace_more(limit=0)
							# writes comments to file
							for top_level_comment in submission.comments:
								with open(fileName, "a", newline='', encoding='utf-16le') as f1:
									myWriter = csv.writer(f1, delimiter=',')
									myWriter.writerow([str(top_level_comment.body)]+[str(datetime.datetime.fromtimestamp(top_level_comment.created))])
								for reply in top_level_comment.replies.list():
									with open(fileName, "a", newline='', encoding='utf-16le') as f2:
										myWriter = csv.writer(f2, delimiter=',')
										myWriter.writerow([str(reply.body)]+[str(datetime.datetime.fromtimestamp(reply.created))])

			#raised by ListGenerator (accessSubmission)
			except StopIteration:
				pass

			#always close the file
			finally:
				f1.close()
				f2.close()

	# Writes to file all comments containing the keyword found by The Search, ordered by first-, then second-, then third- ... -level comments.
	def getCommentsContainingKeyword(self):
		fileName = self.getTextFileName()
		keyword = self.getKeyword()

		# The Search
		mySRList = self.getSubredditsByKeyword(keyword)
		for i in range(len(mySRList)):
			myLG = self.getSubmissionIDByKeyword(str(mySRList[i]), keyword)
			try:
				for j in range(10):			##could be problematic if there are not 10 submissions in the subreddit##
					while(os.path.getsize(str("C:\\Users\\btayl\\OneDrive\\Documents\\SFI Internship 2017\\PRAW\\"+fileName)) < 100000):   ##while file is less than 100KB
						submission = self.accessSubmission(str(myLG.next()))
						submission.comments.replace_more(limit=0)
						# writes comments to file
						for comment in submission.comments.list():
							with open(fileName, "a", encoding='utf-16le') as f:
								if keyword in str(comment.body):
									f.write(comment.body)

			#raised by ListGenerator (accessSubmission)
			except StopIteration:
				pass

			#always close the file
			finally:
				f.close()

	# Writes to csv file all comments containing the keyword found by The Search and their epoch date.
	def getCommentsContainingKeywordWithDate(self):
		fileName = self.getCSVFileName()
		keyword = self.getKeyword()
		# print("Please input a start date to search.")
		startDateTime = 1420095600
		# print("\nPlease input an end date to search.")
		endDateTime = 1451631599

		# The Search
		mySRList = self.getSubredditsByKeyword(keyword)
		for i in range(len(mySRList)):
			myLG = self.getSubmissionIDByKeyword(str(mySRList[i]), keyword)
			try:
				for j in range(10):			##could be problematic if there are not 10 submissions in the subreddit##
					while(os.path.getsize(str("C:\\Users\\btayl\\OneDrive\\Documents\\SFI Internship 2017\\PRAW\\"+fileName)) < 100000):   ##while file is less than 100KB
						submission = self.accessSubmission(str(myLG.next()))
						if( (submission.created > startDateTime) and (submission.created < endDateTime) ):
							submission.comments.replace_more(limit=0)
							# writes comments to file
							for comment in submission.comments.list():
								with open(fileName, "a", newline='', encoding='utf-16le') as f:
									if keyword in str(comment.body):
										myWriter = csv.writer(f, delimiter=',')
										myWriter.writerow([str(comment.body)]+[str(datetime.datetime.fromtimestamp(comment.created))])

			#raised by ListGenerator (accessSubmission)
			except StopIteration:
				pass

			#always close the file
			finally:
				f.close()


	""" Functions for cleaning the data """

	# Replaces all occurrences of typical Reddit formatting characters
	def readAndReplaceChars(self, string):
		for ch in ['*','^','#','>']:
			if ch in string:
				string = string.replace(ch, " ")
		return string.strip()

	# Removes all occurrences of links (in brackets or not)
	# regex help from https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
	def readAndReplaceLinks(self, string):
		listOfLinks = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
		for link in listOfLinks:
			string = string.replace(link, "")
		return string.strip()

	# Finds the pairs of parentheses
	# adapted from https://stackoverflow.com/questions/29991917/indices-of-matching-parentheses-in-python
	def findParens(self, string):
		pairDict = {}
		parenStack = []
		for i, c in enumerate(string):
			if c == '(':
				parenStack.append(i)
			elif c == ')':
				if len(parenStack) == 0:
					continue
				pairDict[parenStack.pop()] = i
		if len(parenStack) > 0:
			parenStack.pop()
		# puts pairDict in order to strip sentence in index order
		od = collections.OrderedDict(sorted(pairDict.items()))
		return od

	# Finds the pairs of brackets
	def findBrackets(self, string):
		pairDict = {}
		brackStack = []
		for i, c in enumerate(string):
			if c == '[':
				brackStack.append(i)
			elif c == ']':
				if len(brackStack) == 0:
					continue
				pairDict[brackStack.pop()] = i
		if len(brackStack) > 0:
			brackStack.pop()
		# puts pairDict in order to strip sentence in index order
		od = collections.OrderedDict(sorted(pairDict.items()))
		return od

	# Deletes all hyperlinks enclosed in []() format
	# Type 'chcp 65001' into Windows CMD beforehand
	def deleteHyperlinks(self, string):
		listToDelete = []
		odP = self.findParens(string)
		odB = self.findBrackets(string)
		# if most ordered dictionaries are non-empty...
		if(odP and odB):
			for bKey, bValue in odB.items():
				for pKey, pValue in odP.items():
					endBrack = bValue
					startParen = pKey
					# ...find the indexes that have '](' signifying a hyperlink, and add the starting [ and ending ) hyperlink indexes to the list
					if(endBrack+1 == startParen):
						listToDelete.append(bKey)
						listToDelete.append(pValue)
		# if there are no hyperlinks, return the string as before
		if(len(listToDelete) == 0):
			return string
		# if there is only one hyperlink, take start and end of the string around the hyperlink
		elif(len(listToDelete) == 2):
			new_data = string[:listToDelete[0]]+string[listToDelete+1:]
		# if there is more than one hyperlink...
		else:
			#... get the beginning string until the first hyperlink...
			new_data = string[:listToDelete[0]]
			#... and the string between each of the other hyperlinks...
			for i in range(int(len(listToDelete)/2)):
				if i % 2 != 0:
					continue
				new_data = new_data + string[listToDelete[i+1]+1:listToDelete[i+2]]
			#... and the end of the string after the last hyperlink
			new_data = new_data + string[listToDelete[len(listToDelete)-1]+1:]
		return new_data

	# Removes all links/mentions to other reddits or users
	def removeUserAndRedditLinks(self, string):
		indexDict = {}		# use dictionary to prevent duplicate indexes if a reddit or user is mentioned more than once
		# find token beginning with /r/ to signify a reddit link
		for a in re.findall(r'(?:/r/?)[^\s]+', string):
			string = string.replace(a, " ")
		# find token beginning with /u/ to signify a user link
		for a in re.findall(r'(?:/u/?)[^\s]+', string):
			string = string.replace(a, " ")
		return string

	# Removes all comments that have been deleted
	def removeDeletedPosts(self, string):
		if "[deleted]" in string:
			string = string.replace("[deleted]", " ")
		return string.strip()

	# Cleans file using above methods
	def cleanFile(self, file):
		# newFileName = self.getTextFileName()
		with open(file, encoding="utf-16le") as f:
			old_data = f.read()
		removedBPLinks = self.deleteHyperlinks(old_data)
		removedOthLinks = self.readAndReplaceLinks(removedBPLinks)
		removedUandRLinks = self.removeUserAndRedditLinks(removedOthLinks)
		removedChars = self.readAndReplaceChars(removedUandRLinks)
		removedDelPosts = self.removeDeletedPosts(removedChars)
		print(removedDelPosts.strip())
		# with open(newFileName, "a", encoding='utf-16le') as f:
		# 	f.write(removedDeletedPosts)

	# def mine(self):
	# 	# fileName = self.getCSVFileName()
	# 	keyword = "bird"
	# 	# print("Please input a start date to search.")
	# 	startDateTime = 1420095600
	# 	# print("\nPlease input an end date to search.")
	# 	endDateTime = 1451631599

	# 	submission = self.accessSubmission("329h7j")
	# 	if( (submission.created > startDateTime) and (submission.created < endDateTime) ):
	# 		submission.comments.replace_more(limit=0)
	# 		# writes comments to file
	# 		for top_level_comment in submission.comments:
	# 			print(top_level_comment.body)
	# 			for ick in top_level_comment.replies.list():
	# 				print(ick.body)


x = RedditDataGatherer()
# x.cleanFile("tickle2.txt")
x.getCommentsWithDate()
# x.mine()