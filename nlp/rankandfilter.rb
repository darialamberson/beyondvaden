require 'rubygems'
require 'sqlite3'
require "set"

# Expects input of the form "category:score,category:score,...,category:score" as ARGV[0],
# where score represents the cosine similarity of this category to the users query
# Filters are ARGV[1] zip, ARGV[2] insurance

def rank:
	# Create a map from categories to scores.
	cscores = Hash.new()
	pairs = ARGV[0].split(',')
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
		puts id
		#Computes therapist relevance to user as 1/(num_categories for this therapist) * score
		results.each do |r|
			r = r.join.downcase.gsub(' ','')
			puts r
			if cscores[r] #should always be true
				therapist_scores[id] += cscores[r].to_f/(results.length.to_f)
			end
		end
		puts therapist_scores.to_s
		puts "*******"
	end

	#Compute therapist rankings
	rankings = therapist_scores.each_with_index.sort.map(&:last).reverse
	puts rankings.to_s

	#Compute all therapists matching filters
	where_clauses = Array.new()
	(1..ARGV.length).each do |i|
		if ARGV[i] != '0'
			if i == 1
				where_clauses << 'therapist_id IN (SELECT therapist_id FROM th_location WHERE zip == ' + ARGV[1] + ')'
			elsif i == 2
				where_clauses << 'therapist_id IN (SELECT therapist_id FROM th_insurance WHERE insurance == "' + ARGV[2] + '")'
			end 
		end
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

	puts filteredrankings



