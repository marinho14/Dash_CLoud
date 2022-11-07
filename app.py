from dash import Dash, dash_table, html , Input, Output, State, dcc , callback_context
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import date
import firebase_admin
import numpy as np
app = Dash(__name__,external_stylesheets=[dbc.themes.SLATE])
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime  
import plotly.graph_objects as go

###################################################################################

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("exoesquelet-eafit-sheet-bcb340f88950.json", scope)
client = gspread.authorize(credentials)

data_base = client.open("NewDatabase")

sheet1 = data_base.worksheet("Sheet1")
sheet2 = data_base.worksheet("sheet2")

color_sliders= "#FFFFFF"

time_stamp_global=[]
Torque_global=[]
###################################################################################
##app.title = 'Utms' ## Tittle in the web page
##app._favicon = ("assets/favicon.ico") Image in the webpage

app.layout = html.Div(children=[
    html.H1(children='Control Exoesqueleto',className='banner_t'),

    dbc.Row([ 
        dbc.Col([
            dbc.Label("Emoción",className='banner_2'),

            dcc.Slider(0, 360, 1,value=180,id='emocion-slider',
            marks={
                0: {'label': '0', 'style': {'color': color_sliders}},
                180: {'label': '180'},
                360: {'label': '360', 'style': {'color': color_sliders}}
            },
            tooltip={"placement": "bottom", "always_visible": True}),
        ],className='Column_1'),

        dbc.Col([      
            dbc.Label("Espasticidad",className='banner_2'),
            dcc.Slider(0, 6,0.1 ,value=3,id='espasticidad-slider',
            marks={
                0: {'label': '0', 'style': {'color': color_sliders}},
                3: {'label': '3'},
                6: {'label': '6', 'style': {'color': color_sliders}},
            },
            tooltip={"placement": "bottom", "always_visible": True}),
        ]),
    ],className="Fila_1"),

    dbc.Row([ 
        dbc.Col([
            dbc.Label("Dolor",className='banner_2'),
            dcc.Slider(0, 1, 0.01,value=0.5,id='dolor-slider',
            marks={
                0: {'label': '0', 'style': {'color': color_sliders}},
                0.5: {'label': '0.5'},
                1: {'label': '1', 'style': {'color': color_sliders}}
            },
            tooltip={"placement": "bottom", "always_visible": True}),
            ],className='Column_1'),

        dbc.Col([
            dbc.Label("Ambiente RV",className='banner_2'),
            dcc.Slider(0, 5, 0.1,value=2.5,id='rv-slider',
            marks={
                0: {'label': '0', 'style': {'color': color_sliders}},
                2.5: {'label': '4'},
                5: {'label': '1', 'style': {'color': color_sliders}}
            },
            tooltip={"placement": "bottom", "always_visible": True}),
        ]),
    ],className="Fila_1"),

    html.Button('Empezar', n_clicks=0, id='start_butt',className='button1'),

    dcc.Graph(id = 'graph_torque_final', animate = True, className="Graph"),
    
    dcc.Interval(
        id = 'graph-update',
        interval = 3000,
        n_intervals = 0
    ),

    dcc.ConfirmDialog(
        id='alert',
        message="Datos enviados correctamente",
    ),



])

###################################################################################

@app.callback(
    Output('alert', 'displayed'),
    Input('start_butt', 'n_clicks'),
    Input('emocion-slider', 'value'),
    Input('espasticidad-slider', 'value'),
    Input('dolor-slider', 'value'),
    Input('rv-slider', 'value'),
)
def change_button_style(n_clicks,emocion,espa,dolor,rv):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'start_butt' in changed_id:
        sheet2.update('A1',[[emocion,espa,dolor,rv,0]])
        return True

@app.callback(
    Output("graph_torque_final", "figure"), 
    Input('graph-update', 'n_intervals'),
)
def graph(n_clicks):
    max_row = int(sheet2.acell('A2').value)
    tiempo= sheet1.get("A"+str(max_row-2)+":A"+str(max_row))
    date_time = list(map(lambda x: datetime.fromtimestamp(float(x[0])), tiempo))
    Torque= sheet1.get("I"+str(max_row-2)+":I"+str(max_row))
    Torque= list(map(lambda x: float(x[0]), Torque))


    time_stamp_global.extend(date_time)
    Torque_global.extend(Torque)

    print(time_stamp_global)
    print(Torque_global)
    data = go.Scatter(
            x=time_stamp_global,
            y=Torque_global,
            name='Scatter',
            mode= 'lines+markers'
    )

    return {'data': [data],
        'layout' : go.Layout(xaxis=dict(range=[min(time_stamp_global),max(time_stamp_global)]),yaxis = dict(range = [min(Torque_global),max(Torque_global)]),)}

###################################################################################


if __name__ == '__main__':
    app.run_server(debug=True)