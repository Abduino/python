import streamlit as st
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import serial
import time
import plotly.graph_objects as go
import numpy as np 
import random
import pygal    
st.write('<style>div.block-container{padding-top:0rem; padding-left:2rem; padding-right: 2rem; max-width: 100%;}</style>', unsafe_allow_html=True)
st.markdown(
     """
     <style>
     [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
         width: 200px;
       }
       [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
           width: 100px;
           margin-left: -500px;
        }
        </style>
        """,
        unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Real Time Analysis </h3>", unsafe_allow_html=True)

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="school")
mycursor = mydb.cursor()
with st.spinner("waiting to fetch the data ..."):
    time.sleep(3)
st.success("Finished!")
mycursor.execute("SELECT * FROM smart_agri")
myresult = mycursor.fetchall()
df = pd.DataFrame(myresult,columns=['Id','Soil Moisture','Water_level','Temperature','Humidity','Light','Pressure' ,'Gas','Altitude','Rain','Time Stamp'])
#df2 = pd.DataFrame(myresult,columns=['Id','Soil Moisture','Water_level','Temperature','Humidity','Light','Pressure' ,'Gas','Altitude','Rain'])
avg_age = np.mean(df['Soil Moisture'])

placeholder = st.empty()


while True:
    with placeholder.container():
        st.subheader("Table Data")
        st.dataframe(df,height=300)
        #st.dataframe(df.iloc[3])
        st.write("---")
        st.subheader("Soil Moisture")
        st.line_chart(df['Soil Moisture'])
        st.write("---")
        st.subheader("Temperature and Humidity")
        st.line_chart(df[['Temperature', 'Humidity']])
        st.write("---")
        st.subheader("Average of Humidity")
        st.line_chart(df['Gas'])
        st.write("---")
        st.subheader("Gas and Light")
        st.line_chart(df['Soil Moisture'])
        st.subheader("Plot Data")
        plt.scatter(df['Soil Moisture'],df['Humidity'],)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
            
           
        time.sleep(10)

