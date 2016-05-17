def getCategoriesAndTherapists(query)
	# return Array.new() << 1 << 2 << 3 << 4 << 5
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


if __FILE__ == $PROGRAM_NAME
	query = "eating fat weight binge purge pounds calories thin skinny cleanse diet puke vomit starve scale toilet anorexic bulimia"
	# query = "suicide kill pills cut"
	output = getCategoriesAndTherapists(query)
	p output[0]
	p output[1]
end