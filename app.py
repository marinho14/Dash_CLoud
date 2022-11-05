from dash import Dash, dash_table, html , Input, Output, State, dcc , callback_context
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import date
import firebase_admin
import numpy as np
app = Dash(__name__,external_stylesheets=[dbc.themes.SLATE])
###################################################################################

## https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/ 

# Example data (a circle).
resolution = 20
t = np.linspace(0, np.pi * 2, resolution)
x, y = np.cos(t), np.sin(t)
# Example app.
figure = dict(data=[{'x': [], 'y': []}], layout=dict(xaxis=dict(range=[-1, 1]), yaxis=dict(range=[-1, 1])))


###################################################################################
##app.title = 'Utms' ## Tittle in the web page
##app._favicon = ("assets/favicon.ico") Image in the webpage

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

])

###################################################################################
@app.callback(
    Output('alert-fade', 'is_open'),
    Input('submit-val', 'n_clicks'),
    Input('show-url', 'n_clicks'),
)


def func_1(n_clicks,n_clicks_2):
    pass
    return "is_open"
    

# @app.callback(
#     Output('alert-fade', 'is_open_2'),
#     Input('submit-val', 'n_clicks_2'),
#     Input('show-url', 'n_clicks_2'),
# )

# def func_2(n_clicks,n_clicks_2):
#     pass
#     return "is_open"

###################################################################################


if __name__ == '__main__':
    app.run_server(debug=True)