from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import re
import os
from time import sleep

import sqlite3
import db_connector as db

driver = webdriver.PhantomJS(os.path.join(os.getcwd(), 'bin/phantomjs'))

#url = 'https://therapists.psychologytoday.com/rms/prof_detail.php?profid=%s&sid=1459550134.2557_26010&zipcode=94305&search=94305&tr=NextProf'
#prof_start_id = '207105' #Savant--maybe we should add in other zip codes?
url = 'https://therapists.psychologytoday.com/rms/prof_detail.php?profid=%s&sid=1461553646.8442_2731&city=Palo+Alto&county=Santa+Clara&state=CA&tr=NextProf' # All PA Zip Codes
prof_start_id = '143458' # April R Holman
prof_id = prof_start_id
num_profiles = 10000 #controls how many therapist profiles we want to scrape

db_name = 'database.db'
connection = sqlite3.connect(db_name)
connection.text_factory = str
c = connection.cursor()

#prof_id = '95997' #Choy
#prof_id = '35139' #Truong
#prof_id = '69009' #May
#prof_id = '66434' #Schellenberg

for i in range(num_profiles):

	#case we have wrapped back around so we're done
	if prof_id == prof_start_id and i > 0:
		break

	info = []
	exists = False #keeps track of whether we've seen the therapist before
	db.select(c, ['therapist_id'], 'therapists', where='pt_id=' + prof_id)
	try:
		therapist_id = c.fetchone()[0]
		if therapist_id != []:
			info.append(therapist_id)
			exists = True
	except TypeError:
		pass

	print '\nID'
	print '-------------------------'
	print prof_id
	info.append(int(prof_id))
	driver.get(url % prof_id)
	soup = BeautifulSoup(driver.page_source)
	#print soup.prettify()

	#extract full name
	print '\nNAME'
	print '-------------------------'
	name = re.search(r'(?:Dr\. )?([A-Za-z\. -]+),?', soup.title.string).group(1)
	info.append(str(name))
	print name

	#extract description paragraph
	print '\nSUMMARY'
	print '-------------------------'
	summary= soup.find('div', {'class' : 'section profile-personalstatement'})
	summary = re.sub("[ \t\n]+"," ", str(summary).strip())
	statements = [summary_i.strip() for summary_i in summary.replace('<div class="section profile-personalstatement"> ', '').replace('</div>', '').split('<div class="statementPara"> ')[1:]]
	collated = ' '.join(statements)
	info.append(collated)
	print ' '.join(statements)

	#extract phone number
	print '\nPHONE'
	print '-------------------------'
	match = re.search(r'(?:<a href=\"tel:([0-9]+))', driver.page_source.replace('\n', ''))
	if match:
		phone = match.group(1)
		info.append(str(phone))
		print phone
	else: 
		info.append('') #no phone number found

	# At this point, we insert this info into the database.
	if exists:
		db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
	else:
		db.insert(c, 'therapists', info, ['pt_id', 'name', 'summary', 'phone'])
	connection.commit()

	# Get the therapist id (for use in later insertions) NEED TO KEEP TRACK OF THIS IN THE FUTURE FOR UPDATES
	db.select(c, ['therapist_id'], 'therapists', where='pt_id=' + prof_id)
	therapist_id = c.fetchone()[0]
	if therapist_id == []:
		c.execute('SELECT last_insert_rowid()')
		therapist_id = c.fetchone()[0]

	#extract the profile linked to by the "next" button (for use the next time through the loop)
	prof_id = re.search(r'ProfileNav_prevProfLink.*?profid=([0-9]+)', driver.page_source.replace('\n', '')).group(1)
	
	#extract location
	print '\nLOCATION'
	print '-------------------------'
	streetAddress = soup.find('span', {'itemprop': 'streetAddress'})
	zipCode = soup.find('span', {'itemprop': 'postalcode'})
	if streetAddress and zipCode:
		if exists:
			db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
		else:
			db.insert(c, 'th_location', (therapist_id, streetAddress.text, zipCode.text))
		print streetAddress.text, zipCode.text

	#extract an additional location, if one exists
	text = re.search(r'Additional Location.*?<a href="tel:', driver.page_source.replace('\n', ''))
	if text:
		text = ' '.join(text.group(0).split())
		streetAddress2 = re.search(r'> *([0-9]+[A-Za-z ]+)<', text)
		zipCode2 = re.search(r'"postalcode">([0-9]{5})<', text)
		if streetAddress2 and zipCode2:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_location', (therapist_id, streetAddress2.group(1), zipCode2.group(1)))
			print streetAddress2.group(1), zipCode2.group(1)


	#extract main specialties
	print '\nSPECIALTIES'
	print '-------------------------'
	specialties = []
	for li in soup.findAll('li', {'class':"highlight"}):
		x = str(re.sub('[^0-9a-zA-Z ,-:]+', '', li.text))
		print x
		specialties.append((therapist_id, x))
	if len(specialties) > 0:
		if exists:
			db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
		else:
			db.insert(c, 'th_specialties', specialties, multi=True)

	#extract issues focus
	print '\nISSUES'
	print '-------------------------'
	issues = []
	text = re.search(r'Issues</h3>.*?<h', driver.page_source.replace('\n', ''))
	if text:
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text
			try:
				for item in str(li.text).split(', '):
					issues.append((therapist_id, item))
			except UnicodeEncodeError:
					pass
		if len(issues) > 0:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_issues', issues, multi=True)

	#extract mental health focus
	print '\nMENTAL HEALTH'
	print '-------------------------'
	focus = []
	text = re.search(r'Mental Health.*?<h', driver.page_source.replace('\n', ''))
	if text:
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text
			focus.append((therapist_id, str(li.text)))
		if len(focus) > 0:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_mental_health_focus', focus, multi=True)

	#extract sexuality focus
	print '\nSEXUALITY'
	print '-------------------------'
	vals = []
	text = re.search(r'Sexuality.*?<div class="spec-list">', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text
			vals.append((therapist_id, str(li.text)))
		if len(vals) > 0:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_sexuality_focus', vals, multi=True)

	#extract categories 
	print '\nCATEGORIES'
	print '-------------------------'
	vals = []
	text = re.search(r'Categories.*?<div class="spec-list">', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text
			vals.append((therapist_id, str(li.text)))
		if len(vals) > 0:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_categories', vals, multi=True)

	#extract languages other than english
	print '\nLANGUAGES'
	print '-------------------------'
	vals = []
	text = re.search(r'Alternative Languages.*?"spec-subcat"', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for s in text.findAll('span'):
			parsed = s.text.replace(',', '')
			vals.append((therapist_id, str(parsed)))
			print parsed
		if len(vals) > 0:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_languages', vals, multi=True)

	#extract treatment approach
	print '\nTREATMENT ORIENTATION'
	print '-------------------------'
	vals = []
	text = re.search(r'Treatment Orientation.*?<h3 class="spec-subcat">', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text
			vals.append((therapist_id, str(li.text)))
		if len(vals) > 0:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_treatment_orientation', vals, multi=True)

	#extract modality
	print '\nMODALITY'
	print '-------------------------'
	vals = []
	text = re.search(r'Modality.*?</div>', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text
			vals.append((therapist_id, str(li.text)))
		if len(vals) > 0:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_modality', vals, multi=True)

	#extract insurance providers
	print '\nINSURANCE'
	print '-------------------------'
	vals = []
	text = re.search(r'Accepted Insurance Plans.*?<h', driver.page_source.replace('\n', ''))
	if text:
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text
			vals.append((therapist_id, str(li.text)))
		if len(vals) > 0:
			if exists:
				db.replace(c, 'therapists', info, ['therapist_id', 'pt_id', 'name', 'summary', 'phone'])
			else:
				db.insert(c, 'th_insurance', vals, multi=True)


	print "\n*********************************************"

	connection.commit()
	sleep(0.25) #to be polite to their servers/behave more like a real client

connection.close()
driver.quit()