require 'rubygems'
require 'sqlite3'


# Create a new hash mapping categories to tf-idf scores.
cscores = Hash.new()


pairs = ARGV[0].split(',')
pairs.each do |pair|
	p = pair.split(':')
	cscores[p[0]] = p[1]
end

puts cscores['dogs']
puts cscores['cats']
puts cscores['birds']

DB = SQLite3::Database.open '../database.db'