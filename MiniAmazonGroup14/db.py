import mysql.connector

mydb = mysql.connector.connect(
  host="vcm-17245.vm.duke.edu",
  user="root",
  password="316project",
  database="cardstore"
)

def createtest():
  mycursor = mydb.cursor()
  mycursor.execute("CREATE TABLE test (name VARCHAR(255), desc VARCHAR(255))")

def posttest():
  mycursor = mydb.cursor()
  sql = "INSERT INTO test (name, desc) VALUES (%s, %s)"
  val = ("John", "Is Cool")
  mycursor.execute(sql, val)
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")

def gettest():
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM test")
  myresult = mycursor.fetchall()
  for x in myresult:
    print(x)