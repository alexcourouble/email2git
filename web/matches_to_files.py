"""
Copyright (C) 2017 Alex Courouble <alex.courouble@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License 

along with this program. If not, see <http://www.gnu.org/licenses/>.



Reads PICKLED matches from subject and line matches files

Input: 
-	LINES_OUTPUT.txt
-	SUBJECT_OUTPUT.txt
-	commit_dates.txt
-	patch_mailinglist_data.txt
-	mailing_lists_ids.txt
"""

LINE_MATCHES = "LINES_OUTPUT.txt"
SUBJECT_MATCHES = "SUBJECT_OUTPUT.txt"

CID_DATE = "commit_dates.txt"
PATCH_MAILINGLIST = "mailing_list_data/patch_mailinglist_data.txt"
ML_NAMES = "mailing_list_data/mailing_lists_ids.txt"

OUTPUT = "/Users/alexandrecourouble/Documents/public_html/cregit_web/matches/"

import cPickle as pickle

class Match():
	def __init__(self, cid, pwid, mailing_list, matchType, date):
		self.cid = cid
		self.pwid = pwid
		self.mailing_list = mailing_list
		self.matchType = matchType
		self.date = date


def readMailingListData():
	ml_map = {}
	patches_data = {}

	print "Reading Mailing List data"
	# Reading mailing lists ids
	with open(ML_NAMES) as f:
		for i in f:
			split = i.strip("\n").split(",")
			ml_map[split[0]] = split[1]


	# reading patches and their mailing list
	with open(PATCH_MAILINGLIST) as f:
		for i in f:
			split = i.strip("\n").split("\t")
			patches_data[split[0]] = (ml_map[split[1]],split[2])

	return patches_data
			

def readMatches():
	print "Rading Matches"

	# new line matches
	with open(LINE_MATCHES) as f:
		parseMatches(pickle.load(f),"l")
	
	# new subject matches
	with open(SUBJECT_MATCHES) as f:
		parseMatches(pickle.load(f),"s")



def parseMatches(matchesDict,matchType):
	print "Read", len(matchesDict),"line matches"

	for i in matchesDict:
		for j in matchesDict[i]:
			pwid = j
			cid = i
			mailing_list = patches_data[pwid][0]
			date = patches_data[pwid][1]
			# matches[i] = Match(cid,pwid,mailing_list,matchType,date)
			if i not in matches:
				matches[i] = set([])
			matches[i].add(Match(cid,pwid,mailing_list,matchType,date))



if __name__ == '__main__':
	matches = {}

	patches_data = readMailingListData()
	
	readMatches()

	for i in matches:
		# creating file to write matches
		file_name = OUTPUT + i +".txt"
		with open(file_name,"w") as f:
			for j in matches[i]:
				lineToWrite = j.pwid+","+j.mailing_list+","+j.date+","+j.matchType+"\n"
				f.write(lineToWrite)
		



