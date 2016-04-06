from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import re

driver = webdriver.PhantomJS()

url = 'https://therapists.psychologytoday.com/rms/prof_detail.php?profid=%s&sid=1459550134.2557_26010&zipcode=94305&search=94305&tr=NextProf'
prof_id = '95997'

for i in range(3):
	print '\nID'
	print prof_id
	driver.get(url % prof_id)
	soup = BeautifulSoup(driver.page_source)

	#extract the profile linked to by the "next" button for use the next time through the loop
	prof_id = re.search(r'ProfileNav_prevProfLink.*?profid=([0-9]+)', driver.page_source.replace('\n', '')).group(1)

	#extract full name
	name = re.search(r'Dr\. ([A-Za-z\. -]+),?', soup.title.string).group(1)
	print '\nNAME'
	print name

	#extract text description as a list of strings, where each string is a paragraph of the description
	summary= soup.find('div', {'class' : 'section profile-personalstatement'})
	summary = re.sub("[ \t\n]+"," ", str(summary).strip())
	statements = [summary_i.strip() for summary_i in summary.replace('<div class="section profile-personalstatement"> ', '').replace('</div>', '').split('<div class="statementPara"> ')[1:]]
	print '\nSUMMARY'
	print statements

	#extract phone number
	phone = re.search(r'(?:<a href=\"tel:([0-9]+))', driver.page_source.replace('\n', '')).group(1)
	print '\nPHONE'
	print phone

	#extract location
	streetAddress = soup.find('span', {'itemprop': 'streetAddress'}).text
	zipCode = soup.find('span', {'itemprop': 'postalcode'}).text
	print '\nLOCATION'
	print streetAddress, zipCode

	#extract specialties

	print "\n*********************************************"

driver.quit()