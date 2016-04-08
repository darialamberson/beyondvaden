from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import re

driver = webdriver.PhantomJS()

url = 'https://therapists.psychologytoday.com/rms/prof_detail.php?profid=%s&sid=1459550134.2557_26010&zipcode=94305&search=94305&tr=NextProf'
prof_id = '207105'

for i in range(1):
	print '\nID'
	print '-------------------------'
	print prof_id
	driver.get(url % prof_id)
	soup = BeautifulSoup(driver.page_source)

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
	phone = re.search(r'(?:<a href=\"tel:([0-9]+))', driver.page_source.replace('\n', '')).group(1)
	print phone

	#extract location
	print '\nLOCATION'
	print '-------------------------'
	streetAddress = soup.find('span', {'itemprop': 'streetAddress'}).text
	zipCode = soup.find('span', {'itemprop': 'postalcode'}).text
	print streetAddress, zipCode

	#extract specialties
	print '\nSPECIALTIES'
	print '-------------------------'
	for li in soup.findAll('li', {'class':"highlight"}):
		print li.text

	#extract issues focus
	print '\nISSUES'
	print '-------------------------'
	text = re.search(r'Issues.*?<h3 class="spec-subcat">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for li in text.findAll('li'):
		print li.text

	#extract mental health focus
	print '\nMENTAL HEALTH'
	print '-------------------------'
	text = re.search(r'Mental Health.*?<h3 class="spec-subcat">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for li in text.findAll('li'):
		print li.text

	#extract sexuality focus
	print '\nSEXUALITY'
	print '-------------------------'
	text = re.search(r'Sexuality.*?<div class="spec-list">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for li in text.findAll('li'):
		print li.text

	#extract categories
	print '\nCATEGORIES'
	print '-------------------------'
	text = re.search(r'Categories.*?<div class="spec-list">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for li in text.findAll('li'):
		print li.text
	#extract languages other than english
	print '\nLANGUAGES'
	print '-------------------------'
	text = re.search(r'Alternative Languages.*?<h3 class="spec-subcat">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for s in text.findAll('span'):
		print s.text.replace(',', '')

	#extract treatment approach
	print '\nTREATMENT ORIENTATION'
	print '-------------------------'
	text = re.search(r'Treatment Orientation.*?<h3 class="spec-subcat">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for b in text.findAll('button', {'class':"ui-button glossary-button"}):
		print b.text

	#extract modality
	print '\nMODALITY'
	print '-------------------------'
	text = re.search(r'Modality.*?</div>', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for li in text.findAll('li'):
		print li.text

	#extract insurance providers
	print '\nINSURANCE'
	print '-------------------------'
	text = re.search(r'Accepted Insurance Plans.*?<div class="profile-verify-ins">', driver.page_source.replace('\n', '')).group(0)
	text = BeautifulSoup(text)
	for li in text.findAll('li'):
		print li.text


	print "\n*********************************************"

driver.quit()