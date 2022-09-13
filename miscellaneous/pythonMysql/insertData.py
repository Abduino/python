import mysql.connector
import serial
import time
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=5)
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="school")
print(mydb)
cursor = mydb.cursor()
while True:
    data = arduino.readline().decode('ascii')
    rows = data.split(',')
    query = "INSERT INTO ardu (potA, potB) VALUES (%s, %s)"
    pota=rows[0]
    potb=rows[1]
    values = (pota, potb)
    cursor.execute(query, values)
    mydb.commit()
    print(cursor.rowcount, "record inserted")
mydb.close()
