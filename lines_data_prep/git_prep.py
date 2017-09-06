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



Reading the a customised git log output

To get files touched by commits:
	git log --no-merges --name-only --pretty=oneline --after="2009-01-01" > ~/Desktop/email2git_data/raw_data/git_file_map.txt

To get the commit diffs:
	git log -p --no-merges --pretty=format:"%H;%an;%ae;%ct;%at" --after="2009-01-01" > ~/Desktop/email2git_data/raw_data/commits_short.txt

"""
import re
import cPickle as pickle
import sys
import sqlite3

class Commit:
	def __innit__(self,cid,name,email,lines,commitTime, authorTime):
		self.cid = cid
		self.name = name
		self.email = email
		self.lines = lines
		self.commitTime = commitTime
		self.authorTime = authorTime

# MATCHED_CID_INPUT = '/Users/alexandrecourouble/Desktop/email2git_data/subject_ouput/matched_cid_pickled.txt'
MATCHED_CID_INPUT = '/home-students/courouble/email2git_data/subject_ouput/matched_cid_pickled.txt'

# INPUT_CID_FILE_MAP = "/Users/alexandrecourouble/Desktop/email2git_data/raw_data/git_file_map.txt"
INPUT_CID_FILE_MAP = "/home-students/courouble/email2git_data/raw_data/git_file_map.txt"
# INPUT_COMMIT_FILE = "/Users/alexandrecourouble/Desktop/email2git_data/raw_data/commits_short.txt"
INPUT_COMMIT_FILE = "/home-students/courouble/email2git_data/raw_data/commits_short.txt"
# PERSONS_DB = '/Users/alexandrecourouble/Desktop/email2git_data/linux_persons.db'
PERSONS_DB = '/home-students/courouble/email2git_data/linux_persons.db'

# OUTPUT_MAP = "/Users/alexandrecourouble/Desktop/email2git_data/COMMIT_MAP_PICKLED.txt"
OUTPUT_MAP = "/home-students/courouble/email2git_data/COMMIT_MAP_PICKLED.txt"
# OUTPUT_COMMITS = "/Users/alexandrecourouble/Desktop/email2git_data/COMMITS_PICKLED_test.txt"
OUTPUT_COMMITS = "/home-students/courouble/email2git_data/COMMITS_PICKLED_test.txt"

COMMIT_FILE_MAP = {}

COMMITS = {}

persons = {}

def readCIDMap():
	with open(INPUT_CID_FILE_MAP) as f:
		currentCommit = ""
		for i in f:
			line = i.strip("\n")
			if re.match(r'\b[0-9a-f]{40}\b', line):
				currentCommit = line[:40]
				if currentCommit not in MATCHED_CID:
					COMMIT_FILE_MAP[currentCommit] = []
			else:
				if currentCommit in COMMIT_FILE_MAP:
					COMMIT_FILE_MAP[currentCommit].append(line)


def readCommits():
	unique_people_id_email = {}
	unique_people_id_name = {}
	# reading persons DB
	conn = sqlite3.connect(PERSONS_DB)
	c = conn.cursor()
	for i in c.execute("SELECT personid, name, lcemail FROM persons"):
		email = i[2].replace("<","").replace(">","")
		unique_people_id_email[email] = i[0]
		unique_people_id_name[i[1]] = i[0]
	conn.close()

	with open(INPUT_COMMIT_FILE) as f:
		cid = ""
		authorName = ""
		authorEmail = ""
		commitTime = ""
		authorTime = ""
		personid = ""
		lines = []

		for i in f:
			line = i.strip("\n")
			if re.match(r'\b[0-9a-f]{40}\b', line):
				# submit previously found data
				if cid != "" and cid not in MATCHED_CID:
					# COMMITS[cid] = Commit(cid,authorName,authorEmail,lines)
					COMMITS[cid] = {"name":authorName,"email":authorEmail,"lines":lines,"commitTime":commitTime,"authorTime":authorTime,"personid":personid}
				# create next commit and reset LINES
				split = line.split(";")
				cid = split[0]
				authorName = split[1]
				authorEmail = split[2]
				commitTime = split[3]
				authorTime = split[4]
				if authorEmail in unique_people_id_email:
					personid = unique_people_id_email[authorEmail]
				elif authorName in unique_people_id_name:
					personid = unique_people_id_name[authorName]
				else:
					personid = authorEmail
				lines = []
			elif line.startswith("+++") or line.startswith("---"):
				pass
			elif line.startswith("+") or line.startswith("-"):
				lines.append(line)


if __name__ == '__main__':

	if sys.argv > 1:
		if "test" not in sys.argv:

			# opening matched cid set from subject matching
			with open(MATCHED_CID_INPUT) as f:
				MATCHED_CID = pickle.load(f)
				print "Read", len(MATCHED_CID), "subject matched cid. Type:" , type(MATCHED_CID)

		elif "test" in sys.argv:
			MATCHED_CID = set([])

	readCIDMap()
	readCommits()

	with open(OUTPUT_MAP,"w") as f:
		f.write(pickle.dumps(COMMIT_FILE_MAP))

	with open(OUTPUT_COMMITS,"w") as f:
		f.write(pickle.dumps(COMMITS))	


	print COMMIT_FILE_MAP
	print len(COMMIT_FILE_MAP)
