"""
This script will create a database containing the first line of the commit message, the commit ID, and the commit time.

How to run:
enter the follwoing command in the linux git repo. The path should be the path to this script. The date is the lower limit of the git log data
git log --no-merges --pretty=format:"%H    %ct    %s" --after={2009-01-01} | python /Users/alexandrecourouble/Desktop/email2git/subject_data_gen/git/commit_subject_generator.py

by Alex Courouble
"""
import sys, sqlite3
DB_PATH = '~/Desktop/email2git_data/commit_subject.db'

# getting data from stdin and storing it in a list of tuples before populating sqlite DB
data = sys.stdin.read()
lines = data.split('\n')
table = []
for i in lines:
	split = i.split('    ')
	if len(split) < 4:
		table.append(tuple(split))



# creating a connection to the DB and inputing the data
conn = sqlite3.connect(DB_PATH) # connecting
conn.text_factory = str
c = conn.cursor() #creating cursor
c.execute('''create table subject(cid char(40), commit_time int, subject text)''') # creating the table
c.executemany('INSERT INTO subject VALUES (?,?,?)', table) # importing all the data
c.execute('CREATE INDEX subjectidx on subject(subject,commit_time)')
c.execute('CREATE INDEX subjectidx2 on subject(cid)')
conn.commit()
conn.close() # we're done!

