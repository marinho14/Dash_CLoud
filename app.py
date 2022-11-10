from dash import Dash, dash_table, html , Input, Output, State, dcc , callback_context
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import date
import firebase_admin
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime  
import plotly.graph_objects as go
from database import Database
###################################################################################



val2show = 10
val2print = 100

Google= Database("NewDatabase","Sheet1","sheet2","firebase")

color_sliders= "#FFFFFF"

###################################################################################
app = Dash(__name__,external_stylesheets=[dbc.themes.SLATE])
server=app.server
app.title = 'Datos Exoesqueleto' ## Tittle in the web page
app._favicon = ("iconn.ico") 

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

    dcc.Dropdown(['Hombre', 'Mujer'], 'Hombre',id='gender-dropdown',className='banner_d'),

    #dcc.RadioItems([{ "label": html.Div(['Hombre'], style={'color': 'Gold', 'font-size': 20}),"value":"Hombre"},{ "label": "  Mujer","value":"Mujer"}],
    #               'Hombre',id='gender-dropdown',className='banner_d', inline=True),
    
    html.Button('Empezar', n_clicks=0, id='start_butt',className='button1'),
    

    dbc.Row([ 

        dbc.Col([
            dcc.Graph(id = 'graph_torque_final', animate = True, className="Graph_izq")
        ]),

        dbc.Col([
            dcc.Graph(id = 'graph_realidad_virtual', animate = True, className="Graph_izq")
        ]),

        dbc.Col([
            dcc.Graph(id = 'graph_disposicion_final', animate = True, className="Graph_der"),
        ]),

    ],className="Fila_1"),

    dbc.Row([ 

        dbc.Col([
            dcc.Graph(id = 'graph_int_torque_final', animate = True, className="Graph_izq")
        ]),

        dbc.Col([
            dcc.Graph(id = 'graph_cont_torque_final', animate = True, className="Graph_der"),
        ]),

    ],className="Fila_1"),


    dcc.Interval(
        id = 'graph-update',
        interval = 10000,
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
    Input('gender-dropdown', 'value'),
)
def change_button_style(n_clicks,emocion,espa,dolor,rv,gender):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'start_butt' in changed_id:
        Google.define_in(emocion,espa,dolor,rv,gender,0)
        return True




@app.callback(
    Output("graph_torque_final", "figure"), 
    Output("graph_disposicion_final", "figure"), 
    Output("graph_int_torque_final", "figure"), 
    Output("graph_cont_torque_final", "figure"), 
    Output("graph_realidad_virtual", "figure"), 
    Output("graph_torque_final", "animate"), 
    Output("graph_disposicion_final", "animate"), 
    Output("graph_int_torque_final", "animate"), 
    Output("graph_cont_torque_final", "animate"), 
    Output("graph_realidad_virtual", "animate"), 
    Input('graph-update', 'n_intervals'),
)
def graph_toqrque(n_intervals):
    max_row = Google.get_max()
    if(max_row>0):
        min_val = max_row-val2print
        
        if(max_row<val2show):
            val2show_local= max_row
        else:
            val2show_local = val2show
        
        if(min_val<=0):min_val=1
        flag_animate = True
        vec_read = Google.read_data(min_val,max_row)  
        
        #[timestamp, emocion,espasticidad,dolor,ambienteRV, disposicion, intensidad_torque, torque_control, torque_Final, stop]
        time_stamp_global= vec_read[0]
        Torque_global = vec_read[8]
        Dispo_global = vec_read[5]
        Inten_Torque = vec_read[6]
        Cont_Torque = vec_read[7]
        Realidad_v = vec_read[4]
        

        data_torque = go.Scatter(
                x=time_stamp_global,
                y=Torque_global,
                name='Scatter',
                mode= 'lines+markers'
        )

        data_dispo = go.Scatter(
                x=time_stamp_global,
                y=Dispo_global,
                name='Scatter',
                mode= 'lines+markers'
        )

        data_int_torq = go.Scatter(
                x=time_stamp_global,
                y=Inten_Torque,
                name='Scatter',
                mode= 'lines+markers'
        )

        data_cont_torq = go.Scatter(
                x=time_stamp_global,
                y=Cont_Torque,
                name='Scatter',
                mode= 'lines+markers'
        )

        data_realidad = go.Scatter(
                x=time_stamp_global,
                y=Realidad_v,
                name='Scatter',
                mode= 'lines+markers'
        )


        rango_minimo_x = min(time_stamp_global[-val2show_local-1:-1])
        rango_maximo_x = max(time_stamp_global[-val2show_local-1:-1])

        rango_minimo_torque= min(Torque_global[-val2show_local-1:-1])
        rango_maximo_torque = max(Torque_global[-val2show_local-1:-1])

        rango_minimo_dispo= min(Dispo_global[-val2show_local-1:-1])
        rango_maximo_dispo= max(Dispo_global[-val2show_local-1:-1])

        rango_minimo_int_tor= min(Inten_Torque[-val2show_local-1:-1])
        rango_maximo_int_tor= max(Inten_Torque[-val2show_local-1:-1])       

        rango_minimo_cont_tor= min(Cont_Torque[-val2show_local-1:-1])
        rango_maximo_cont_tor= max(Cont_Torque[-val2show_local-1:-1])

        rango_minimo_realidad= min(Realidad_v[-val2show_local-1:-1])
        rango_maximo_realidad= max(Realidad_v[-val2show_local-1:-1])

    else:
        flag_animate = False
        data_torque = go.Scatter(
            x=[],
            y=[],
            name='Scatter',
            mode= 'lines+markers'
        )

        data_dispo = go.Scatter(
            x=[],
            y=[],
            name='Scatter',
            mode= 'lines+markers'
        )

        data_int_torq = go.Scatter(
                x=[],
                y=[],
                name='Scatter',
                mode= 'lines+markers'
        )

        data_cont_torq = go.Scatter(
                x=[],
                y=[],
                name='Scatter',
                mode= 'lines+markers'
        )

        data_realidad = go.Scatter(
                x=[],
                y=[],
                name='Scatter',
                mode= 'lines+markers'
        )

        time_stamp_global=[0]
        Torque_global = [0]
        Dispo_global = [0]
        Inten_Torque = [0]
        Cont_Torque = [0]
        Realidad_v = [0]

        rango_minimo_x = 0
        rango_maximo_x = 1

        rango_minimo_torque= 0
        rango_maximo_torque = 1

        rango_minimo_dispo= 0
        rango_maximo_dispo= 1

        rango_minimo_int_tor= 0
        rango_maximo_int_tor= 1     

        rango_minimo_cont_tor= 0
        rango_maximo_cont_tor= 1

        rango_minimo_realidad= 0
        rango_maximo_realidad= 1

    return {'data'   : [data_torque],
            'layout' : go.Layout(xaxis=dict(range=[rango_minimo_x,rango_maximo_x],color="#f1f1f1"),yaxis = dict(range = [rango_minimo_torque,rango_maximo_torque],color="#f1f1f1"),
            title=dict(text="Grafica Torque",font=dict(color="#f1f1f1")), plot_bgcolor ='#141316',paper_bgcolor='#818d9b')
            },{'data'   : [data_dispo],
            'layout' : go.Layout(xaxis=dict(range=[rango_minimo_x,rango_maximo_x],color="#f1f1f1"),yaxis = dict(range = [rango_minimo_dispo,rango_maximo_dispo],color="#f1f1f1"),
            title=dict(text="Grafica Disposición",font=dict(color="#f1f1f1")), plot_bgcolor ='#141316',paper_bgcolor='#818d9b')
            },{'data'   : [data_int_torq],
            'layout' : go.Layout(xaxis=dict(range=[rango_minimo_x,rango_maximo_x],color="#f1f1f1"),yaxis = dict(range = [rango_minimo_int_tor,rango_maximo_int_tor],color="#f1f1f1"),
            title=dict(text="Grafica Intensidad Torque",font=dict(color="#f1f1f1")), plot_bgcolor ='#141316',paper_bgcolor='#818d9b')
            },{'data'   : [data_cont_torq],
            'layout' : go.Layout(xaxis=dict(range=[rango_minimo_x,rango_maximo_x],color="#f1f1f1"),yaxis = dict(range = [rango_minimo_cont_tor,rango_maximo_cont_tor],color="#f1f1f1"),
            title=dict(text="Grafica Control Torque",font=dict(color="#f1f1f1")), plot_bgcolor ='#141316',paper_bgcolor='#818d9b')
            },{'data'   : [data_realidad],
            'layout' : go.Layout(xaxis=dict(range=[rango_minimo_x,rango_maximo_x],color="#f1f1f1"),yaxis = dict(range = [rango_minimo_realidad,rango_maximo_realidad],color="#f1f1f1"),
            title=dict(text="Grafica Ambiente Virtual",font=dict(color="#f1f1f1")), plot_bgcolor ='#141316',paper_bgcolor='#818d9b')
            },flag_animate,flag_animate,flag_animate,flag_animate,flag_animate



###################################################################################


if __name__ == '__main__':
    app.run_server(debug=True)