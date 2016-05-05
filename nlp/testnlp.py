from CategoryClassifier import CategoryClassifier
from PorterStemmer import PorterStemmer

TEST_KEYWORDS = 1
TEST_PROSE = 1


def main():
	tf_file = 'tf_matrix10.csv'
	tfidf_file = 'tf_idf.dat'
	idf_file = 'idf.csv'

	c = CategoryClassifier(tf_file = tf_file, tfidf_file = tfidf_file, idf_file = idf_file)
	# output = c.classify("sad assault assault assault")
	# print output
	if TEST_KEYWORDS:
		print 'Test 1: Food keywords\n***********************************'
		query = 'eating fat weight binge purge whale pounds calories thin skinny cleanse diet puke vomit starve scale toilet anorexic bulimia'
		expected_categories = ['eating disorders', 'obesity', 'weight loss']
		testQuery(query, expected_categories, c)

		print 'Test 2: Suicide keywords\n***********************************'
		query = 'kill die suicide angry depressed knife cut pills gun dead gone sorry note'
		expected_categories = ['suicidal ideation', 'teen violence', 'depression']
		testQuery(query, expected_categories, c)

		print 'Test 3: Academic keywords\n***********************************'
		query = 'school struggle fail classes teachers mean hard boring work grades bad bully read math'
		expected_categories = ['academic underachievement', 'learning disabilities']
		testQuery(query, expected_categories, c)

	# 	print 'Test 4: Gay keywords\n***********************************'
	# 	query = 'pride gay homosexual lgbt sex men closet queer identity'
	# 	expected_categories = ['gay']
	# 	testQuery(query, expected_categories, c)

	# 	print 'Test 5: OCD keywords\n***********************************'
	# 	query = 'obsessive repetitive behavior control germs perfect count ritual'
	# 	expected_categories = ['obsessive compulsive ocd']
	# 	testQuery(query, expected_categories, c)

	# if TEST_PROSE:
	# 	print 'Test 1: Infidelity prose\n***********************************'
	# 	query = 'That bastard cheated with his mistress. I\'ll kill him and the hoe.'
	# 	expected_categories = ['infidelity', 'relationship issues']
	# 	testQuery(query, expected_categories, c)

	# 	print 'Test 2: Body image prose\n***********************************'
	# 	query = 'I am a fat bloated whale who needs to lose weight.'
	# 	expected_categories =['eating disorders', 'obesity', 'weight loss']
	# 	testQuery(query, expected_categories, c)

	# 	print 'Test 2: Post partum prose\n***********************************'
	# 	query = 'I am feeling sad after having a baby. I gave birth 2 weeks ago'
	# 	expected_categories =['post partum depression', 'postpartum adjustment', 'parenting', 'depression']
	# 	testQuery(query, expected_categories, c)


#For every expected category with rank i in the top 5, add 1/i to points. We weight a high rank more heavily than a low one.
#Max points is the score if all n expected categories come first in the top five, ie 1/1 + 1/2 + ... 1/n, where n <= 5. 
#If we get at least half the max points, pass.
def testQuery(query, expected_categories, c):
	print 'expected_categories=', expected_categories
	max_points = sum(1/float(i+1) for i in range(len(expected_categories)))

	output_categories = c.classify(query)
	points = 0
	false_pos = []
	false_neg = []
	for i in range(5):
		if output_categories[i][0] in expected_categories:
			points += 1/float(i+1)
			print 'match:', output_categories[i][0], 'with rank', i+1
		else:
			false_pos.append(output_categories[i][0])
	for category in expected_categories:
		if category not in [x[0] for x in output_categories[0:5]]:
			false_neg.append(category)
	print 'false positives=', false_pos
	print 'false negatives=', false_neg
	score = points/float(max_points)
	print 'score=', score
	print 'PASS\n' if score > .5 else 'FAIL\n'


if __name__ == "__main__":
    main()


