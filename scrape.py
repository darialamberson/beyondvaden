from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import re

driver = webdriver.PhantomJS()

url = 'https://therapists.psychologytoday.com/rms/prof_detail.php?profid=%s&sid=1459550134.2557_26010&zipcode=94305&search=94305&tr=NextProf'
prof_id = '95997'

for i in range(1):
	print 'prof_id=', prof_id

	driver.get(url % prof_id)
	match = re.search(r'ProfileNav_prevProfLink.*?profid=([0-9]+)', driver.page_source.replace('\n', ''))
	prof_id = match.group(1)
	soup = BeautifulSoup(driver.page_source)
	name = re.search(r'(^[A-Za-z\. ]+),?', soup.title.string).group(1)
	print name
	summary= soup.find('div', {'class' : 'section profile-personalstatement'})
	summary = re.sub("[ \t\n]+"," ", str(summary).strip())
	statements = [summary_i.strip() for summary_i in summary.replace('<div class="section profile-personalstatement"> ', '').replace('</div>', '').split('<div class="statementPara"> ')[1:]]
	print statements

driver.quit()