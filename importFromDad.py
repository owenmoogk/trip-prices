import sqlite3
import csv
from datetime import date, datetime
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

def addPrice(resortId, price, dateInput):
  while True:
    try:
      cursor.execute(f"insert into api_pricedatapoint values({randint(0,100000000)}, {price}, \'{dateInput.year}-{dateInput.month}-{dateInput.day}\', {resortId})")
      conn.commit()
      return
    except:
      pass

updateResortNames()

with open('dad.csv', "r") as f:
  reader = csv.reader(f)
  rows = []
  for row in reader:
    rows.append(row)
  names = rows[0]
  names.remove("")
  rows.remove(names)

  for row in rows:
    currDate = datetime.strptime(row[0], "%d-%b-%y")
    row.remove(row[0])
    
    for index, price in enumerate(row):
      if price:
        resortName = names[index]
        resortId = resortIds[resortNames.index(resortName)]
        addPrice(resortId, price, currDate)


# for row in rows:
#   name = row.find("th").text.replace("'", "")
#   price = row.find(class_= "four").text
  
#   resortId = resortIds[resortNames.index(name)]
#   try:
#     float(price)
#     addPrice(resortId, price)
#   except:
#     pass