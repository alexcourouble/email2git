"""
Author: Alex Courouble <alex.courouble@gmail.com>
"""
import sqlite3
import cPickle as pickle
import difflib
import time

# LINES
PATCHES_PICKLED = '/Users/alexandrecourouble/Desktop/email2git_data/PATCHES_PICKLED_test.txt'
COMMITS_PICKLED = '/Users/alexandrecourouble/Desktop/email2git_data/COMMITS_PICKLED_test.txt'
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




def getLineMatches():
	readPW()
	readGit()
	doAuthMapMatching()
	doFileMapMatching()
	doBruteMatching()


def readPW():
	global PATCH_AUTHOR_MAP
	global patches
	with open(PATCHES_PICKLED) as f:
		print "Reading patches data"
		patches = pickle.load(f)
		for i in patches:
			# CREATING FILE BASED DICT {filePath : pwid}
			for j in patches[i]["files"]:
				filename = j
				if filename not in PATCH_FILE_MAP:
					PATCH_FILE_MAP[filename] = []
				PATCH_FILE_MAP[filename].append(i)

	for i in patches:
		auth = patches[i]["author"]
		if auth not in PATCH_AUTHOR_MAP:
			PATCH_AUTHOR_MAP[auth] = []
		PATCH_AUTHOR_MAP[auth].append(i)
	print 'Found:',len(patches),"patches."

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
		print "Found:", len(commits), "commits"

	# creating cid -> author email map.
	for i in commits:
		COMMIT_AUTHOR_MAP[i] = commits[i]["email"]


def doAuthMapMatching():
	global MATCHED_PWID
	global MATCHED_CID
	print "Starting author map based line matches"





	# iterate through the author map
	countNoAuth = 0
	for i in COMMIT_AUTHOR_MAP:
		if COMMIT_AUTHOR_MAP[i] in PATCH_AUTHOR_MAP:
			# print i, PATCH_AUTHOR_MAP[COMMIT_AUTHOR_MAP[i]]
			for j in PATCH_AUTHOR_MAP[COMMIT_AUTHOR_MAP[i]]:
				compareDiffs(i,j,MATCH_RATIO)
		else:
			# print "not found: ",COMMIT_AUTHOR_MAP[i]
			countNoAuth += 1
	print "number of commits in author map:", len(COMMIT_AUTHOR_MAP)
	print "not found: ", countNoAuth
	print "len(MATCHED_CID)", len(MATCHED_CID)
	print "len(MATCHED_PWID)", len(MATCHED_PWID)




def doFileMapMatching():
	global MATCHED_PWID
	global MATCHED_CID
	print "Starting file map based line matches"
	countNoFile = 0
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
						compareDiffs(i,k,MATCH_RATIO)
			else:
				# print j ,"NOT FOUND"
				countNoFile += 1

	print "not found: ", countNoFile
	print "len(MATCHED_CID)", len(MATCHED_CID)
	print "len(MATCHED_PWID)", len(MATCHED_PWID)


def doBruteMatching():
	print "Starting brute force matching on remaining of matches"
	global MATCHED_PWID
	global MATCHED_CID
	for i in commits:
		if i not in MATCHED_CID:
			for j in patches.keys():
				if j not in MATCHED_PWID:
					compareDiffs(i,j,.5)


def compareDiffs(cid,pwid, threshold):
	global MATCHED_PWID
	global MATCHED_CID
	global commits
	global patches
	doCheck = True

	# git diff:commits[cid]["lines"]
	if cid in commits:
		gitDiff = commits[cid]["lines"]
	else:
		doCheck = False
	# patch diff: patches[pwid]["lines"]
	if pwid in patches:
		pwDiff = patches[pwid]["lines"]
	else:
		# print pwid
		doCheck = False

	if doCheck:
		# print 'commits[cid]["time"],patches[pwid]["time"]', commits[cid]["time"], patches[pwid]["time"]
		# print commits[cid]["authorTime"], patches[pwid]["time"], commits[cid]["commitTime"]
		if patches[pwid]["time"] != "NULL":
			if int(commits[cid]["commitTime"]) < int(patches[pwid]["time"]) and int(patches[pwid]["time"]) > int(commits[cid]["authorTime"]) - 86400:
				doCheck = False

	if doCheck:
		sm=difflib.SequenceMatcher(None,gitDiff,pwDiff)
		ratio = sm.ratio()
		if ratio > threshold:
			MATCHED_CID.add(cid)
			MATCHED_PWID.add(pwid)
			if len(MATCHED_CID) % 10 == 0:
				print len(MATCHED_CID)
			# print cid, pwid, ratio
			if cid not in lineMatches:
				lineMatches[cid] = set([])
			lineMatches[cid].add(pwid)

			# remove and pwid from the dict
			del patches[pwid]



if __name__ == '__main__':
	start = time.time()

	getLineMatches()

	print "MATCHED_PWID:", len(MATCHED_PWID)
	print "MATCHED_CID:", len(MATCHED_CID)

	# print "Subject commit matched: ", len(subjectMatches)
	# print "lines commit matched: ", len(lineMatches)
	# print "subject commits total: ", subjectMatchesCount
	print "len(patches)", len(patches)
	print "len(commits)", len(commits)

	print "Created in", time.time() - start

	# with open("subjectMatches.txt") as f:
	# 	f.write(pickle.dumps(subjectMatches))

	# with open("lineMatches.txt") as f:
	# 	f.write(pickle.dumps(lineMatches))
