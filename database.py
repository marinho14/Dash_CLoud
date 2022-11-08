import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import time
from gspread_dataframe import set_with_dataframe

class Database_Google:

    def __init__(self, Database,sheet_1,sheet_2):
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
    
    def define_in(self,emocion,espasticidad,dolor,ambiente_rv,gender,stop): 
        self.emocion = emocion
        self.espasticidad= espasticidad
        self.dolor = dolor
        self.ambiente_rv= ambiente_rv
        self.stop = stop
        self.gender=gender
        self.sheet2.update('A1',[[self.emocion,self.espasticidad,self.dolor,self.ambiente_rv,self.gender,self.stop]])
    
    def define_out(self,df,tam_lista):  ## Se agrega lo del socket
        #set_with_dataframe(worksheet=self.sheet1, dataframe=df, include_index=False,include_column_header=False, resize=True)
        df_values = df.values.tolist()
        self.data_base.values_append('Sheet1', {'valueInputOption': 'RAW'}, {'values': df_values})
        self.cont_out= self.cont_out+ (tam_lista-1)
        self.sheet2.update('A2',self.cont_out)


