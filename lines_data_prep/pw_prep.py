"""
how to get the data from db:
mysql -u gitmine -p -h 172.30.200.1 KORG_PATCHWORK -e "select id, submitter_id, content from patchwork_patch where date > '2017-01-01';" > patches_short.txt

mysql -u gitmine -p -h 172.30.200.1 KORG_PATCHWORK -e "select id, submitter_id, content from patchwork_patch where date > '2016-10-01';" > patches_short.txt

This script will go through the output from the wuery and create a lighter file containing the info required for the line-based matching.


"""
# try:
import cPickle as pickle
# except:
#     import pickle

MATCHED_PWID_INPUT = '/Users/alexandrecourouble/Desktop/email2git_data/subject_ouput/matched_pwid_pickled.txt'

INPUT_FILE_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/raw_data/patches_short_time.txt'
NAME_MAP_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/raw_data/name_map_short.txt'

OUTPUT_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/PATCHES_PICKLED_test.txt'

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
	def __init__(self, pid, name, email):
		self.pid = pid
		self.name = name
		self.email = email


def getPeople():
	with open(NAME_MAP_PATH) as f:
		for i in f:
			split = i.strip("\n").split("\t")
			# id, name, email
			PEOPLE[split[0]] = People(split[0],split[2],split[1])


def readDataFile():
	global PATCHES
	global PEOPLE
	# limit = 0
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


if __name__ == '__main__':
	# opening matched pwid set from subject matching
	with open(MATCHED_PWID_INPUT) as f:
		MATCHED_PWID = pickle.load(f)
		print "Read", len(MATCHED_PWID), "subject matched PWID. Type:" , type(MATCHED_PWID)


	getPeople()
	readDataFile()

	out = {}
	for i in PATCHES:

		out[i] = {}
		out[i]["lines"] = PATCHES[i].lines
		out[i]["files"] = PATCHES[i].files
		out[i]["time"] = PATCHES[i].time
		out[i]["author"] = PATCHES[i].author.email
		# print PATCHES[i].pwid
		# print PATCHES[i].files
		# print PATCHES[i].author.email

	# print out
	with open(OUTPUT_PATH,"w") as f:
		f.write(pickle.dumps(out))





