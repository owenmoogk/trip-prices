import sqlite3
import re

# connect to the database
conn=sqlite3.connect('src/db.sqlite3')
cursor = conn.cursor()

rows=cursor.execute('''SELECT * FROM api_resort''')
names = [row[1] for row in rows]
newNames = [re.sub(r'\([^)]*\)', '', name).strip() for name in names]


for index, originalName in enumerate(names):
  cursor.execute(f"""
                  update api_resort
                  set name = '{newNames[index]}'
                  where name = '{originalName}'
                """)
  conn.commit()