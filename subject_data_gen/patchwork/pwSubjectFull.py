"""
Script used to create a DB from the patchwork email subject data dump.

By Alex Courouble
"""
import sqlite3
DB_PATH = 'pwSubjectFull.db'

table = []

with open("subject_full.txt","r") as s:
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