from bs4 import BeautifulSoup
from selenium import webdriver
import csv
from datetime import date
import time


url = "https://www.tripcentral.ca/vacationgrid/index.php?params=0,143,19942,0,2,1,3,202401,0,11101,0,0,0,0,2,1,0,0-0-0,0,0,100,0,0,0,0,0,0,0,1,1,0,0&numberOfAdults=2&numberOfRooms=1"
options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Edge(
    options=options,
)

browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

rows = soup.find(id="resultstbody").findAll(class_ = "linkRow")

resortMatchNames = [
  "Barcelo Maya Palace",
  "Hilton Tulum",
  "Margaritaville",
  "Royal Hideaway",
  "Secrets",
  "Sensira"
]

appendRows = []
appendNames = [""]
print(rows)
for row in rows:

    # if resort name matches
    for matchName in resortMatchNames:
      if matchName in row.find("th").text:
        appendNames.append(row.find("th").text)
        appendNames.append("")
        appendNames.append("")
        appendRows.append(row)
        break


with open("master.csv", "a", newline="") as f:
  appendArr = [str(date.today().year)+"/"+str(date.today().month)+"/"+str(date.today().day)]
  
  for row in appendRows:
    appendArr.append(row.find(class_= "four").text)
    appendArr.append(row.find(class_= "five").text)
    appendArr.append(row.find(class_= "six").text)
  
  writer = csv.writer(f)
  # writer.writerow(appendNames)
  writer.writerow(appendArr)



time.sleep(5)