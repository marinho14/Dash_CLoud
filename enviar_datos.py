import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import time
from database import Database_Google
from gspread_dataframe import set_with_dataframe

Google_enviar= Database_Google("NewDatabase","Sheet1","sheet2")
ambiente_rv_dat = 2
disposicion_dat = 1
intensidad_torque_dat= 0.5
torque_control_dat = 10
torque_final_dat= torque_control_dat*intensidad_torque_dat
tam_lista =10
cont_fila = 1
ambiente_rv=[]
disposicion=[]
intensidad_torque=[]
torque_control=[]
torque_final=[]
ts=[]

emocion_reg=[]
espasticidad_reg=[]
dolor_reg=[]
ambiente_rv_reg=[]

Google_enviar.sheet1.clear()

for j in range(1000):
    for i in range(tam_lista):
        ambiente_rv_dat+=0.01
        disposicion_dat+=0.02
        torque_control_dat+=5
        intensidad_torque_dat+=0.001
        torque_final_dat = torque_control_dat*intensidad_torque_dat

        ambiente_rv.append(ambiente_rv_dat)
        disposicion.append(disposicion_dat)
        torque_control.append(torque_control_dat)
        intensidad_torque.append(intensidad_torque_dat)
        torque_final.append(torque_final_dat)
        aux = Google_enviar.sheet2.get("A1"+":D1")

        emocion_reg.append(aux[0][0])
        espasticidad_reg.append(aux[0][1])
        dolor_reg.append(aux[0][2])
        ambiente_rv_reg.append(aux[0][3])

        dt = datetime.now()
        ts_dat = datetime.timestamp(dt)
        ts.append(ts_dat)
    list_stop=[0]*tam_lista
    df = pd.DataFrame(list(zip(ts,emocion_reg,espasticidad_reg,dolor_reg,ambiente_rv_reg,ambiente_rv,disposicion,intensidad_torque,torque_control,torque_final,list_stop)))
    print(df)
    print(j)
    time.sleep(tam_lista)
    Google_enviar.define_out(df,tam_lista)
    ambiente_rv=[]
    disposicion=[]
    intensidad_torque=[]
    torque_control=[]
    torque_final=[]
    ts=[]