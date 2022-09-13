import streamlit as st

import mysql.connector
import pandas as pd
import serial
import time
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="school")
print(mydb)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM ardu")
myresult = mycursor.fetchall()
df = pd.DataFrame(myresult)
print("====================print=========================")
print(df)
print("==================dataframe===========================")
st.dataframe(df)
print("===================table==========================")
st.table(df)
print("=================write============================")
st.write(df)
