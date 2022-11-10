import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timezone, timedelta
import time
import firebase_admin

import firebase_admin
from firebase_admin import credentials as cre_fire
from firebase_admin import db

import math

import json


class Database:

    def __init__(self, Database,sheet_1,sheet_2,name_database):
        if(name_database == "Google"):
            self.cond = 0
            self.Database= Database
            self.sheet_1 = sheet_1
            self.sheet_2 = sheet_2
            scope = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_name("exoesquelet-eafit-sheet-bcb340f88950.json", scope)
            client = gspread.authorize(credentials)
            self.data_base = client.open(Database)
            self.sheet1 = self.data_base.worksheet(self.sheet_1)
            self.sheet2 = self.data_base.worksheet(self.sheet_2) 
            self.cont_out=1
        else:
            self.cond=1
            cred = cre_fire.Certificate("exoesqueleto-eafit-firebase-adminsdk-ubdid-01f812b4a1.json")
            firebase_admin.initialize_app(cred, 
                {'databaseURL':"https://exoesqueleto-eafit-default-rtdb.firebaseio.com"})
            self.ref_data_soc = db.reference("/data/data_soc")
            self.ref_max_data = db.reference("/data/maximo_dato")
            self.ref = db.reference("/data")
    
    
    def define_in(self,emocion,espasticidad,dolor,ambiente_rv,gender,stop): 
        self.emocion = emocion
        self.espasticidad= espasticidad
        self.dolor = dolor
        self.ambiente_rv= ambiente_rv
        self.stop = stop
        self.gender=gender
        if(self.cond==0):
            self.sheet2.update('A1',[[self.emocion,self.espasticidad,self.dolor,self.ambiente_rv,self.gender,self.stop]])
        else:
            self.ref.update({"data_web":{"emocion":self.emocion,
                                         "espasticidad":self.espasticidad,
                                        "dolor":self.dolor,
                                        "Ambiente_RV":self.ambiente_rv,
                                        "gender":self.gender,
                                        "stop":self.stop}
                             })
        
    def get_max(self):
        if(self.cond==0):
            max_row = int(self.sheet2.acell('A2').value)-1
        else:
            read_data = self.ref_max_data.get()
            max_row= (read_data['max'])-1
            self.num_data = read_data['num_data']
        
        return max_row
    
    def read_data(self,min_val,max_val):
        
        if (self.cond==0):
            data_read =self.sheet1.get("A"+str(min_val)+":K"+str(max_val))   
            
            lista_out = list(map(lambda x:list(map(lambda y: float(y),x)) ,data_read))
            lista_out = pd.DataFrame(lista_out)
            
            lista_out[0]= lista_out[0].map(lambda x: datetime.fromtimestamp(x , tz=timezone(timedelta(hours=5)))) 
        else:
            datos_leidos = self.ref_data_soc.order_by_child("id").limit_to_last(math.ceil((max_val-min_val+1)/self.num_data)).get()
            lista_aux = list(map(lambda x: x['tabla'],list(datos_leidos.values())))
            lista_out = []
            for i in lista_aux:
                lista_out.extend(i)
            lista_out = pd.DataFrame(lista_out)
            lista_out[0]= lista_out[0].map(lambda x: datetime.fromtimestamp(x,tz=timezone(timedelta(hours=5)))) 
        return lista_out


