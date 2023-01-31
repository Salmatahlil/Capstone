import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pymssql
import joblib

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import plotly.offline as pyo
import numpy as np


from config import database
from config import table
from config import username
from config import password
from config import server


dash.register_page(__name__, name='API')

conn = pymssql.connect(server,username, password, database)
cursor = conn.cursor()

query = f"SELECT * FROM {table}"
df = pd.read_sql(query, conn)

df["datetime"] = pd.to_datetime(df[['year','month','day']])
df['trend_diff'] = df['atmospheric_trend'].diff()
df['cycle_diff'] = df['atmospheric_cycle'].diff()
data = df[["datetime", "atmospheric_cycle", "atmospheric_trend", "trend_diff", "cycle_diff"]]



def making_figure():
    fig = make_subplots()
    fig.add_trace(
        go.Scatter(x=data["datetime"], y=data["atmospheric_cycle"], name='Atmospheric CO2 Levels', mode='lines', line=dict(color="#FFC300"))
    )
    fig.add_trace(
        go.Scatter(x=data["datetime"], y=data["atmospheric_trend"], name='Atmospheric CO2 Levels Trend', mode='lines', line=dict(color="#4462FA"))
    )
    # Add figure title
    fig.update_layout(
        title_text="Global CO2 Emissions and US Storm Frequencies Together"
    )
    # Set x-axis title
    fig.update_xaxes(title_text="Year")
    # Set y-axes titles
    fig.update_yaxes(title_text="Global CO2 Emissions (Million Tons)", secondary_y=False)
    fig.update_yaxes(title_text="Yearly Number of Storms in US", secondary_y=True)

    fig.update_layout(height=500, width=1200, template='plotly_dark')

    return fig

####### Make into a card
timeframe = 145 #days
change_in_co2 = data[-timeframe:][["trend_diff", "cycle_diff"]].sum()
# print(f'''The overall change is co2 in the past {timeframe} days is {change_in_co2.values[1]} million tons. However, when we adjust this value to account for natural Earth CO2 processes, the true change in CO2 levels is {change_in_co2.values[0]} million tons.''')
timeframe = 30

def making_figure2():
    fig2 = make_subplots()
    fig2.add_trace(
        go.Scatter(x=data[-timeframe:]["datetime"], y=data[-timeframe:]["atmospheric_cycle"], name='Atmospheric CO2 Levels', mode='lines', line=dict(color="#FFC300"))
    )
    fig2.add_trace(
        go.Scatter(x=data[-timeframe:]["datetime"], y=data[-timeframe:]["atmospheric_trend"], name='Atmospheric CO2 Levels Trend', mode='lines', line=dict(color="#4462FA"))
    )
    # Add figure title
    fig2.update_layout(
        title_text="Global CO2 Emissions and US Storm Frequencies Together"
    )
    # Set x-axis title
    fig2.update_xaxes(title_text="Year")
    # Set y-axes titles
    fig2.update_yaxes(title_text="Global CO2 Emissions (Million Tons)", secondary_y=False)
    fig2.update_yaxes(title_text="Yearly Number of Storms in US", secondary_y=True)
    fig2.update_layout(height=500, width=1200, template='plotly_dark')

    return fig2

def making_figure3():
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(
        go.Scatter(x=data[-timeframe:]["datetime"], y=data[-timeframe:]["atmospheric_cycle"], name='Atmospheric CO2 Levels', mode='lines', line=dict(color="#FFC300")),
        secondary_y= False
    )
    fig3.add_trace(
        go.Scatter(x=data[-timeframe:]["datetime"], y=data[-timeframe:]["cycle_diff"], name='Daily CO2 Cycle Differences', mode='lines', line=dict(color="#069519")),
        secondary_y=True
    )
    # Add figure title
    fig3.update_layout(
        title_text="Global CO2 Emissions and US Storm Frequencies Together"
    )
    # Set x-axis title
    fig3.update_xaxes(title_text="Year")
    # Set y-axes titles
    fig3.update_yaxes(title_text="Global CO2 Emissions (Million Tons)", secondary_y=False)
    fig3.update_yaxes(title_text="Yearly Number of Storms in US", secondary_y=True)
    fig3.update_layout(height=500, width=1200, template='plotly_dark')

    return fig3


def making_figure4():
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(
        go.Scatter(x=data[-timeframe:]["datetime"], y=data[-timeframe:]["atmospheric_trend"], name='Atmospheric CO2 Levels Trend', mode='lines', line=dict(color="#4462FA")),
        secondary_y=False
    )
    fig4.add_trace(
        go.Scatter(x=data[-timeframe:]["datetime"], y=data[-timeframe:]["trend_diff"], name='Daily CO2 Trend Differences', mode='markers', line=dict(color="#66108B")),
        secondary_y=True
    )
    # Add figure title
    fig4.update_layout(
        title_text="Global CO2 Emissions and US Storm Frequencies Together"
    )
    # Set x-axis title
    fig4.update_xaxes(title_text="Year")
    # Set y-axes titles
    fig4.update_yaxes(title_text="Global CO2 Emissions (Million Tons)", secondary_y=False)
    fig4.update_yaxes(title_text="Yearly Number of Storms in US", secondary_y=True)
    fig4.update_layout(height=500, width=1200, template='plotly_dark')

    return fig4
    
df= making_figure()
df1= making_figure2()
df2= making_figure3()
df3= making_figure4()




layout=dbc.Container([
 
    dbc.Col ([
            dcc.Graph(
        id='example-graph8',
        figure= making_figure())
        ],  width={'size': 5, 'offset': 0},
        style={'width': '96%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

                                 }),
    dbc.Col([
               dcc.Graph(
            id='example-graph',
            figure=making_figure2())
            ], width={'size': 5, 'offset': 0}, 
            style={'width': '96%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

                                 }),
    dbc.Col([
            dcc.Graph(
        id='example-graph2',
        figure=making_figure3())
        ], width={'size': 5, 'offset': 0}, 
        style={'width': '96%', 'display': 'inline-block',
                                'border-radius': '15px',
                                'box-shadow': '8px 8px 8px grey',
                                'background-color': 'black',
                                'padding': '10px',
                                'margin-bottom': '10px'

                                }),
     dbc.Col([
               dcc.Graph(
            id='example-graph3',
            figure= making_figure4())
            ], width={'size': 5, 'offset': 0}, 
            style={'width': '96%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

                                 })
        # dcc.Interval(
        #     id='interval-component',
        #     interval=5*1000, # in milliseconds
        #     n_intervals=0
        #     )


])

# @callback(
#     Output('example-graph8', 'figure'),
#     Input('interval-component', 'n_intervals')
# )
# def update_figure_1(n_intervals=None):
#     return making_figure()