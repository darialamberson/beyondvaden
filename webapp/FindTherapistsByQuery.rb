def getTherapists(query)
	return Array.new() << 1 << 2 << 3 << 4 << 5
	# f = open("|python ../nlp/FindTherapistsByQuery.py " + query)
	# return f.read().strip().split(", ")
end

if __FILE__ == $PROGRAM_NAME
	query = "eating fat weight binge purge whale pounds calories thin skinny cleanse diet puke vomit starve scale toilet anorexic bulimia"
	therapists = getTherapists(query)
	p therapists
end