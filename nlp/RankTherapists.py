import getpass
import sqlite3
import os
import operator

#Input is a list of tuples ex. [("category",score)]
def rank(categoryAndWeight):
	# Create a map from categories to scores.
	weights = {}
	for i in range(len(categoryAndWeight)):
		weights[categoryAndWeight[i][0]] = categoryAndWeight[i][1]

	dir_path = os.path.dirname(os.path.abspath(__file__))
	# full_path = os.path.join(dir_path, '../database.db')
	full_path = os.path.join(dir_path, '../Theratree/db/development.sqlite3')
	conn = sqlite3.connect(full_path)
	cur = conn.cursor()

	cur.execute('SELECT therapist_id from therapists')
	ids = cur.fetchall()

	scores = {}
	#Loop through all therapists in db
	for row in ids:
		th_id = row[0]
		cur.execute('SELECT specialty FROM th_specialties WHERE therapist_id = ' + str(th_id))
		specialties = cur.fetchall()
		scores[th_id] = 0
		for s in specialties:
			s = s[0].lower()
			scores[th_id] += (weights[s]/len(specialties)) if s in weights else 0

	#Return therapist ids sorted in descending order of score
	sorted_x = [x[0] for x in sorted(scores.items(), key=operator.itemgetter(1), reverse = True)]
	return sorted_x




