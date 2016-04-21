import cPickle as pickle
from scipy.sparse import csr_matrix
import numpy as np
# assume we have a tf-idf table
# take a natural string query of undefined length
# categorize naively, if failure, then reprompt to add information or select category
# returns a vector 
def classify_query(query, tfidf_file, wordcount_file):
	#reconstruct tf-idf matrix
	with open('tfidf_sparse.dat', 'rb') as f:
		X = pickle.load(f)
	X = X.todense()

	words, categories, word_to_index = build_word_to_index_map(wordcount_file)
	q = build_query_vector(query, word_to_index)

	membership_scores = np.dot(X,q)
	membership_scores = np.squeeze(np.asarray(membership_scores))
	together = zip(membership_scores, categories)
	return sorted(together)

#constructs a word_count vector for the query based on all the words from all the categories
def build_query_vector(query, word_to_index):
	query_words = query.split() #todo: stem words
	q = np.zeros(len(word_to_index))
	for word in query_words:
		if word in word_to_index:
			q[word_to_index[word]]+= 1
	return q

#build array of words, array of categories, and map from word to corresponding tf-idf index
def build_word_to_index_map(wordcount_file):
	f = open(wordcount_file, 'r')
	words = f.readline().strip().split(',')
	word_to_index = {}
	for i in range(len(words)):
		word_to_index[words[i]] =  i
	categories = []
	for line in f: 
		categories.append(line.split(',')[0])
	return words, categories, word_to_index




		
