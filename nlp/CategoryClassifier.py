from numpy import genfromtxt
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import csr_matrix
import numpy as np


class CategoryClassifier(object):
	def __init__(self, word_counts_file):
		with open(word_counts_file, 'r') as f:
			f.readline()
			num_cols = len(f.readline().split(','))
			f.seek(0)
			word_count_matrix = genfromtxt(f, delimiter=',', skip_header=1, usecols=range(1, num_cols))
		tfidf_transformer = TfidfTransformer()
		self.tfidf_matrix = tfidf_transformer.fit_transform(word_count_matrix).todense()

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
				q[self.word_to_index[word]] += 1

		membership_scores = np.squeeze(np.asarray(np.dot(self.tfidf_matrix, q)))
		return sorted(zip(membership_scores, self.categories), reverse=True)