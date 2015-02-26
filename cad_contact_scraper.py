##################################################
## TX County Appraisal District Contact Scraper ##
##################################################

## Pulls all CAD contacts listed at "http://www.window.state.tx.us/propertytax/references/directory/cad/" 
## to a local CSV; have left in pyodbc for db hook up later if wanted

##By Bradley Smith (bradleysmith.dev@gmail.com, bradley.taft.smith@gmail.com)

########################################################################################################

#!/usr/bin/python

import mechanize
from BeautifulSoup import BeautifulSoup
Soup = BeautifulSoup
import csv
import sys
import time


#import pyodbc
#connString = 'DRIVER={PostgreSQL ANSI};Server=localhost;Database=XXX;UID=postgres;PWD=XXX'
#print connString
#conn = pyodbc.connect(connString)

br = mechanize.Browser()
cnt_csv = csv.reader(open("txcnt.csv"))

for row in cnt_csv: #scrape data and output csv for every non-empty township range combo 
   url = "http://www.window.state.tx.us/propertytax/references/directory/cad/" # reassign url w/o county
   county = str(row[0])
   url = "http://www.window.state.tx.us/propertytax/references/directory/cad/" + county + ".html" #assign county number in URL
   html = br.open(url)
   soup = Soup(html)

   #results
   content = soup.find("div", {"id": "content"})
   cnty = str(content.findAll('h1')[0].contents[0].strip().split(' ')[0].strip("\n"))
   update = str(str(content.find("p", {"class": "fileInfo"}).contents[0].strip()).split(':')[1].strip())
   aprsr = str(str(content.findAll("h2")[0].contents[0]).split(': ')[1].strip())
   phone = str(content.findAll("p")[1].contents[5]).strip()
   fax = str(content.findAll("p")[1].contents[12]).strip()
   urls = content.findAll("a",href=True)
   if len(urls) >= 1:
      email = urls[0].get('href').lstrip('mailto:') 
   else:
      email = "not listed"
   if len(urls) == 2:
      cadurl = urls[1].get('href').lstrip('"')
   else:
      cadurl = "not listed"
   maddr = '"' + str(content.findAll("p")[2].contents[0].strip()) + ", " + str(content.findAll("p")[2].contents[2]).strip() + '"'
   saddr = '"' + str(content.findAll("p")[3].contents[0].strip()) + ", " + str(content.findAll("p")[2].contents[2]).strip() + '"'
   #clctunt = str(content.findAll("p")[4].contents[0]).strip() ## Collecting Unit
   #taxunts = ", ".join(str(x) for x in content.findAll('li')) ## Active Taxing Units
   tmstmp = time.strftime("%d %b %y, %I:%M:%S %p")

   #output
   row = [cnty, update, aprsr, phone, fax, email, cadurl, maddr, saddr, tmstmp]
   print ",".join(str(x) for x in row)
   
   #sys.exit()
  
   

   
   
   #####  CONNECTION  ################################################################################

