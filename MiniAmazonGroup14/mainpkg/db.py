import mysql.connector
from mysql.connector import errorcode

def getdb():
  
  mydb = mysql.connector.connect(
    host="vcm-17245.vm.duke.edu",
    user="develop",
    password="316project",
    database="cardstore"
  )
  '''
  mydb = mysql.connector.connect(
    host="localhost",
    user="newuser",
    password="password",
    database="cardstore"
  )
  
  mydb = mysql.connector.connect(
    host="vcm-17245.vm.duke.edu",
    user="sean",
    password="seanm",
    database="cardstore"
  )
  '''

  return mydb

print(getdb())