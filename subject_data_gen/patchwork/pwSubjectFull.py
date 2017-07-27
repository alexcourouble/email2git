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




Script used to create a DB from the patchwork email subject data dump.

in PWDB: "select id, name from patchwork_patch"

By Alex Courouble
"""
import sqlite3, os
INPUT_FILE_PATH = '/home-students/courouble/email2git_data/raw_data/subject_pw.txt'
DB_PATH = '/home-students/courouble/email2git_data/pwSubject_short.db'


table = []

with open(INPUT_FILE_PATH,"r") as s:
	for i in s:
		patchData = i.split("\t")
		patchId = patchData[0] 
		patchSubject =  patchData[1]
		# print patchId,"	",patchSubject
		table.append((patchId,patchSubject))

if os.path.isfile(DB_PATH):
	os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH) # connecting
conn.text_factory = str
c = conn.cursor() #creating cursor
c.execute('''create table subject(pwid int, subject text)''') # creating the table
c.executemany('INSERT INTO subject VALUES (?,?)', table) # importing all the data
conn.commit()
conn.close() # we're done!