from numpy import genfromtxt
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import csr_matrix
import cPickle as pickle
import numpy as np

#Assumes wordcount file is a csv in the following format: 
#1st row: comma separated column names (ignored here)
#all other rows: category name, 1st word count, 2nd word count, etc.
#Writes a sparse tf-idf matrix to the outfile
def generate_tfidf(wordcount_file):
	with open(wordcount_file, 'r') as f:
		f.readline()
		num_cols = len(f.readline().split(','))
		f.seek(0)
		print num_cols
		X = genfromtxt(f, delimiter=',', skip_header=1, usecols=range(1,num_cols))
	#print X, '\n'
	tfidf_transformer = TfidfTransformer()
	X_hat = tfidf_transformer.fit_transform(X)
	#print X_hat.todense(), "\n"
	with open('tfidf_sparse.dat', 'wb') as outfile:
		pickle.dump(X_hat, outfile, pickle.HIGHEST_PROTOCOL)

