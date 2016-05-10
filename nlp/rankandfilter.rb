require 'rubygems'
require 'sqlite3'
require "set"


#Given a string 'category:score, ... category:score', returns a list of therapist ids in 
#decreasing order of relevance to the categories
def rank(categoryscores)
	# Create a map from categories to scores.
	cscores = Hash.new()
	pairs = categoryscores.split(',')
	pairs.each do |pair|
		p = pair.split(':')
		cscores[p[0].gsub('\'', '')] = p[1]
	end

	db = SQLite3::Database.open '../database.db'
	num_therapists = 5#db.get_first_value("SELECT COUNT(*) FROM therapists")

	therapist_scores = Array.new(arr_size = num_therapists + 1, 0) #array is 0-indexed but therapist ids start at 1

	#Loop through all the therapists
	(1..num_therapists).each do |id|
		#Get all the categories associated with this therapist
		results = db.execute('SELECT specialty FROM th_specialties WHERE therapist_id =' + id.to_s)
		#Computes therapist relevance to user as 1/(num_categories for this therapist) * score
		results.each do |r|
			r = r.join.downcase.gsub(' ','')
			if cscores[r] #should always be true
				therapist_scores[id] += cscores[r].to_f/(results.length.to_f)
			end
		end
	end
	#Compute therapist rankings by descending order of scores
	rankings = therapist_scores.each_with_index.sort.map(&:last).reverse
	return rankings
end


#Returns only those therapists in the rankings list who match the zip code and insurance filters
def filter(rankings, zip, insurance)
	db = SQLite3::Database.open '../database.db'
	#Compute all therapists matching filters
	where_clauses = Array.new()
	if zip != 0 && zip != '0'
		where_clauses << 'therapist_id IN (SELECT therapist_id FROM th_location WHERE zip == ' + zip + ')'
	end
	if insurance != 0 && insurance != '0'
		where_clauses << 'therapist_id IN (SELECT therapist_id FROM th_insurance WHERE insurance == "' + insurance + '")'
	end
	
	query = 'SELECT therapist_id FROM therapists WHERE ' + where_clauses.join(" AND ")
	results = db.execute(query)

	#Keep from rankings only the therapists who match the filters
	results = Set.new(results.map{ |x| x.join.to_i })
	filteredrankings = Array.new()
	rankings.each do |t|
		if results.include?(t)
			filteredrankings << t
		end
	end
	return filteredrankings
end

# Expects input of the form "category:score,category:score,...,category:score" as ARGV[0],
# where score represents the cosine similarity of this category to the users query
# Filters are ARGV[1] zip, ARGV[2] insurance
if __FILE__ == $PROGRAM_NAME
	rankings = rank(ARGV[0])
	puts rankings.to_s
	filteredrankings = filter(rankings, ARGV[1], ARGV[2])
	puts filteredrankings
end



