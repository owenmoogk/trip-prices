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

def addPrice(resortId, price, dateRecorded, tripStartDate, tripEndDate):
  while True:
    try:
      cursor.execute(f"""
                     insert into api_pricedatapoint (id, price, dateCollected, resort_id, tripStartDate, tripEndDate) values(
                        {randint(0,100000000)}, 
                        {price}, 
                        \'{dateRecorded.year}-{dateRecorded.month}-{dateRecorded.day}\', 
                        {resortId},
                        \'{tripStartDate.year}-{tripStartDate.month}-{tripStartDate.day}\',
                        \'{tripEndDate.year}-{tripEndDate.month}-{tripEndDate.day}\'
                    )""")
      conn.commit()
      return
    except Exception as e:
      print(e)
      pass

updateResortNames()

with open('dad.csv', "r") as f:
  reader = csv.reader(f)
  rows = []
  for row in reader:
    rows.append(row)
  names = rows[0]
  startDates = rows[1]
  endDates = rows[2]

  names.remove("")
  startDates.remove("")
  endDates.remove("")

  rows.remove(names)
  rows.remove(startDates)
  rows.remove(endDates)

  for index, name in enumerate(names):
    try:
      if name == "" and names[index+1] == "":
        names[index] = names[index-1]
      elif name == "":
        names[index] = names[index+1]
    except:
      names[index] = names[index - 1]

  for row in rows:
    dateRecorded = datetime.strptime(row[0], "%d-%b-%y")
    row.remove(row[0])
    
    for index, price in enumerate(row):
      if price:
        resortName = names[index]
        tripStartDate = datetime.strptime(startDates[index], "%d-%b-%y")
        tripEndDate = datetime.strptime(endDates[index], "%d-%b-%y")
        resortId = resortIds[resortNames.index(resortName)]
        addPrice(resortId, price, dateRecorded, tripStartDate, tripEndDate)


# for row in rows:
#   name = row.find("th").text.replace("'", "")
#   price = row.find(class_= "four").text
  
#   resortId = resortIds[resortNames.index(name)]
#   try:
#     float(price)
#     addPrice(resortId, price)
#   except:
#     pass