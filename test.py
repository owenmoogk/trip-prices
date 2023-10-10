import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
from datetime import date
import time

# connect to the database
conn=sqlite3.connect('src/db.sqlite3')
cursor = conn.cursor()

rows = cursor.execute("select * from api_pricedatapoint")
print([row for row in rows])
# conn.commit()

# sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
 
# # Creating cursor object using connection object
  
# # executing our sql query
# cursor.execute(sql_query)
# print("List of tables\n")
  
# # printing all tables list
# print(cursor.fetchall())