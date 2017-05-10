"""

Author: Alex Courouble <alex.courouble@gmail.com>
"""
import sqlite3
import cPickle as pickle

# SUBJECT
PW_DB = '/Users/alexandrecourouble/Desktop/email2git_data/pwSubject_short.db'
GIT_DB = '/Users/alexandrecourouble/Desktop/email2git_data/commit_subject.db'
OUTPUT = '/Users/alexandrecourouble/Desktop/email2git_data/SUBJECT_OUTPUT.txt'

# LINES
PATCHES_PICKLED = '/Users/alexandrecourouble/Desktop/email2git_data/PATCHES_PICKLED.txt'

PATCH_FILE_MAP = {}


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



def readPW():
	with open(PATCHES_PICKLED) as f:
		patches = pickle.load(f)
		for i in patches:
			print i, patches[i]["author"]
			print patches[i]["files"]


			# CREATING FILE BASED DICT {filePath : pwid}
			for j in patches[i]["files"]:
				if j not in PATCH_FILE_MAP:
					PATCH_FILE_MAP[j] = []
				PATCH_FILE_MAP[j].append(i)

	print PATCH_FILE_MAP
	print len(PATCH_FILE_MAP)







if __name__ == '__main__':
	# getSubjectMatches()


	getLineMatches()