import sys
from CategoryClassifier import CategoryClassifier
from RankTherapists import rank

def main(words):
	c = CategoryClassifier(tf_file='../nlp/tf_matrix_working.csv', tfidf_file='../nlp/tf_idf.dat', idf_file='../nlp/idf.csv')
	categoryAndWeight = c.classify(query=' '.join(words))
	# print categoryAndWeight
	# print '****************'
	print rank(categoryAndWeight)
	#print ', '.join([x[0] for x in categoryAndWeight[: 3]])

if __name__ == '__main__':
	main(sys.argv[1 :])

