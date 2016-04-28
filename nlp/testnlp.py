from CategoryClassifier import CategoryClassifier
from PorterStemmer import PorterStemmer


def main():
	word_counts_file = 'tf_matrix.csv'
	query = 'I am struggling in school. I understand nothing. The teachers are mean and the work is boring and hard. I just do not care.'
	c = CategoryClassifier(word_counts_file=word_counts_file)
	top_categories = c.classify(query)
	print top_categories[0:5]


if __name__ == "__main__":
    main()