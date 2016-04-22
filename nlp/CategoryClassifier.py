from numpy import genfromtxt
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import csr_matrix
import numpy as np
import math


class CategoryClassifier(object):
	def __init__(self, word_counts_file):
		with open(word_counts_file, 'r') as f:
			f.readline()
			num_cols = len(f.readline().split(','))
			f.seek(0)
			word_count_matrix = genfromtxt(f, delimiter=',', skip_header=1, usecols=range(1, num_cols))
		self.tfidf_matrix = TfidfTransformer().fit_transform(word_count_matrix).todense()
		self.idf = np.array([math.log(1 + x) for x in float(len(word_count_matrix))/np.sum(word_count_matrix > 0, axis=0)])

		with open(word_counts_file, 'r') as f:
			words = f.readline().strip().split(',')
			self.word_to_index = {}
			for i in range(len(words)):
				self.word_to_index[words[i]] = i
			self.categories = []
			for line in f: 
				self.categories.append(line.split(',')[0])


	def classify(self, query):
		query_words = query.split() #todo: stem words
		q = np.zeros(len(self.word_to_index))
		for word in query_words:
			if word in self.word_to_index:
				q[self.word_to_index[word]] += self.idf[self.word_to_index[word]]

		membership_scores = np.squeeze(np.asarray(np.dot(self.tfidf_matrix, q)))
		return sorted(zip(self.categories, membership_scores), key=lambda x: x[1], reverse=True)

