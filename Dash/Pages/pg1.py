import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np

dash.register_page(__name__, path='/', name= 'Emissions')

# page 1 data

#read data
co2 = pd.read_csv('cleaned_energy.csv')


world= co2.loc[co2['Country'] == 'World']
cont= co2.loc[co2['Country'] != 'World']
contALL= cont.loc[cont['Energy_type'] == 'all_energy_types']

#fig1
fig= px.box(contALL, y='CO2_emission', animation_frame= 'Year', color='Continent', title="CO2 Emissions IQR change of Continents", template= 'plotly_dark')
fig.update_yaxes(type='log')
fig.update_layout({
    'title':
    {'x': 0.5, 
    'y': 0.9},
    'yaxis': {
    'title' : 'CO2 Emissions (MMtonnes CO2)',
    }})


fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

## fig2
NA= contALL.loc[contALL['Continent'] == 'North America'][['Country', 'Year', 'CO2_emission']]
w= world[world['Energy_type'] != 'all_energy_types']
world_emission= w.groupby('Year')['CO2_emission'].median().reset_index()
NA_emission= NA.groupby('Year')['CO2_emission'].median().reset_index()
world_emission['Country']= ['World']*len(world_emission)
NA_emission['Country']= ['North America']*len(NA_emission)
NA_emit= pd.concat([NA, world_emission])
NA_emit= pd.concat([NA_emit, NA_emission])



NA_plot= NA_emit[NA_emit['Year']== 2019].sort_values(by='CO2_emission', ascending=False).reset_index(drop=True)
colors= ['#03588C']*len(NA_plot.index)
colors[np.where(NA_plot['Country'] == 'World')[0][0]] = 'purple'
colors[np.where(NA_plot['Country'] == 'North America')[0][0]] = 'gold'

fig2= go.Figure()
fig2.add_trace(go.Bar(x= NA_plot['Country'], y= NA_plot['CO2_emission'], marker_color= colors, ))
fig2.update_yaxes(type='log')


fig2.update_layout(
{
    'title': { 
    'text': f"CO2 Emissions of North American Countries 2019",
    'x' : 0.5,
    'y': 0.9,
    'font': {'size': 20}
    },
    'xaxis' : {
    'title' : 'Countries',
    'tickfont': {'size' : 10},
    'showticklabels': True
    },
    'yaxis': {
    'title' : 'CO2 Emissions (MMtonnes CO2(log))',
    'tickfont': {'size' : 10}
    },
    'template' : 'plotly_dark'
}
)
# df3 = df2
# df4= df3
countries = contALL
top_countries = countries.groupby('Country').sum().sort_values(by='CO2_emission', ascending=False).head(10)

fig4= go.Figure()

fig4.add_trace(go.Bar(x= top_countries.index, y= top_countries['CO2_emission']))
fig4.update_yaxes(type='log')

fig4.update_layout(
    {
        'title': { 
        'text': f"Top Ten Countries of CO2 Emissions",
        'x' : 0.5,
        'y': 0.9,
        'font': {'size': 20}
        },
        'xaxis' : {
        'title' : 'Countries',
        'tickfont': {'size' : 10},
        'showticklabels': True
        },
        'yaxis': {
        'title' : 'CO2 Emissions (MMtonnes CO2)',
        'tickfont': {'size' : 10}
        },
        'template' : 'plotly_dark'
    }
)
# df5 = df4
line1 = go.Scatter(x=countries[countries['Country'] == 'United States']['Year'],
                    y=countries[countries['Country'] == 'United States']['CO2_emission'],
                    mode='lines',
                    name='United States')
line2 = go.Scatter(x=countries[countries['Country'] == 'China']['Year'],
                    y=countries[countries['Country'] == 'China']['CO2_emission'],
                    mode='lines',
                    name='China')
line3 = go.Scatter(x=countries[countries['Country'] == 'Russia']['Year'],
                    y=countries[countries['Country'] == 'Russia']['CO2_emission'],
                    mode='lines',
                    name='Russia')
line4 = go.Scatter(x=countries[countries['Country'] == 'Germany']['Year'],
                    y=countries[countries['Country'] == 'Germany']['CO2_emission'],
                    mode='lines',
                    name='Germany')
line5 = go.Scatter(x=countries[countries['Country'] == 'United Kingdom']['Year'],
                    y=countries[countries['Country'] == 'United Kingdom']['CO2_emission'],
                    mode='lines',
                    name='United Kingdom')

# Create the layout
layout = go.Layout(title='CO2 Emissions of Top 5 Consumers from 1988-2019 ',
                   yaxis=dict(title='CO2 Emissions (MMtonnes CO2)'),
                   xaxis=dict(title='Years'),
                   template = 'plotly_dark')

# Create the figure
fig5 = go.Figure(data=[line1, line2, line3, line4, line5], layout=layout)

# df6 = df5
line1 = go.Scatter(x=countries[countries['Country'] == 'United States']['Year'],
                    y=countries[countries['Country'] == 'United States']['GDP'],
                    mode='lines',
                    name='United States')
line2 = go.Scatter(x=countries[countries['Country'] == 'China']['Year'],
                    y=countries[countries['Country'] == 'China']['GDP'],
                    mode='lines',
                    name='China')
line3 = go.Scatter(x=countries[countries['Country'] == 'Russia']['Year'],
                    y=countries[countries['Country'] == 'Russia']['GDP'],
                    mode='lines',
                    name='Russia')
line4 = go.Scatter(x=countries[countries['Country'] == 'Germany']['Year'],
                    y=countries[countries['Country'] == 'Germany']['GDP'],
                    mode='lines',
                    name='Germany')
line5 = go.Scatter(x=countries[countries['Country'] == 'United Kingdom']['Year'],
                    y=countries[countries['Country'] == 'United Kingdom']['GDP'],
                    mode='lines',
                    name='United Kingdom')

# Create the layout
layout = go.Layout(title='GDP over the years of Top 5 Consumers',
                   yaxis=dict(title='GDP (Billion 2015$ PPP)'),
                   xaxis=dict(title='Years'),
                   template = 'plotly_dark')

# Create the figure
fig6 = go.Figure(data=[line1, line2, line3, line4, line5], layout=layout)

# df7 = df6
line1 = go.Scatter(x=countries[countries['Country'] == 'United States']['Year'],
                    y=countries[countries['Country'] == 'United States']['Energy_intensity_by_GDP'],
                    mode='lines',
                    name='United States')
line2 = go.Scatter(x=countries[countries['Country'] == 'China']['Year'],
                    y=countries[countries['Country'] == 'China']['Energy_intensity_by_GDP'],
                    mode='lines',
                    name='China')
line3 = go.Scatter(x=countries[countries['Country'] == 'Russia']['Year'],
                    y=countries[countries['Country'] == 'Russia']['Energy_intensity_by_GDP'],
                    mode='lines',
                    name='Russia')
line4 = go.Scatter(x=countries[countries['Country'] == 'Germany']['Year'],
                    y=countries[countries['Country'] == 'Germany']['Energy_intensity_by_GDP'],
                    mode='lines',
                    name='Germany')
line5 = go.Scatter(x=countries[countries['Country'] == 'United Kingdom']['Year'],
                    y=countries[countries['Country'] == 'United Kingdom']['Energy_intensity_by_GDP'],
                    mode='lines',
                    name='United Kingdom')

# Create the layout
layout = go.Layout(title='Energy Intensity by GDP of Top 5 Consumers',
                   yaxis=dict(title='Energy Intensity (1000 Btu/GDP)'),
                   xaxis=dict(title='Years'),
                   template = 'plotly_dark')

# Create the figure
fig7 = go.Figure(data=[line1, line2, line3, line4, line5], layout=layout)
# #put figured into dashboard's html
temp_Allc= contALL[['Country', 'Year', 'CO2_emission']].groupby(['Country','Year']).sum().reset_index()
temp_Allc
fig8= px.choropleth(data_frame=temp_Allc, locations= 'Country', locationmode= 'country names', animation_frame= 'Year', color= 'CO2_emission', template= 'plotly_dark', color_continuous_scale='Tropic')
        
fig8.update_layout(
    width=1000,
    height=620,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    title={
        'text': '<b>CO2 Emissions Over Time</b>',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    title_font_color='white',
    title_font_size=26,
    font=dict(
        family='Heebo', 
        size=18, 
        color='white'
    )
)

layout=dbc.Container([
 
    dbc.Row([dbc.Col ([
            dcc.Graph(
        id='example-graph8',
        figure=fig8)
        ],  width={'size': 12, 'offset': 1},
        style={'width': '78%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

                                 }),
    
        dbc.Row([
        dbc.Col ([
            dcc.Graph(
        id='first-graph',
        figure=fig)
        ],  width={'size': 6},
        style={'width': '50%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

                                 }),
        dbc.Col([
               dcc.Graph(
            id='example-graph',
            figure=fig2)
        ], width={'size': 5}, 
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
            id='example-graph4',
            figure=fig4) 
        ], width={'size': 5,'offset': 0},
        style={'width': '52%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),
                dbc.Col([  
                dcc.Graph(
            id='example-graph5',
            figure=fig5)
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
            id='example-graph6',
            figure=fig6) 
        ], width={'size': 5, "offset": 0},
        style={'width': '52%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),

                dbc.Col([  
                dcc.Graph(
                id='example-graph7',
                figure=fig7)
                ], width={'size': 6},
                style={'width': '46%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),  
 dcc.Interval(
        id= 'interval-component',
        interval = 5*1000,
        n_intervals= 0
    )

],)       

       
         ])
    ])
])

     















    