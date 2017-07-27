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




how to get the data from db:
mysql -u gitmine -p -h 172.30.200.1 KORG_PATCHWORK -e "select id, submitter_id, content from patchwork_patch where date > '2017-01-01';" > patches_short.txt

mysql -u gitmine -p -h 172.30.200.1 KORG_PATCHWORK -e "select id, submitter_id, content from patchwork_patch where date > '2016-10-01';" > patches_short.txt

This script will go through the output from the wuery and create a lighter file containing the info required for the line-based matching.


"""
# try:
import cPickle as pickle
import sqlite3
import sys
# except:
#     import pickle

# reading pwid that were already matched (no need to include them)


# MATCHED_PWID_INPUT = '/Users/alexandrecourouble/Desktop/email2git_data/subject_ouput_tmp/matched_pwid_pickled.txt'

# INPUT_FILE_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/raw_data/patches_short_time.txt'
# NAME_MAP_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/raw_data/name_map_short.txt'
# PERSONS_DB = '/Users/alexandrecourouble/Desktop/email2git_data/linux_persons.db'

# OUTPUT_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/PATCHES_PICKLED_test.txt'
# DB_PATH = "/Users/alexandrecourouble/Desktop/email2git_data/lookupDB.db"


MATCHED_PWID_INPUT = '/home-students/courouble/email2git_data/subject_ouput_tmp/matched_pwid_pickled.txt'

INPUT_FILE_PATH = '/home-students/courouble/email2git_data/raw_data/patches_short_time.txt'
NAME_MAP_PATH = '/home-students/courouble/email2git_data/raw_data/name_map_short.txt'
PERSONS_DB = '/home-students/courouble/email2git_data/linux_persons.db'

OUTPUT_PATH = '/home-students/courouble/email2git_data/PATCHES_PICKLED_test.txt'
DB_PATH = "/home-students/courouble/email2git_data/lookupDB.db"


PATCHES = {}
PEOPLE = {}


class Patch:
	def __init__(self, pwid, author, files, time, lines):
		self.pwid = pwid
		self.author = author
		self.files = files
		self.time = time
		self.lines = lines


class People:
	def __init__(self, pid, name, email, personid):
		self.pid = pid
		self.name = name
		self.email = email
		self.personid = personid # personid found in DMG's people DB


def getPeople():
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


	with open(NAME_MAP_PATH) as f:
		for i in f:
			personid = ""
			split = i.strip("\n").split("\t")
			if split[1] in unique_people_id_email:
				personid = unique_people_id_email[split[1]]
			elif split[2] in unique_people_id_name:
				personid = unique_people_id_name[split[2]]
			else:
				personid = split[1]

			# id, name, email, personid
			PEOPLE[split[0]] = People(split[0],split[2],split[1],personid)


def readDataFile():
	global PATCHES
	global PEOPLE
	# limit = 0
	countNoAuthor = 0
	with open(INPUT_FILE_PATH) as f:
		for i in f:
			# limit += 1
			split = i.split("\t")
			# print split
			if len(split) > 1:
				# data points:
				pwid = split[0]
				if split[1] in PEOPLE: 
					author = PEOPLE[split[1]]
				else:
					author = People("","","","")
					countNoAuthor += 1
				time = split[2]
				files = []
				lines = []

				if pwid not in MATCHED_PWID:
					a = 'h'
					for j in split[3].split("\\n"):
						if j.startswith("+++"): # get file name
								files.append(j.replace("+++ b/",""))
						elif j.startswith("---"): 
							pass
						elif j.startswith("+") or j.startswith("-"):
							lines.append(j)

					PATCHES[pwid] = Patch(pwid, author, files, time, lines)

				# if limit == 20: break
	print "Could not find: ", countNoAuthor


if __name__ == '__main__':

	if sys.argv > 1:
		if "test" not in sys.argv:
			# opening matched pwid set from subject matching
			with open(MATCHED_PWID_INPUT) as f:
				MATCHED_PWID = pickle.load(f)
				print "Read", len(MATCHED_PWID), "subject matched PWID. Type:" , type(MATCHED_PWID)
		elif "test" in sys.argv:
			MATCHED_PWID = set([])


	getPeople()
	readDataFile()

	out = {}
	table = []
	for i in PATCHES:

		out[i] = {}
		out[i]["lines"] = PATCHES[i].lines
		out[i]["files"] = PATCHES[i].files
		out[i]["time"] = PATCHES[i].time
		out[i]["author"] = PATCHES[i].author.personid

		table.append((int(i),PATCHES[i].time))
		

	# print out
	with open(OUTPUT_PATH,"w") as f:
		f.write(pickle.dumps(out))

	# creating db for faster pwid lookup

	conn = sqlite3.connect(DB_PATH) # connecting
	conn.text_factory = str
	c = conn.cursor() #creating cursor
	c.execute('''create table lines(pwid int, date date)''') # creating the table
	c.executemany('INSERT INTO lines VALUES (?,?)', table) # importing all the data
	conn.commit()
	conn.close() # we're done!





