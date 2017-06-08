"""
Script used to create a DB from the patchwork email subject data dump.

in PWDB: "select id, name from patchwork_patch"

By Alex Courouble
"""
import sqlite3
INPUT_FILE_PATH = '/home-students/courouble/email2git_data/raw_data/subject_pw.txt'
DB_PATH = '/home-students/courouble/email2git_data/pwSubject_short.db'


table = []

with open(INPUT_FILE_PATH,"r") as s:
	for i in s.read().split('\n'):
		patchData = i.split("\t")
		patchId = patchData[0] 
		patchSubject =  patchData[1]
		# print patchId,"	",patchSubject
		table.append((patchId,patchSubject))

conn = sqlite3.connect(DB_PATH) # connecting
conn.text_factory = str
c = conn.cursor() #creating cursor
c.execute('''create table subject(pwid int, subject text)''') # creating the table
c.executemany('INSERT INTO subject VALUES (?,?)', table) # importing all the data
conn.commit()
conn.close() # we're done!