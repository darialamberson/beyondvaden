
#Returns a pair where p[0] is an array containing the 
#top three categories, and p[1] is an array containing 
#therapist ids in descending order of relevance
def getCategoriesAndTherapists(query)
	query = query.gsub("'", "")

	f = open("|python ../nlp/FindTherapistsByQuery.py " + query)
	output = f.read().strip().gsub("\n", ", ").split(", ")
	categories = Array.new()

	for x in output[0..2] do
		x.sub!('[', '')
		x.sub!(']', '')
		categories << x
	end

	therapists = Array.new()
	for x in output[3..-1] do
		x.sub!('[', '')
		x.sub!(']', '')
		therapists << x.to_i
	end
	return [categories,therapists]

end
