# Requires wikipedia package and bs4

db_name = '../database.db'

import sqlite3
import wikipedia #Documentation: https://wikipedia.readthedocs.org/en/latest/code.html


import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #Sets python to look for things in the parent directory
import db_connector as db

# Step 1: Find all distinct issue categories.
connection = sqlite3.connect(db_name)
c = connection.cursor()
db.select(c, ['issue'], 'th_issues', distinct=True)
issues = [str(i[0]) for i in c.fetchall()]
print issues
connection.close()

# Step 2: For each category, find the closest wikipedia page and generate term-frequency lists.