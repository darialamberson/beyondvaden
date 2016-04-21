from generate_tfidf import generate_tfidf
from classify import classify_query
import cPickle as pickle

def main():
	wordcount_file = 'counts.csv'
	tf_idf_file = 'tfidf_sparse.dat'
	query = 'kill kill assault sad'
	generate_tfidf(wordcount_file)
	scores = classify_query('kill kill assault ', tf_idf_file, wordcount_file)
	print scores


if __name__ == "__main__":
    main()