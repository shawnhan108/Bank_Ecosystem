import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="anshulshawn",
    database="mydb"
)

mycursor = mydb.cursor()

mycursor.execute("show tables")

for tb in mycursor:
    print(tb)

