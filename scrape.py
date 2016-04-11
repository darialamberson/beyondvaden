from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import re
from time import sleep

driver = webdriver.PhantomJS()

url = 'https://therapists.psychologytoday.com/rms/prof_detail.php?profid=%s&sid=1459550134.2557_26010&zipcode=94305&search=94305&tr=NextProf'
prof_start_id = '207105'#Savant
prof_id = prof_start_id
num_profiles = 1 #controls how many therapist profiles we want to scrape

#prof_id = '95997' #Choy
#prof_id = '35139' #Truong
#prof_id = '69009' #May
#prof_id = '66434' #Schellenberg

for i in range(num_profiles):
	#case we have wrapped back around so we're done
	if prof_id == prof_start_id and i > 0:
		break

	print '\nID'
	print '-------------------------'
	print prof_id
	driver.get(url % prof_id)
	soup = BeautifulSoup(driver.page_source)
	#print soup.prettify()

	#extract the profile linked to by the "next" button (for use the next time through the loop)
	prof_id = re.search(r'ProfileNav_prevProfLink.*?profid=([0-9]+)', driver.page_source.replace('\n', '')).group(1)

	#extract full name
	print '\nNAME'
	print '-------------------------'
	name = re.search(r'(?:Dr\. )?([A-Za-z\. -]+),?', soup.title.string).group(1)
	print name

	#extract description paragraph
	print '\nSUMMARY'
	print '-------------------------'
	summary= soup.find('div', {'class' : 'section profile-personalstatement'})
	summary = re.sub("[ \t\n]+"," ", str(summary).strip())
	statements = [summary_i.strip() for summary_i in summary.replace('<div class="section profile-personalstatement"> ', '').replace('</div>', '').split('<div class="statementPara"> ')[1:]]
	print ' '.join(statements)

	#extract phone number
	print '\nPHONE'
	print '-------------------------'
	match = re.search(r'(?:<a href=\"tel:([0-9]+))', driver.page_source.replace('\n', ''))
	if match:
		phone = match.group(1)
		print phone

	#extract location
	print '\nLOCATION'
	print '-------------------------'
	streetAddress = soup.find('span', {'itemprop': 'streetAddress'})
	zipCode = soup.find('span', {'itemprop': 'postalcode'})
	if streetAddress and zipCode:
		print streetAddress.text, zipCode.text

	#extract an additional location, if one exists
	text = re.search(r'Additional Location.*?<a href="tel:', driver.page_source.replace('\n', ''))
	if text:
		text = ' '.join(text.group(0).split())
		streetAddress2 = re.search(r'> *([0-9]+[A-Za-z ]+)<', text)
		zipCode2 = re.search(r'"postalcode">([0-9]{5})<', text)
		if streetAddress2 and zipCode2:
			print streetAddress2.group(1), zipCode2.group(1)


	#extract main specialties
	print '\nSPECIALTIES'
	print '-------------------------'
	for li in soup.findAll('li', {'class':"highlight"}):
		x = re.sub('[^0-9a-zA-Z ,-:]+', '', li.text)
		print x

	#extract issues focus
	print '\nISSUES'
	print '-------------------------'
	text = re.search(r'Issues</h3>.*?<h', driver.page_source.replace('\n', ''))
	if text:
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text

	#extract mental health focus
	print '\nMENTAL HEALTH'
	print '-------------------------'
	text = re.search(r'Mental Health.*?<h', driver.page_source.replace('\n', ''))
	if text:
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text

	#extract sexuality focus
	print '\nSEXUALITY'
	print '-------------------------'
	text = re.search(r'Sexuality.*?<div class="spec-list">', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text

	#extract categories 
	print '\nCATEGORIES'
	print '-------------------------'
	text = re.search(r'Categories.*?<div class="spec-list">', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text

	#extract languages other than english
	print '\nLANGUAGES'
	print '-------------------------'
	text = re.search(r'Alternative Languages.*?"spec-subcat"', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for s in text.findAll('span'):
			print s.text.replace(',', '')

	#extract treatment approach
	print '\nTREATMENT ORIENTATION'
	print '-------------------------'
	text = re.search(r'Treatment Orientation.*?<h3 class="spec-subcat">', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text

	#extract modality
	print '\nMODALITY'
	print '-------------------------'
	text = re.search(r'Modality.*?</div>', driver.page_source.replace('\n', ''))
	if text: 
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text

	#extract insurance providers
	print '\nINSURANCE'
	print '-------------------------'
	text = re.search(r'Accepted Insurance Plans.*?<h', driver.page_source.replace('\n', ''))
	if text:
		text = BeautifulSoup(text.group(0))
		for li in text.findAll('li'):
			print li.text


	print "\n*********************************************"

	sleep(3) #to be polite to their servers/behave more like a real client

driver.quit()