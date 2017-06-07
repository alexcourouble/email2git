"""
reading and comparing matches outputed by subject and line
"""
import pickle
try:
    import cPickle as pickle
except:
    import pickle
    print "Could not import cPickle. Using regular pickle implementation. Expect performance loss."


subject_matches = "/Users/alexandrecourouble/Desktop/email2git_data/test_results/SUBJECT_OUTPUT.txt"
lines_matches = '/Users/alexandrecourouble/Desktop/email2git_data/test_results/LINES_OUTPUT.txt'

subject = {}
subject_set = set([])

lines = {}
lines_set = set([])

# reading subject matches
with open(subject_matches) as f:
	subject = pickle.load(f)

# populating set with unique match string (cid + pwid)
nmb_s_matches = 0
for i in subject:
	for j in subject[i]:
		subject_set.add(i+j)
		nmb_s_matches += 1

with open(lines_matches) as f:
	lines = pickle.load(f)

count = 0
nmb_l_matches = 0
for i in lines:
	for j in lines[i]:
		nmb_l_matches += 1
		if i+j in subject_set:
			count += 1 

print count

print "Number of SUBJECT matches :", nmb_s_matches
print "Number of LINES matches :", nmb_l_matches