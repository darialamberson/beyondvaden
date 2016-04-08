from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import re

driver = webdriver.PhantomJS()

url = 'https://therapists.psychologytoday.com/rms/prof_detail.php?profid=%s&sid=1459550134.2557_26010&zipcode=94305&search=94305&tr=NextProf'
prof_id = '207105'

for i in range(1):
	print '\nID'
	print prof_id
	driver.get(url % prof_id)
	soup = BeautifulSoup(driver.page_source)

	#extract the profile linked to by the "next" button (for use the next time through the loop)
	prof_id = re.search(r'ProfileNav_prevProfLink.*?profid=([0-9]+)', driver.page_source.replace('\n', '')).group(1)

	#extract full name
	name = re.search(r'(?:Dr\. )?([A-Za-z\. -]+),?', soup.title.string).group(1)
	print '\nNAME'
	print name

	#extract description paragraph
	summary= soup.find('div', {'class' : 'section profile-personalstatement'})
	summary = re.sub("[ \t\n]+"," ", str(summary).strip())
	statements = [summary_i.strip() for summary_i in summary.replace('<div class="section profile-personalstatement"> ', '').replace('</div>', '').split('<div class="statementPara"> ')[1:]]
	print '\nSUMMARY'
	print '-------------------------'
	print ' '.join(statements)

	#extract phone number
	phone = re.search(r'(?:<a href=\"tel:([0-9]+))', driver.page_source.replace('\n', '')).group(1)
	print '\nPHONE'
	print '-------------------------'
	print phone

	#extract location
	streetAddress = soup.find('span', {'itemprop': 'streetAddress'}).text
	zipCode = soup.find('span', {'itemprop': 'postalcode'}).text
	print '\nLOCATION'
	print '-------------------------'
	print streetAddress, zipCode

	#extract specialties
	specialties = soup.findAll('li', {'class':"highlight"})
	print '\nSPECIALTIES'
	print '-------------------------'
	for hit in specialties:
		print hit.text

	#extract issues/mental health/sexuality focuses
	print '\nISSUES'
	print '-------------------------'
	issues = soup.findAll('div', {'class':"col-xs-12 col-sm-12 col-md-6 col-lg-6"})
	for hit in issues:
		for li in hit.findAll('li'):
			print li.text

	#extract treatment approach
	print '\nTREATMENT ORIENTATION'
	print '-------------------------'
	text = re.search(r'Treatment Orientation.*<h3 class="spec-subcat">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	#print text
	treatments = text.findAll('button', {'class':"ui-button glossary-button"})
	for treatment in treatments:
		print treatment.text

	#extract modality
	print '\nMODALITY'
	print '-------------------------'
	text = re.search(r'Modality.*?</div>', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for m in text.findAll('li'):
		print m.text


	print '\nINSURANCE'
	print '-------------------------'
	text = re.search(r'Accepted Insurance Plans.*?<div class="profile-verify-ins">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for i in text.findAll('li'):
		print i.text


	print '\nLANGUAGES'
	print '-------------------------'
	text = re.search(r'Alternative Languages.*?<h3 class="spec-subcat">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for i in text.findAll('span'):
		print i.text.replace(',', '')


	print "\n*********************************************"

driver.quit()