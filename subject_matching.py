try:
    import cPickle as pickle
except:
    import pickle
    print "Could not import cPickle. Using regular pickle implementation. Expect performance loss."

import sqlite3



PW_DB = '/Users/alexandrecourouble/Desktop/email2git_data/pwSubject_short.db'
GIT_DB = '/Users/alexandrecourouble/Desktop/email2git_data/commit_subject.db'
OUTPUT = '/Users/alexandrecourouble/Desktop/email2git_data/subject_ouput/SUBJECT_OUTPUT.txt'

MATCHED_CID_OUTPUT = '/Users/alexandrecourouble/Desktop/email2git_data/subject_ouput/matched_cid_pickled.txt'
MATCHED_PWID_OUTPUT = '/Users/alexandrecourouble/Desktop/email2git_data/subject_ouput/matched_pwid_pickled.txt'


subjectMatches = {}

MATCHED_PWID = set([])
MATCHED_CID = set([])

def getSubjectMatches():
	print "Finding subject matches"

	connGIT = sqlite3.connect(GIT_DB) # connecting
	connGIT.text_factory = str
	cg = connGIT.cursor() #creating cursor
	gitCommits = {}
	for row in cg.execute('select * from subject'):
		gitCommits[row[0]] = (row[1],row[2])
	connGIT.close()

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

	# printing remaining cids
	connPW.close()

getSubjectMatches()

print "Matched ", len(MATCHED_CID), "commits"
print "Matched ", len(MATCHED_PWID), "patches"

# Outputing data:
# matched cids:
with open(MATCHED_CID_OUTPUT, "w") as f:
	f.write(pickle.dumps(MATCHED_CID))

# matched pwid:
with open(MATCHED_PWID_OUTPUT, "w") as f:
	f.write(pickle.dumps(MATCHED_PWID))

