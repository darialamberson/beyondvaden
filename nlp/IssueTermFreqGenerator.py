# Requires packages: html2text, bs4, google

db_name = '../database.db'
num_articles = 10
logging = True #logging output to check what kinds of results we're getting

import sqlite3
import html2text
import urllib2
import re
import ast
from PorterStemmer import PorterStemmer
from google import search
from collections import Counter

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #Sets python to look for things in the parent directory
import db_connector as db

h = html2text.HTML2Text()
h.ignore_links = True
stemmer = PorterStemmer()
tf_folder_path = os.path.join(os.getcwd(), 'tf')
corpus = set()
pause_time=0.5

if logging:
	log = open('tf-log', 'w')

# Step 1: Find all distinct specialty classes.
connection = sqlite3.connect(db_name)
c = connection.cursor()
db.select(c, ['specialty'], 'th_specialties', distinct=True)
issues = set(str(re.sub(r'[^a-zA-Z]+', ' ', i[0])).lower() for i in c.fetchall())
#issues = [str(re.sub(r'[^a-zA-Z]+', ' ', i[0])).lower() for i in c.fetchall()][0:3]
connection.close()
if logging:
	log.write("Issues: \n")
	log.write(', '.join(issues))
	log.write('\n\n')

print "Step 1 complete."

# Step 2: For each category, find the top num_articles google results and generate tf counts of the stemmed plaintext.

for issue in issues:
	results = search(issue, stop = num_articles, pause=pause_time)
	urls = [str(url) for url in results][:num_articles]
	
	if logging:
		print issue
		log.write('Issue: ' + issue + '\n')
		log.write('\n'.join(urls))
		log.write('\n\n')

	cumulative = []

	for url in urls:
		if not url.endswith('.pdf'):
			try:
				html = urllib2.urlopen(url) #gets the raw html of the url
				plaintext = h.handle(unicode(html.read(), 'ISO-8859-1')) #converts the html into plaintext
				processed = re.sub(r'[^a-zA-Z]+', ' ', plaintext)
				#print processed
				stemmed = [str(stemmer.stem(word.lower())) for word in processed.split()]
				cumulative += stemmed
			except:
				pass
	counts = Counter(cumulative)
	tf = open(os.path.join(tf_folder_path, issue), 'w')

	for word in sorted(counts.keys()): #sort words in alphabetical order
		if len(word) < 15:
			corpus.add(word)
			tf.write(str((word, counts[word]))) #write tuples of words with the word count
			tf.write('\n')

	tf.close()

print "Step 2 complete."

# Step 3: Combine files

files = sorted(issues)
num_files = len(files)
count_vectors = {}
for word in corpus:
	count_vectors[word] = [0]*num_files

# Flesh out count_vectors
for i in range(len(files)):
	curr = open(os.path.join(tf_folder_path, files[i]), 'r')
	for line in curr.readlines():
		pair = ast.literal_eval(line)
		count_vectors[pair[0]][i] = pair[1]
	curr.close()

# Write to tf_matrix
tf_matrix = open('tf_matrix.csv', 'w')
tf_matrix.write(','.join(files))
tf_matrix.write('\n')

for word in sorted(count_vectors.keys()):
	line = word + ',' + ','.join([str(num) for num in count_vectors[word]])
	tf_matrix.write(line)
	tf_matrix.write('\n')
tf_matrix.close()

print "Step 3 complete."
	
if logging:
	log.close()