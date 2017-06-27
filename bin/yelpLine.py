import sqlite3 as sqlite
import time
import urllib
import zlib
import os
import timestring
import time


APP_PATH = os.getcwd()

conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')
conn.text_factory = str #text will be returned as string not unicode (default for sqlite3)
cur = conn.cursor()

cur.execute('''SELECT time_created, rating FROM Reviews WHERE business_id = ?''', ("wendys-belmont-2",))
reviews = cur.fetchall()
print reviews

dateData = []
for review in reviews:
    review_data = (timestring.Date(review[0]), review[1])
    dateData.append(review_data)

print sorted(dateData) # sorts by date, not rating

fhand = open('yelpLine.js','w')
fhand.write("yelpLine = [ ['Date'")
for review in reviews:
    fhand.write(",'"+review[0]+"'")
fhand.write("]")

# for month in months[1:-1]: burasi yanlis
for date in dateData:
    date = (str(date[0]), date[1])
    fhand.write(",\n['"+date[0]+"'")
    for review in reviews:
        key = (date, date[1])
        val = review[0], review[1]
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")

print "Data written to yelpline.js"
print "Open yelpline.htm in a browser to view"

