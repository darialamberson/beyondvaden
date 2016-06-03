from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import re
from time import sleep
import sqlite3 

driver = webdriver.PhantomJS()
url = 'https://therapists.psychologytoday.com/rms/prof_detail.php?profid=%s'
conn = sqlite3.connect('../Theratree/db/development.sqlite3', isolation_level=None)
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS th_photos')
c.execute('CREATE TABLE th_photos (therapist_id INT PRIMARY KEY NOT NULL, img_url TEXT)')
c.execute('SELECT therapist_id, pt_id FROM therapists')
ids = c.fetchall()
#print ids

for id in ids:
	driver.get(url % id[1])
	#soup = BeautifulSoup(driver.page_source)
	#print soup.prettify()
	try:
		img_url = re.search(r'<img src=\"(.*?jpg.*?)\"', driver.page_source.replace('\n', '')).group(1)
	except:
		print "Using anonymous photo"
		img_url = "https://pixabay.com/static/uploads/photo/2014/04/02/10/25/man-303792_960_720.png"
	s = 'INSERT INTO th_photos VALUES(%s, \"%s\")'%(id[0], img_url)
	#print s
	c.execute(s)
	sleep(0.25) 

driver.quit()