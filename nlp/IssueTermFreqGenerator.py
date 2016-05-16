# Requires packages: html2text, bs4, google

db_name = '../database.db'
default_filename = 'tf_matrix.csv'
num_articles = 10
logging = True #logging output to check what kinds of results we're getting
check_validity = True #filters out words that don't appear in the valid_words_file
#valid_words_file = 'google-10000-english-master/google-10000-english.txt'
stop_words_file = 'stopwords.txt'
extra_search_keywords = ''
valid_words_file = 'google-10000-english-master/20k.txt'

import shutil
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

def main(filename, crashed=False): #"crashed" is an option to continue from the current state if the requests time out
	#print filename
	#print crashed

	h = html2text.HTML2Text()
	h.ignore_links = True
	stemmer = PorterStemmer()
	tf_folder_path = os.path.join(os.getcwd(), 'tf')
	if not os.path.exists(tf_folder_path):
		os.mkdir(tf_folder_path)
	corpus = set()
	pause_time = 0.5

	if check_validity:
		valid_words = set(str(stemmer.stem(line.rstrip().lower())) for line in open(valid_words_file, 'r'))
		stop_words = set(str(stemmer.stem(line.rstrip().lower())) for line in open(stop_words_file, 'r'))
		keywords = set(str(stemmer.stem(word.lower()) for word in extra_search_keywords.split()))
		stop_words = stop_words.union(keywords)

	if logging:
		log = open('tf-log', 'w')

	# Step 1: Find all distinct specialty classes.
	connection = sqlite3.connect(db_name)
	c = connection.cursor()
	db.select(c, ['specialty'], 'th_specialties', distinct=True)
	issues = set(str(re.sub(r'[^a-zA-Z]+', ' ', i[0])).lower() for i in c.fetchall())
	connection.close()
	if logging:
		log.write("Issues: \n")
		log.write(', '.join(issues))
		log.write('\n\n')

	print "Step 1 complete."

	# Step 2: For each category, find the top num_articles google results and generate tf counts of the stemmed plaintext.

	if crashed:
		completed = set(f for f in os.listdir(tf_folder_path) if os.path.isfile(os.path.join(tf_folder_path, f)))
		issues = issues - completed
		#print issues

	for issue in issues:
		results = search(issue + ' ' + extra_search_keywords, stop = num_articles, pause = pause_time)
		urls = [str(url) for url in results][: num_articles]
		
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
					if check_validity:
						for word in processed.split():
							processed = str(stemmer.stem(word.lower()))
							if processed not in stop_words and processed in valid_words:
								cumulative.append(processed)
					else:
						stemmed = [str(stemmer.stem(word.lower())) for word in processed.split()]
						cumulative += stemmed
				except: #mostly to ignore urllib2 errors...
					pass
		counts = Counter(cumulative)
		tf = open(os.path.join(tf_folder_path, issue), 'w')

		for word in sorted(counts.keys()): #sort words in alphabetical order
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
	tf_matrix = open(filename, 'w')
	tf_matrix.write(','.join(files))
	tf_matrix.write('\n')

	for word in sorted(count_vectors.keys()):
		line = word + ',' + ','.join([str(num) for num in count_vectors[word]])
		tf_matrix.write(line)
		tf_matrix.write('\n')
	tf_matrix.close()

	shutil.rmtree(tf_folder_path) #removes intermediates!

	print "Step 3 complete."
		
	if logging:
		log.close()


if __name__ == '__main__':
	filename = sys.argv[1] if len(sys.argv) > 1 else default_filename
	crashed = sys.argv[2] if len(sys.argv) > 2 else False
	main(filename, crashed)