import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np
from plotly.subplots import make_subplots

dash.register_page(__name__, name='Energy Consumption')

co2 = pd.read_csv('cleaned_energy.csv')


cont= co2.loc[co2['Country'] != 'World']
us_etype_all= cont[cont['Country'] == 'United States']
us_etype_all= us_etype_all[us_etype_all['Energy_type'] != 'all_energy_types']
world= co2.loc[co2['Country'] == 'World']

#all energy types
contALL= cont.loc[cont['Energy_type'] == 'all_energy_types']


china_etype_all= cont[cont['Country'] == 'China']
china_etype_all= china_etype_all[china_etype_all['Energy_type'] != 'all_energy_types']

fig13= go.Figure()

figures = [
            px.line(us_etype_all, x= us_etype_all['Year'], y=us_etype_all['Energy_consumption'], symbol= us_etype_all['Energy_type'], color= us_etype_all['Energy_type']),
            px.line(china_etype_all, x= china_etype_all['Year'], y=china_etype_all['Energy_consumption'], symbol= china_etype_all['Energy_type'], color= china_etype_all['Energy_type'])
        ]

fig13 = make_subplots(rows=len(figures), cols=1, y_title="Energy Consumption", shared_xaxes=True, shared_yaxes= True, subplot_titles=("US Yearly Energy Consumption For Each Energy Type","China Yearly Energy Consumption For Each Energy Type")) 

for i, figure in enumerate(figures):
    for trace in range(len(figure["data"])):
        fig13.append_trace(figure["data"][trace], row=i+1, col=1)

        fig13.update_layout(
            {
                'title': { 
                'x' : 0.5,
                'y': 0.95,
                'font': {'size': 20}
                },
                'xaxis' : {
                'tickfont': {'size' : 8},
                'showticklabels': True
                },
                'yaxis': {
                'tickfont': {'size' : 8}
                },
                'template' : 'plotly_dark'
            }
        )
fig14= px.box(us_etype_all, y='Energy_consumption', color='Energy_type', title="US Total Energy Consumtion by Energy Type", template= 'plotly_dark')
fig14.update_layout({'title':{'x': 0.5, 'y': 0.9}})

fig15= px.box(china_etype_all, y='Energy_consumption', color='Energy_type', title="China's Total Energy Consumtion by Energy Type", template= 'plotly_dark')
fig15.update_layout({'title':{'x': 0.5, 'y': 0.9}})

contALL.head()
consumption= []
#sum of energy consumption
for i in contALL['Country'].unique():
    total= contALL[contALL['Country'] == i]['Energy_consumption'].sum(axis=0)
    consumption.extend([[i,total]])
#Making dataframe
consumption_data= pd.DataFrame(consumption, columns= ['Country', 'Total_Energy_Consumption'])
consumption_data= consumption_data.sort_values(by='Total_Energy_Consumption', ascending= False)
fig16= px.bar(consumption_data.head(10), x= 'Country', y='Total_Energy_Consumption', title= 'Top 10 Energy Consumers over time', template= 'plotly_dark')
fig16.update_layout(
        {
    'title':{
            'x': 0.5, 
            'y': 0.9},
    'xaxis' : {
            'tickfont': {'size' : 10},
         },
    'yaxis': {
            'title' : 'Total Energy Consumption (quad Btu)',
            'tickfont': {'size' : 10}
            }
        })


etype_coal= cont[cont['Energy_type'] == 'coal'].groupby(['Country'])['Energy_consumption'].sum().reset_index().sort_values(by='Energy_consumption', ascending= False)
etype_gas= cont[cont['Energy_type'] == 'natural_gas'].groupby(['Country'])['Energy_consumption'].sum().reset_index().sort_values(by='Energy_consumption', ascending= False)
etype_liquid= cont[cont['Energy_type'] == 'petroleum_n_other_liquids'].groupby(['Country'])['Energy_consumption'].sum().reset_index().sort_values(by='Energy_consumption', ascending= False)
etype_nuclear= cont[cont['Energy_type'] == 'nuclear'].groupby(['Country'])['Energy_consumption'].sum().reset_index().sort_values(by='Energy_consumption', ascending= False)
etype_renewable= cont[cont['Energy_type'] == 'renewables_n_other'].groupby(['Country'])['Energy_consumption'].sum().reset_index().sort_values(by='Energy_consumption', ascending= False)


fig17=px.bar(etype_coal.head(5), x= 'Country', y='Energy_consumption', title='Coal', template= 'plotly_dark')
fig17.update_layout(
        {
        'title':{
        
                'x': 0.5, 
                'y': 0.9},
        'xaxis' : {
                'title' : 'Country',
                'tickfont': {'size' : 8},
                },
        'yaxis': {
                'title' : 'Energy Consumption (quad Btu)',
                'tickfont': {'size' : 8}
                },
        'height' : 400,
        'width' : 550})

fig18= px.bar(etype_gas.head(5), x= 'Country', y='Energy_consumption', title= 'Natural Gas', template= 'plotly_dark')
fig18.update_layout(
        {
        'title':{
        
                'x': 0.5, 
                'y': 0.9},
        'xaxis' : {
                'title' : 'Country',
                'tickfont': {'size' : 8},
                },
        'yaxis': {
                'title' : 'Energy Consumption (quad Btu)',
                'tickfont': {'size' : 8}
                },
        'height' : 400,
        'width' : 550})

fig19= px.bar(etype_liquid.head(5), x= 'Country', y='Energy_consumption', title= 'Petroleum and other liquids', template= 'plotly_dark')
fig19.update_layout(
        {
        'title':{
        
                'x': 0.5, 
                'y': 0.9},
        'xaxis' : {
                'title' : 'Country',
                'tickfont': {'size' : 8},
                },
        'yaxis': {
                'title' : 'Energy Consumption (quad Btu)',
                'tickfont': {'size' : 8}
                },
        'height' : 400,
        'width' : 550})

fig20= px.bar(etype_nuclear.head(5), x= 'Country', y='Energy_consumption', title= 'Nuclear', template= 'plotly_dark')
fig20.update_layout(
        {
        'title':{
        
                'x': 0.5, 
                'y': 0.9},
        'xaxis' : {
                'title' : 'Country',
                'tickfont': {'size' : 8},
                },
        'yaxis': {
                'title' : 'Energy Consumption (quad Btu)',
                'tickfont': {'size' : 8}
                },
        'height' : 400,
        'width' : 550})
    
fig21= px.bar(etype_renewable.head(5), x= 'Country', y='Energy_consumption', title= 'Renewables and other', template= 'plotly_dark')
fig21.update_layout(
        {
        'title':{
        
                'x': 0.5, 
                'y': 0.9},
        'xaxis' : {
                'title' : 'Country',
                'tickfont': {'size' : 6},
                },
        'yaxis': {
                'title' : 'Energy Consumption (quad Btu)',
                'tickfont': {'size' : 6}
                },
        'height' : 400,
        'width' : 550})


    









layout=dbc.Container([
 
    dbc.Row([dbc.Col ([
            dcc.Graph(
        id='example-co2',
        figure=fig13)
        ],  width={'size': 12, 'offset': 1},
        style={'width': '78%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

                                 }),
        dbc.Col ([
        dcc.Graph(
            id='barplot_graph',
            figure= fig14)
            ],  width={'size': 5, 'offset': 0},
            style={'width': '93%', 'display': 'inline-block',
                                    'border-radius': '15px',
                                    'box-shadow': '8px 8px 8px grey',
                                    'background-color': 'black',
                                    'padding': '10px',
                                    'margin-bottom': '10px'
                                    }),   
        dbc.Col ([
        dcc.Graph(
            id='barplot_chinagraph',
            figure= fig15)
            ],  width={'size': 5, 'offset': 0},
            style={'width': '93%', 'display': 'inline-block',
                                    'border-radius': '15px',
                                    'box-shadow': '8px 8px 8px grey',
                                    'background-color': 'black',
                                    'padding': '10px',
                                    'margin-bottom': '10px'
                                    }),
         dbc.Col ([
        dcc.Graph(
            id='top10_graph',
            figure= fig16)
            ],  width={'size': 5, 'offset': 0},
            style={'width': '93%', 'display': 'inline-block',
                                    'border-radius': '15px',
                                    'box-shadow': '8px 8px 8px grey',
                                    'background-color': 'black',
                                    'padding': '10px',
                                    'margin-bottom': '10px'
                                    }),  
                dbc.Row([
                dbc.Col([
               dcc.Graph(
            id='coal-graph',
            figure=fig17) 
        ], width={'size': 5,'offset': 0},
        style={'width': '46%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),
                dbc.Col([  
                dcc.Graph(
            id='naturalgas-graph',
            figure=fig18)
    ], width={'size': 5,'offset': 0},
    style={'width': '46%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),
                                 dbc.Row([
                dbc.Col([
               dcc.Graph(
            id='petroleum-graph',
            figure=fig19) 
        ], width={'size': 5,'offset': 0},
        style={'width': '46%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),
                dbc.Col([  
                dcc.Graph(
            id='nuclear-graph',
            figure=fig20)
    ], width={'size': 5,'offset': 0},
    style={'width': '46%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),
                                           dbc.Col([  
                dcc.Graph(
            id='renewable-graph',
            figure=fig21)
    ], width={'size': 5,'offset': 0},
    style={'width': '46%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),
                         
    ])
    ])
])
])

