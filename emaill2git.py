"""

Author: Alex Courouble <alex.courouble@gmail.com>
"""
import sqlite3
import cPickle as pickle
import difflib
import time

# SUBJECT
PW_DB = '/Users/alexandrecourouble/Desktop/email2git_data/pwSubject_short.db'
GIT_DB = '/Users/alexandrecourouble/Desktop/email2git_data/commit_subject.db'
OUTPUT = '/Users/alexandrecourouble/Desktop/email2git_data/SUBJECT_OUTPUT.txt'

# LINES
PATCHES_PICKLED = '/Users/alexandrecourouble/Desktop/email2git_data/PATCHES_PICKLED.txt'
COMMITS_PICKLED = '/Users/alexandrecourouble/Desktop/email2git_data/COMMITS_PICKLED.txt'
COMMIT_MAP = '/Users/alexandrecourouble/Desktop/email2git_data/COMMIT_MAP_PICKLED.txt'

MATCH_RATIO = .2

PATCH_FILE_MAP = {}
COMMIT_FILE_MAP = {}

PATCH_AUTHOR_MAP = {}
COMMIT_AUTHOR_MAP = {}

patches = {}
commits = {}

subjectMatches = {}
lineMatches = {}

subjectMatchesCount = 0
lineMatchesCount = 0


MATCHED_CID = set([])
MATCHED_PWID = set([])


notMatched = []

def getSubjectMatches():
	print "Finding subject matches"

	global subjectMatches
	global subjectMatchesCount
	global notMatched
	connGIT = sqlite3.connect(GIT_DB) # connecting
	connGIT.text_factory = str
	cg = connGIT.cursor() #creating cursor
	gitCommits = {}
	for row in cg.execute('select * from subject'):
		gitCommits[row[0]] = (row[1],row[2])
	connGIT.close()

	 # list containing all cids that weren't matched
	connPW = sqlite3.connect(PW_DB) # connecting
	connPW.text_factory = str
	cp = connPW.cursor() # creating cursor

	# with open(OUTPUT,"w") as matches: # opening file for writting subject matches
	# 	for i in gitCommits:
	# 		string = '%'+gitCommits[i][1]+'%'
	# 		count = 0
	# 		for j in cp.execute("""select * from subject where subject like ?;""", (string,)):
	# 			# print str(j[0])+','+i
	# 			matches.write(str(j[0])+','+i+'\n')
	# 			count += 1
	# 		if count == 0: notMatched.append(i)

	for i in gitCommits:
			string = '%'+gitCommits[i][1]+'%'
			count = 0
			for j in cp.execute("""select * from subject where subject like ?;""", (string,)):
				# print str(j[0])+','+i
				if i not in subjectMatches:
					subjectMatches[i] = set([])
				subjectMatches[i].add(str(j[0]))
				MATCHED_PWID.add(str(j[0]))
				MATCHED_CID.add(i)
				count += 1
				subjectMatchesCount += 1
			if count == 0: notMatched.append(i)

	# printing remaining cids
	connPW.close()

	# for i in subjectMatches:
	# 	print i, subjectMatches[i]
	# print len(subjectMatches)
		
	# with open(OUTPUT,"w") as no_match:
	# 	for i in notMatched:
	# 		no_match.write(i+"\n")


def getLineMatches():
	readPW()
	readGit()
	doAuthMapMatching()
	doFileMapMatching()



def readPW():
	global PATCH_AUTHOR_MAP
	global patches
	with open(PATCHES_PICKLED) as f:
		print "reading patches data"
		patches = pickle.load(f)
		for i in patches:
			# CREATING FILE BASED DICT {filePath : pwid}
			for j in patches[i]["files"]:
				if j not in PATCH_FILE_MAP:
					PATCH_FILE_MAP[j] = []
				PATCH_FILE_MAP[j].append(i)

	for i in patches:
		auth = patches[i]["author"]
		if auth not in PATCH_AUTHOR_MAP:
			PATCH_AUTHOR_MAP[auth] = []
		PATCH_AUTHOR_MAP[auth].append(i)

def readGit():
	global commits
	global notMatched
	global COMMIT_FILE_MAP
	global COMMIT_AUTHOR_MAP
	# opening commit file map
	with open(COMMIT_MAP) as f:
		print "Reading commit map"
		COMMIT_FILE_MAP = pickle.load(f)
		print len(COMMIT_FILE_MAP), "commits in COMMIT_FILE_MAP"

	# opening commit pickle
	with open(COMMITS_PICKLED) as f:
		print "Reading commit data"
		commits = pickle.load(f)
		print "Found data for:", len(commits)

	# creating cid -> author email map.
	for i in commits:
		COMMIT_AUTHOR_MAP[i] = commits[i]["email"]


def doAuthMapMatching():
	# iterate through the author map
	countNoAuth = 0
	for i in COMMIT_AUTHOR_MAP:
		if COMMIT_AUTHOR_MAP[i] in PATCH_AUTHOR_MAP:
			# print i, PATCH_AUTHOR_MAP[COMMIT_AUTHOR_MAP[i]]
			for j in PATCH_AUTHOR_MAP[COMMIT_AUTHOR_MAP[i]]:
				compareDiffs(i,j)
		else:
			print "not found: ",COMMIT_AUTHOR_MAP[i]
			countNoAuth += 1
	print "not found: ", countNoAuth
	print "COMMIT_AUTHOR_MAP", len(COMMIT_AUTHOR_MAP)
	print "PATCH_AUTHOR_MAP", len(PATCH_AUTHOR_MAP)






def doFileMapMatching():

	# iterate through cid-file map
	for i in COMMIT_FILE_MAP:
		# if i in notMatched: # taking only commits that have NOT been matched by subject
		# for all the files j touched by commit i
		for j in COMMIT_FILE_MAP[i]: 
			# find all PWID that touched that file:
			# Have to check if file is in FILE-PWID map
			if j in PATCH_FILE_MAP:
				for k in PATCH_FILE_MAP[j]:
					if i not in MATCHED_CID and j not in MATCHED_PWID:
						compareDiffs(i,k)
			else:
				print j ,"NOT FOUND"



def compareDiffs(cid,pwid):
	global MATCHED_PWID
	global MATCHED_CID
	doCheck = True

	# git diff:commits[cid]["lines"]
	if cid in commits:
		gitDiff = commits[cid]["lines"]
	else:
		doCheck = False
	# patch diff
	# print patches[pwid]["lines"]
	if pwid in patches:
		pwDiff = patches[pwid]["lines"]
	else:
		print pwid
		doCheck = False

	if doCheck:
		sm=difflib.SequenceMatcher(None,gitDiff,pwDiff)
		ratio = sm.ratio()
		if ratio > MATCH_RATIO:
			MATCHED_CID.add(cid)
			MATCHED_PWID.add(pwid)
			print cid, pwid, sm.ratio()
			if cid not in lineMatches:
				lineMatches[cid] = set([])
			lineMatches[cid].add(pwid)




if __name__ == '__main__':
	start = time.time()

	getSubjectMatches()
	getLineMatches()

	print "MATCHED_PWID:", len(MATCHED_PWID)
	print "MATCHED_CID:", len(MATCHED_CID)

	print "Subject commit matched: ", len(subjectMatches)
	print "lines commit matched: ", len(lineMatches)
	print "subject commits total: ", subjectMatchesCount
	print "len(patches)",len(patches)
	print "len(commits)",len(commits)

	print "Created in", time.time() - start
