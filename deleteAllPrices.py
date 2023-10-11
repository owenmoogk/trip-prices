import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
from datetime import date
import time

# connect to the database
conn=sqlite3.connect('src/db.sqlite3')
cursor = conn.cursor()

rows = cursor.execute("delete from api_pricedatapoint")
conn.commit()