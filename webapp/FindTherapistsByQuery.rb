def getTherapists(query)
	# return Array.new() << 1 << 2 << 3 << 4 << 5
	f = open("|python ../nlp/FindTherapistsByQuery.py " + query)
	output = f.read().strip().split(", ")
	therapists = Array.new()
	for x in output do
		x.sub!('[', '')
		x.sub!(']', '')
		therapists << x.to_i
	end
	return therapists

end

if __FILE__ == $PROGRAM_NAME
	query = "eating fat weight binge purge pounds calories thin skinny cleanse diet puke vomit starve scale toilet anorexic bulimia"
	#query = "suicide suicide suicide suicide"
	therapists = getTherapists(query)
	p therapists
end