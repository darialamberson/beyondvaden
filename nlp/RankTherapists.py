import psycopg2
import getpass

#Input is a list of tuples ex. [("category",score)]
def rank(categoryAndWeight):
	# Create a map from categories to scores.
	weights = {}
	for i in range(len(categoryAndWeight)):
		weights[categoryAndWeight[i][0]] = categoryAndWeight[i][1]

	try:
		conn = psycopg2.connect("dbname='therapists' user='%s' host='localhost' password=''" %(getpass.getuser()))
	except:
	    print "I am unable to connect to the database"
	cur = conn.cursor()

	cur.execute("""SELECT id from therapists""")
	ids = cur.fetchall()

	#Allocate array to hold therapist scores
	scores = [0 for i in range(ids[len(ids)-1][0] + 1)]

	#Loop through all therapists in db
	for row in ids:
		th_id = row[0]
		#Compute score for therapist
		cur.execute("""SELECT specialty FROM th_specialties WHERE therapist_id = %s""", [th_id])
		specialties = cur.fetchall()
		for s in specialties:
			s = s[0].lower()
			scores[th_id] += (weights[s]/len(specialties)) if s in weights else 0
	return [i[0] for i in sorted(enumerate(scores), key=lambda x:x[1], reverse=True)]




