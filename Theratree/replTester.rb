require_relative 'FindTherapistsByQuery'
require 'sqlite3'

db = SQLite3::Database.new( "../Theratree/db/development.sqlite3" )

puts "\n\nHi there! I'm going to help you find a relevant therapist."
loop do
 	puts "Please list some keywords that you feel are related to the problem you're having. Don't hold back, anything helps!\n\n"
 	print ">> "
 	query = gets.chomp
 	output = getCategoriesAndTherapists(query)

 	suicide = 0

 	for category in output[0] do
 		puts category
 		if category.include?("suicid")
 			suicide = 1
 		end
 	end

 	if suicide == 1
 		puts "\n\nIt seems you are having suicidal thoughts. Please call the National Suicide Prevention Lifeline at 1(800)273-8255. Stay strong, we're here for you!\n"
	else
		puts "\n\nOk! I believe the 3 categories most relevant to your problem are:\n\n"
		puts output[0]
		puts "\n\nI think the following 5 therapists will be most helpful for you:"
		for id in output[1][1..5] do
			name = db.get_first_row('SELECT name FROM therapists WHERE therapist_id =' + id.to_s)[0] 
			specialties = db.execute('SELECT specialty FROM th_specialties WHERE therapist_id =' + id.to_s)
			print name + ": 		"
			print specialties
			puts "\n"
		end
	end
	puts "\n\nWould you like to search for therapists related to another problem? (y/n)\n"
	print ">> "
	answer = gets.chomp
	if answer.include?("n")
		puts "Goodbye for now!"
 		break
 	end
 	puts "\n"
end