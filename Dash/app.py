import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import pymssql

from config import database
from config import table
from config import username
from config import password
from config import server

import pycountry_convert as pc
import numpy as np
import plotly.graph_objects as go
import plotly.offline as pyo



app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])


# app.layout = html.Div(children=[
#     html.H1(children='C02 Emissions Dashboard'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),
app.layout = dbc.Container([
    dbc.Row ([
        dbc.Col(html.H1('CO2 Emissions Dashboard',
                        className='text-center text-secondary, mb-4'),
                width = 12)
    ]),
    html.Div([
        dcc.Link(children=page['name']+"  |  ", href=page['path'])
        for page in dash.page_registry.values()

    ]),
    html.Hr(),

    # Content of each page
    dash.page_container
])  






if __name__ == '__main__':
    app.run_server(debug=True)