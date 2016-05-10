query = "eating fat weight binge purge whale pounds calories thin skinny cleanse diet puke vomit starve scale toilet anorexic bulimia"
f = open("|python ../nlp/FindTherapistsByQuery.py " + query)
p f.read().strip().split(", ")