import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
from datetime import date
import time
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

def addPrice(resortId, price):
  while True:
    try:
      cursor.execute(f"insert into api_pricedatapoint values({randint(0,100000000)}, {price}, \'{date.today().year}-{date.today().month}-{date.today().day}\', {resortId})")
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
url = "https://www.tripcentral.ca/vacationgrid/index.php?params=0,143,19942,0,2,1,3,202401,0,11101,0,0,0,0,2,1,0,0-0-0,0,0,100,0,0,0,0,0,0,0,1,1,0,0&numberOfAdults=2&numberOfRooms=1"
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# find all of the elements
rows = soup.find(id="resultstbody").findAll(class_ = "linkRow")

# only match these resorts
# resortMatchNames = [
#   "Barcelo Maya Palace",
#   "Hilton Tulum",
#   "Margaritaville",
#   "Royal Hideaway",
#   "Secrets",
#   "Sensira"
# ]

for row in rows:
  name = row.find("th").text.replace("'", "")
  price = row.find(class_= "four").text
  
  if name not in resortNames:
    addResortName(name)
  
  resortId = resortIds[resortNames.index(name)]
  try:
    float(price)
    addPrice(resortId, price)
  except:
    pass


# with open("master.csv", "a", newline="") as f:
#   appendArr = [str(date.today().year)+"/"+str(date.today().month)+"/"+str(date.today().day)]
  
#   for row in appendRows:
#     appendArr.append(row.find(class_= "four").text)
#     appendArr.append(row.find(class_= "five").text)
#     appendArr.append(row.find(class_= "six").text)
  
#   writer = csv.writer(f)
#   # writer.writerow(appendNames)
#   writer.writerow(appendArr)



# time.sleep(5)


# sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
 
# # Creating cursor object using connection object
  
# # executing our sql query
# cursor.execute(sql_query)
# print("List of tables\n")
  
# # printing all tables list
# print(cursor.fetchall())