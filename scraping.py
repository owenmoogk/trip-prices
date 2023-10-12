import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date, datetime
import re
from random import randint

# connect to the database
conn=sqlite3.connect('src/db.sqlite3')
cursor = conn.cursor()

resortNames = []
resortIds = []
nextResortId = -1

def updateResortNames():
  cursor.execute("SELECT * FROM api_resort")
  resorts = cursor.fetchall()
  
  global resortNames, resortIds, nextResortId
  resortNames = [resort[1] for resort in resorts]
  resortIds = [resort[0] for resort in resorts]
  nextResortId = max(resortIds) + 1

def addResortName(name):
  global nextResortId
  print(nextResortId, name)
  cursor.execute(f"insert into api_resort (id, name) values ({nextResortId}, '{name}')")
  conn.commit()
  updateResortNames()

def addPrice(resortId, price, tripStartDate, tripEndDate):
  while True:
    try:
      cursor.execute(f"""
                     insert into api_pricedatapoint (id, price, dateCollected, resort_id, tripStartDate, tripEndDate) values(
                        {randint(0,100000000)}, 
                        {price}, 
                        \'{date.today().year}-{date.today().month}-{date.today().day}\', 
                        {resortId},
                        \'{tripStartDate.year}-{tripStartDate.month}-{tripStartDate.day}\',
                        \'{tripEndDate.year}-{tripEndDate.month}-{tripEndDate.day}\'
                    )""")
      conn.commit()
      return
    except:
      pass

updateResortNames()

# scraper setup
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Edge(
  options=options,
)

# scrape the website
url = "https://www.tripcentral.ca/vacationgrid/index.php?params=0,143,19942,0,2,1,2,202401,0,11101,0,0,0,0,2,1,0,0-0-0,0,0,100,0,0,0,0,0,0,0,1,1,0,0&numberOfAdults=2&numberOfRooms=1"
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# find all of the elements
rows = soup.find(id="resultstbody").findAll(class_ = "linkRow")

for row in rows:
  name = re.sub(r'\([^)]*\)', '', row.find("th").text.replace("'", "")).strip()
  price4 = row.find(class_= "four").text
  price5 = row.find(class_= "five").text
  price6 = row.find(class_= "six").text
  
  if name not in resortNames:
    addResortName(name)
  
  resortId = resortIds[resortNames.index(name)]
  try:
    float(price4)
    addPrice(resortId, price4, datetime.strptime("17-Jan-23", "%d-%b-%y"), datetime.strptime("24-Jan-23", "%d-%b-%y"))
  except:
    pass

  try:
    float(price5)
    addPrice(resortId, price5, datetime.strptime("24-Jan-23", "%d-%b-%y"), datetime.strptime("31-Jan-23", "%d-%b-%y"))
  except:
    pass

  try:
    float(price6)
    addPrice(resortId, price6, datetime.strptime("31-Jan-23", "%d-%b-%y"), datetime.strptime("07-Feb-23", "%d-%b-%y"))
  except:
    pass