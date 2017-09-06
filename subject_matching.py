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
"""

try:
    import cPickle as pickle
except:
    import pickle
    print "Could not import cPickle. Using regular pickle implementation. Expect performance loss."

import sqlite3
import sys


PW_DB = '/home-students/courouble/email2git_data/pwSubject_short.db'
GIT_DB = '/home-students/courouble/email2git_data/commit_subject.db'
OUTPUT = '/home-students/courouble/email2git_data/subject_ouput/SUBJECT_OUTPUT.txt'

MATCHED_CID_OUTPUT = '/home-students/courouble/email2git_data/subject_ouput/matched_cid_pickled.txt'
MATCHED_PWID_OUTPUT = '/home-students/courouble/email2git_data/subject_ouput/matched_pwid_pickled.txt'


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





if sys.argv > 1:
	if "test" in sys.argv:
		OUTPUT ='/Users/alexandrecourouble/Desktop/email2git_data/test_results/SUBJECT_OUTPUT.txt'


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


# MATCHES
with open(OUTPUT, "w") as f:
	f.write(pickle.dumps(subjectMatches))

