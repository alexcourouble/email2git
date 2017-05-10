"""
how to get the data from db:
mysql -u gitmine -p -h 172.30.200.1 KORG_PATCHWORK -e "select id, submitter_id, content from patchwork_patch where date > '2017-01-01';" > patches_short.txt

This script will go through the output from the wuery and create a lighter file containing the info required for the line-based matching.


"""
# try:
import cPickle as pickle
# except:
#     import pickle

INPUT_FILE_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/raw_data/patches_short.txt'
NAME_MAP_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/raw_data/name_map_short.txt'

OUTPUT_PATH = '/Users/alexandrecourouble/Desktop/email2git_data/PATCHES_PICKLED.txt'

PATCHES = {}
PEOPLE = {}


class Patch:
	def __init__(self, pwid, author, files, lines):
		self.pwid = pwid
		self.author = author
		self.files = files
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
	# limit = 0
	with open(INPUT_FILE_PATH) as f:
		for i in f:
			# limit += 1
			split = i.split("\t")

			# data points:
			pwid = split[0]
			if split[1] in PEOPLE: author = PEOPLE[split[1]]
			files = []
			lines = []

			a = 'h'
			for j in split[2].split("\\n"):
				if j.startswith("+++"): # get file name
						files.append(j.replace("+++ b/",""))
				elif j.startswith("---"): 
					pass
				elif j.startswith("+") or j.startswith("-"):
					lines.append(j)

			PATCHES[pwid] = Patch(pwid, author, files, lines)

			# if limit == 20: break


if __name__ == '__main__':
	getPeople()
	readDataFile()

	out = {}
	for i in PATCHES:

		out[i] = {}
		out[i]["lines"] = PATCHES[i].lines
		out[i]["files"] = PATCHES[i].files
		out[i]["author"] = PATCHES[i].author
		# print PATCHES[i].pwid
		# print PATCHES[i].files
		# print PATCHES[i].author.email

	# print out
	with open(OUTPUT_PATH,"w") as f:
		f.write(pickle.dumps(out))





