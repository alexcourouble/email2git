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


PATCH_FILE_MAP = {}
COMMIT_FILE_MAP = {}

patches = {}
commits = {}

foundCount = 0
foundSet = set([])

fileNotFound = set([])

def getSubjectMatches():
	connGIT = sqlite3.connect(GIT_DB) # connecting
	connGIT.text_factory = str
	cg = connGIT.cursor() #creating cursor

	gitCommits = {}
	for row in cg.execute('select * from subject'):
		gitCommits[row[0]] = (row[1],row[2])

	connGIT.close()


	notMatched = [] # list containing all cids that weren't matched
	connPW = sqlite3.connect(PW_DB) # connecting
	connPW.text_factory = str
	cp = connPW.cursor() # creating cursor

	with open(OUTPUT,"w") as matches: # opening file for writting subject matches
		for i in gitCommits:
			string = '%'+gitCommits[i][1]+'%'
			count = 0
			for j in cp.execute("""select * from subject where subject like ?;""", (string,)):
				# print str(j[0])+','+i
				matches.write(str(j[0])+','+i+'\n')
				count += 1
			if count == 0: notMatched.append(i)

	# printing remaining cids
	connPW.close()
		
	# with open(OUTPUT,"w") as no_match:
	# 	for i in notMatched:
	# 		no_match.write(i+"\n")


def getLineMatches():
	readPW()
	readGit()
	# doMatching()



def readPW():
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
	# for i in patches:
	# 	print type(i)


def readGit():
	global commits
	global fileNotFound
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

		for i in commits:
			print i

	# iterate through cid-file map
	for i in COMMIT_FILE_MAP:
		# for all the files j touched by commit i
		for j in COMMIT_FILE_MAP[i]:
			# find all PWID that touched that file:
			# Have to check if file is in FILE-PWID map
			if j in PATCH_FILE_MAP:
				for k in PATCH_FILE_MAP[j]:

					compareDiffs(i,k)

					# pass
			else:
				print j ,"NOT FOUND"
				fileNotFound.add(j)



def compareDiffs(cid,pwid):
	global foundCount
	global foundSet
	

	doCheck = True

	# CHECK AUthor EMAIL???
	# git diff:
	# print commits[cid]["lines"]
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
		if ratio > .2:
			foundCount += 1
			foundSet.add(cid)
			print cid, pwid, sm.ratio()



if __name__ == '__main__':
	start = time.time()
	# getSubjectMatches()
	getLineMatches()

	print "len(fileNotFound)",len(fileNotFound)

	print "foundCount",foundCount
	print "foundSet", len(foundSet)
	print "len(patches)",len(patches)
	print "len(commits)",len(commits)

	print "Created in", time.time() - start
