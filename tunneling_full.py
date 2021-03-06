#! /usr/bin/python

import os
import sys
import sqlite3
import argparse
import datetime
from datetime import timedelta

tunnel_limit = 15

datetimeFormat = '%Y-%m-%d %H:%M:%S.%f' 

def main(argv):
	parser = argparse.ArgumentParser(description="SQLite3 Extractor")
	parser.add_argument('db',help='SQLite3 Database file')
	args = parser.parse_args()

	if not os.path.isfile(args.db):
		print "Database file not found. Exiting"
		sys.exit()

	DATABASE = sqlite3.connect(args.db)

	cur = DATABASE.cursor()

	cre = cur.execute("SELECT ure_fullname, usne_event_id, COUNT(*)  FROM usn_event_ref WHERE usne_event_id='Creations' GROUP BY ure_fullname, usne_event_id HAVING COUNT(*) > 1 ").fetchall()

	ren_ren = cur.execute("SELECT ure_fullname, usne_event_id, COUNT(*) FROM usn_event_ref WHERE usne_event_id='Renames_Moves' GROUP BY ure_fullname, usne_event_id HAVING COUNT(*) > 1 ").fetchall()

	ren_del = cur.execute("SELECT ure_fullname, usne_event_id, COUNT(*) FROM usn_event_ref WHERE usne_event_id='Renames_Moves' OR usne_event_id='Deletions' GROUP BY ure_fullname HAVING COUNT(*) > 1 ").fetchall()

	cre_files = []

	ren_ren_files = []
	
	ren_del_files = []

	for row in cre:
		cre_files.append(row[0])

	for row in ren_ren:
		ren_ren_files.append(row[0])

	for row in ren_del:
		ren_del_files.append(row[0])

	print len(cre_files), 'creations files to search'
	print len(ren_ren_files), 'rename to rename files to search'
	print len(ren_del_files), 'delete to rename files to search'
	
	suspicious = []	
	
	print 'Searching for create after delete tunneling....'
	
	for fil in cre_files:
		dat2 = cur.execute("SELECT * FROM usn_event_ref WHERE ure_fullname = '"+fil+"' AND usne_event_id='Creations'").fetchall() 
		dat3 = cur.execute("SELECT * FROM usn_event_ref WHERE ure_fullname = '"+fil+"' AND usne_event_id='Deletions'").fetchall() 
		for row2 in dat2:
			date1 = row2[18]
			for row3 in dat3:
				date2 = row3[18]
				diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
				if diff.seconds > 0 and diff.seconds < tunnel_limit:
					suspicious.append(fil)

	if len(suspicious) > 0:	
		print 'The following are suspicious files that should be further investigated for malicious file system tunneling:\n'
		print 'REASON: New file created within tunneling time limit with same name of deleted file\n'
		for sus in suspicious:
			 print sus, '\n'

	else:
		print 'No create after delete tunneling detected'

	suspicious = []	
	
	print 'Searching for create after rename tunneling....'
	
	for fil in cre_files:
		dat2 = cur.execute("SELECT * FROM usn_event_ref WHERE ure_fullname = '"+fil+"' AND usne_event_id='Creations'").fetchall() 
		dat3 = cur.execute("SELECT * FROM usn_event_ref WHERE ure_fullname = '"+fil+"' AND usne_event_id='Renames_Moves'").fetchall() 
		for row2 in dat2:
			date1 = row2[18]
			for row3 in dat3:
				date2 = row3[18]
				diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
				if diff.seconds > 0 and diff.seconds < tunnel_limit:
					suspicious.append(fil)
	if len(suspicious) > 0:	
		print 'The following are suspicious files that should be further investigated for malicious file system tunneling:'
		print 'REASON: New file created within tunneling time limit with same name of renamed file\n'
		for sus in suspicious:
			 print sus, '\n'
	else:
		print 'No create after rename tunneling detected'

	suspicious = []	
	
	print 'Searching for rename after rename tunneling....'

	for fil in ren_ren_files:
		dat2 = cur.execute("SELECT * FROM usn_event_ref WHERE ure_fullname = '"+fil+"' AND usne_event_id='Renames_Moves'").fetchall() 
		dat3 = cur.execute("SELECT * FROM usn_event_ref WHERE ure_fullname = '"+fil+"' AND usne_event_id='Renames_Moves'").fetchall() 
		for row2 in dat2:
			date1 = row2[18]
			for row3 in dat3:
				date2 = row3[18]
				diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
				if diff.seconds > 0 and diff.seconds < tunnel_limit:
					suspicious.append(fil)
	if len(suspicious) > 0:	
		print 'The following are suspicious files that should be further investigated for malicious file system tunneling:\n'
		print 'REASON: File renamed within tunneling time limit with same name of renamed file\n'
		for sus in suspicious:
			 print sus, '\n'
	else:
		print 'No rename after rename tunneling detected'


	suspicious = []	

	print 'Searching for rename after delete tunneling....'

	for fil in ren_del_files:
		dat2 = cur.execute("SELECT * FROM usn_event_ref WHERE ure_fullname = '"+fil+"' AND usne_event_id='Renames_Moves'").fetchall() 
		dat3 = cur.execute("SELECT * FROM usn_event_ref WHERE ure_fullname = '"+fil+"' AND usne_event_id='Deletions'").fetchall() 
		for row2 in dat2:
			date1 = row2[18]
			for row3 in dat3:
				date2 = row3[18]
				diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
				if diff.seconds > 0 and diff.seconds < tunnel_limit:
					suspicious.append(fil)
	if len(suspicious) > 0:	
		print 'The following are suspicious files that should be further investigated for malicious file system tunneling:\n'
		print 'REASON: File renamed within tunneling time limit with same name of deleted file\n'
		for sus in suspicious:
			 print sus, '\n'

	else:
		print 'No rename after delete tunneling detected'


	DATABASE.close()

if __name__ == "__main__":
	main(sys.argv)
