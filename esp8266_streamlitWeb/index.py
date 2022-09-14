#app.py
import streamlit as st
import pandas as pd
import re
import time
from bs4 import BeautifulSoup
import requests as req
import plotly.graph_objects as go
import numpy as np 
import random
import pygal 
import mysql.connector
from streamlit_echarts import st_echarts
from millify import millify
temp = 0
vsoil_moisture=0
vwater_level=0
vtemperature=0
vhumidity=0
vlight=0
vpressure=0
vgas=0
valtitude=0
vrain=10
mydb=''
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write('<style>div.block-container{padding-top:0rem; padding-left:2rem; padding-right: 2rem; max-width: 100%;}</style>', unsafe_allow_html=True)
st.markdown(
     """
     <style>
     [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
         width: 200px;
       }
       [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
           width: 100px;
           margin-left: -100px;
        }
        </style>
        """,
        unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Real Time Data </h3>", unsafe_allow_html=True)

st.session_state['key'] = st.text_input('Input the IP Address')
if not st.session_state['key']:
  st.stop()
url = "http://" + st.session_state['key'] + "/"
#ipadd = st.text_input('Input the IP Address')
#if not ipadd:
#  st.stop()
#url = "http://" + ipadd + "/"
#input_var = st.text_input('enter a name')
#st.write(f"Hello, {input_var}!")
#if ('name' not in st.session_state) and (input_var != ''):
#    st.session_state['name'] = input_var

#st.write('first name you have entered:')
#if 'name' in st.session_state:
#    st.write(st.session_state['name'])

#st.write(st.session_state)
placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            resp = req.get (url) #("http://10.230.37.170/")
            #resp = req.get ("http://192.168.1.6/")
            #myobj = {'somekey': 'somevalue'}
            #x = req.post(url + 'post',data =myobj)
            soup = BeautifulSoup(resp.text, "html.parser")
            head = soup.find_all(["h2"])      
            query = "INSERT INTO smart_agri (soil_moisture,water_level,temperature,humidity,light,pressure ,gas,altitudevar,rain) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)"
            try:
                vsoil_moisture= head[0].text.strip()
                vwater_level= 10
                vtemperature= head[1].text.strip()
                vhumidity= head[2].text.strip()
                vlight=head[3].text.strip()
                vpressure=head[5].text.strip()
                vgas=head[4].text.strip()
                valtitude=head[6].text.strip()
                vrain=10
            except:
                pass
            moisture_sensor_value=int(float(vsoil_moisture))
            temperature_sensor_value=int(float(vtemperature))
            humidity_sensor_value=int(float(vhumidity))
            light_sensor_value=int(float(vlight))
            gas_sensor_value=int(float(vgas))
            air_pressure_sensor_value=int(float(vpressure))
            sealevel_pressure_sensor_value=int(float(vsoil_moisture))
            altitude_sensor_value=int(float(valtitude))
            altitude_sensor_value_2=int(float(vsoil_moisture))
            values = (vsoil_moisture,vwater_level,vtemperature,vhumidity,vlight,vpressure ,vgas,valtitude,vrain)
            try:
                mydb = mysql.connector.connect(host="localhost", user="root", password="", database="school")
                cursor = mydb.cursor()
                #cursor.execute(query, values)
                #mydb.commit()
            except mysql.connector.Error as err:
                st.info("Connection to the database refused")
            col0, col1, col2,col3,col4, col5, col6,col7 = st.columns(8)
            col0.metric("Soil Moisture", str(moisture_sensor_value) + "%", temp)
            col1.metric("Temperature", str(temperature_sensor_value) + " c° ", " 50 c° ")
            col2.metric("Humidity", str(humidity_sensor_value) + "%", "50%")
            col3.metric("Light", str(light_sensor_value) + " lux", "50 °lux")
            col4.metric("Gas Level", str(gas_sensor_value) + "%", "1.2 %")
            col5.metric("Pressure", millify(vpressure) + " pa", "-8pa")
            col6.metric("Altitude", millify(valtitude) + " m", "4m")
            col7.metric("Rain", vrain, "1.2")
            st.write("---")
            temp =vsoil_moisture
            fig0= go.Figure(go.Indicator(
                value = moisture_sensor_value,
                mode = "gauge+number+delta",
                title = {'text': "Soil Moisture", 'font': {'size': 25}},
                delta = {'reference': 50},
                gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "lightblue"},
                 'bgcolor': "white",
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
                ))
            fig1= go.Figure(go.Indicator(
                value = humidity_sensor_value,
                mode = "gauge+number+delta",
                title = {'text': "Humidity", 'font': {'size': 25}},
                delta = {'reference': 50},
                gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "lightblue"},
                 'bgcolor': "white",
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
                ))
            fig2= go.Figure(go.Indicator(
                value = temperature_sensor_value,
                mode = "gauge+number+delta",
                title = {'text': "Temperature", 'font': {'size': 25}},
                delta = {'reference': 50},
                gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "lightblue"},
                 'bgcolor': "white",
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
                ))
            fig3= go.Figure(go.Indicator(
                value = light_sensor_value,
                mode = "gauge+number+delta",
                title = {'text': "Light", 'font': {'size': 25}},
                delta = {'reference': 50},
                gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "lightblue"},
                 'bgcolor': "white",
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
                ))
            fig4= go.Figure(go.Indicator(
                value = gas_sensor_value,
                mode = "gauge+number+delta",
                title = {'text': "Gas Level", 'font': {'size': 25}},
                delta = {'reference': 50},
                gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "lightblue"},
                 'bgcolor': "white",
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
                ))
            fig5= go.Figure(go.Indicator(
                value = air_pressure_sensor_value,
                mode = "gauge+number+delta",
                title = {'text': "Pressure", 'font': {'size': 25}},
                delta = {'reference': 50},
                gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "lightblue"},
                 'bgcolor': "white",
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
                ))
            fig6= go.Figure(go.Indicator(
                value = 50,
                mode = "gauge+number+delta",
                title = {'text': "Rain", 'font': {'size': 25}},
                delta = {'reference': 50},
                gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "lightblue"},
                 'bgcolor': "white",
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
                ))
            fig7= go.Figure(go.Indicator(
                value = 50,
                mode = "gauge+number+delta",
                title = {'text': "Altitude", 'font': {'size': 25}},
                delta = {'reference': 50},
                gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "lightblue"},
                 'bgcolor': "white",
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 29}}
                ))

            fig0.update_layout(autosize=False, height=250,margin=dict(l=1,r=1,b=1,t=60,pad=3),paper_bgcolor="#f0f2f1")
            fig1.update_layout(autosize=False, height=250,margin=dict(l=1,r=1,b=1,t=60,pad=3),paper_bgcolor="#f0f2f1")
            fig2.update_layout(autosize=False, height=250,margin=dict(l=1,r=1,b=1,t=60,pad=3),paper_bgcolor="#f0f2f1")
            fig3.update_layout(autosize=False, height=250,margin=dict(l=1,r=1,b=1,t=60,pad=3),paper_bgcolor="#f0f2f1")
            fig4.update_layout(autosize=False, height=250,margin=dict(l=1,r=1,b=1,t=60,pad=3),paper_bgcolor="#f0f2f1")
            fig5.update_layout(autosize=False, height=250,margin=dict(l=1,r=1,b=1,t=60,pad=3),paper_bgcolor="#f0f2f1")
            fig6.update_layout(autosize=False,height=250,margin=dict(l=1,r=1,b=1,t=60,pad=3),paper_bgcolor="#f0f2f1")
            fig7.update_layout(autosize=False, height=250,margin=dict(l=1,r=1,b=1,t=60,pad=3),paper_bgcolor="#f0f2f1")
            #col0, col1, col2,col3,col4, col5, col6,col7 = st.columns(8)
            cola, colb, colc,cold= st.columns(4)
            with cola:
                 st.plotly_chart(fig0,use_container_width=True)
            with colb:
                 st.plotly_chart(fig1,use_container_width=True)
            with colc:
                 st.plotly_chart(fig2,use_container_width=True)
            with cold:
                 st.plotly_chart(fig3,use_container_width=True)
            cole, colf, colg,colh= st.columns(4)
            with cole:
                 st.plotly_chart(fig4,use_container_width=True)
            with colf:
                 st.plotly_chart(fig5,use_container_width=True)
            with colg:
                 st.plotly_chart(fig6,use_container_width=True)
            with colh:
                 st.plotly_chart(fig7,use_container_width=True)

        except req.exceptions.ConnectionError:
            st.info("Connection refused")
        time.sleep(5)
