# pip install mysql-connector-python

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="foobar",
  database="employees"
)

mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)