from numpy import genfromtxt
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import csr_matrix
import numpy as np
import math
import os
from PorterStemmer import PorterStemmer
import cPickle as pickle


class CategoryClassifier(object):


	def __init__(self, tf_file, tfidf_file, idf_file):
		if not os.path.isfile(tfidf_file):
			print '**** Creating tfidf files \n'
			self.createTfidfFiles(tf_file, tfidf_file, idf_file)

		with open(tf_file, 'r') as f:
			self.categories = f.readline().strip().split(',')
			self.word_to_index = {}
			i = 0
			for line in f: 
			 	word = line.split(',')[0]
			 	self.word_to_index[word] = i
			 	i += 1

		with open(tfidf_file, 'rb') as infile:
		 	self.tfidf_matrix = pickle.load(infile).todense()
		
		self.idf = genfromtxt(idf_file, delimiter = ',')


	def createTfidfFiles(self, tf_file, tfidf_file, idf_file):
		with open(tf_file, 'r') as f:
			f.readline()
			num_cols = len(f.readline().split(','))
			f.seek(0)
			word_count_matrix = np.transpose(genfromtxt(f, delimiter = ',', skip_header = 1, usecols = range(1, num_cols)))
		tfidf_matrix = TfidfTransformer().fit_transform(word_count_matrix)
		idf = np.array([math.log(1 + x) for x in float(len(word_count_matrix))/np.sum(word_count_matrix > 0, axis = 0)])

		with open(idf_file, 'wb') as f:
			for i in range(len(idf) - 1):
				f.write(str(idf[i]))
				f.write(',')
			f.write(str(idf[len(idf) - 1]))
			f.close()

		with open(tfidf_file, 'wb') as f:
			pickle.dump(tfidf_matrix, f, pickle.HIGHEST_PROTOCOL)


	def classify(self, query):
		query = "".join(c for c in query if c not in ('!','.',':',',',';','?')).lower()
		query_words = query.split() 
		p = PorterStemmer()
		query_words = [p.stem(query_words[i]) for i in range(len(query_words))]
		q = np.zeros(len(self.word_to_index))
		for word in query_words:
			if word in self.word_to_index:
				q[self.word_to_index[word]] += self.idf[self.word_to_index[word]]

		membership_scores = np.squeeze(np.asarray(np.dot(self.tfidf_matrix, q)))
		return sorted(zip(self.categories, membership_scores), key=lambda x: x[1], reverse=True)

