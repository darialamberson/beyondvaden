from CategoryClassifier import CategoryClassifier


def main():
	word_counts_file = 'counts.csv'
	query = 'kill kill assault sad'

	c = CategoryClassifier(word_counts_file=word_counts_file)
	top_categories = c.classify(query)
	print top_categories


if __name__ == "__main__":
    main()