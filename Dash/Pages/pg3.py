import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np
from plotly.subplots import make_subplots

dash.register_page(__name__, name='Storms')

world_emissions = pd.read_csv('world_emissions.csv')
world_emissions = world_emissions[world_emissions["Energy_type"] == 'all_energy_types']

temperatures = pd.read_csv("cleaned_temperature_data_US.csv")
temperatures = temperatures.groupby("year")["net_difference"].mean()
temperatures_filtered = temperatures[temperatures.keys() >= 1988]
temperatures_filtered = temperatures_filtered[temperatures_filtered.keys() <= 2019]
emissions = pd.read_csv('GCB2022v27_MtCO2_flat.csv')
emissions = emissions[emissions["Country"] == 'Global']
yearly_data = emissions.groupby('Year')["Total"].sum()
yearly_data = yearly_data[yearly_data.keys() >= 1950]

temperatures = temperatures[temperatures.keys() <= 2021]

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=yearly_data.keys(), y=yearly_data.values, name='Global Emissions', mode='markers', line=dict(color="#FFC300")),
    secondary_y=False
)

fig.add_trace(
    go.Scatter(x=temperatures.keys(), y=temperatures.values, name='Net Temperature Difference', mode='markers', line=dict(color="#C70039")),
    secondary_y=True
)

fig2 = px.scatter(x=yearly_data.keys(), y=yearly_data.values, trendline='lowess', trendline_color_override="#FFC300")
fig2.data[1].name = 'CO2 Emissions Trendline'
fig2.data[1].showlegend = True

fig3 = px.scatter(x=temperatures.keys(), y=temperatures.values, trendline='lowess', trendline_color_override="#C70039")
fig3.data[1].name = 'Net Temperature Diff Trendline'
fig3.data[1].showlegend = True

fig.add_trace(fig2.data[1])
fig.add_trace(fig3.data[1], secondary_y=True)

# Add figure title
fig.update_layout(
    title_text="Global CO2 Emissions and US Temperature Increase Together"
)

# Set x-axis title
fig.update_xaxes(title_text="Year")

# Set y-axes titles
fig.update_yaxes(title_text="Global CO2 Emissions (Million Tons)", secondary_y=False)
fig.update_yaxes(title_text="Yearly Average Temperature Increase from Historical Average (Degrees F)", secondary_y=True)

fig.update_layout(height=800, width=750, template='plotly_dark')


#figure 2 
storm= pd.read_csv('cleaned_storm_data.csv')
storm = storm.drop_duplicates(subset=["Weather_type", "State", "Year", "Month"])
storm_frequencies = storm.groupby("Year")["Weather_type"].count()
storm_frequencies = storm_frequencies[storm_frequencies.keys() <= 2021]
yearly_data_storm = yearly_data[yearly_data.keys() >= 1996]


fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4.add_trace(
    go.Scatter(x=yearly_data_storm.keys(), y=yearly_data_storm.values, name='Global Emissions', mode='markers', line=dict(color="#FFC300")),
    secondary_y=False
)

fig4.add_trace(
    go.Scatter(x=storm_frequencies.keys(), y=storm_frequencies.values, name='Storm Frequencies', mode='markers', line=dict(color="#4462FA")),
    secondary_y=True
)
fig2 = px.scatter(x=yearly_data_storm.keys(), y=yearly_data_storm.values, trendline='lowess', trendline_color_override="#FFC300")
fig2.data[1].name = 'CO2 Emissions Trendline'
fig2.data[1].showlegend = True
fig3 = px.scatter(x=storm_frequencies.keys(), y=storm_frequencies.values, trendline='lowess', trendline_color_override="#4462FA")
fig3.data[1].name = 'Storm Frequency Lowess Trendline'
fig3.data[1].showlegend = True

fig4.add_trace(fig2.data[1])
fig4.add_trace(fig3.data[1], secondary_y=True)

# Add figure title
fig4.update_layout(
    title_text="Global CO2 Emissions and US Storm Frequencies Together"
)

# Set x-axis title
fig4.update_xaxes(title_text="Year")

# Set y-axes titles
fig4.update_yaxes(title_text="Global CO2 Emissions (Million Tons)", secondary_y=False)
fig4.update_yaxes(title_text="Yearly Number of Storms in US", secondary_y=True)

fig4.update_layout(height=800, width=750, template='plotly_dark')

 #figure 3
hurricanes = storm[(storm["Weather_type"] == 'Hurricane') | (storm["Weather_type"] == 'Hurricane (Typhoon)') | (storm["Weather_type"] == 'Marine Hurricane/Typhoon')]
hurricanes = hurricanes.drop_duplicates(subset=["State", "Year", "Month"])
hurricane_data = hurricanes.groupby("Year")["Weather_type"].count()
px.scatter(x=hurricane_data.keys(), y=hurricane_data.values, trendline='lowess')

tropical_storms = storm[storm["Weather_type"] == 'Tropical Storm']
tropical_storms = tropical_storms.drop_duplicates(subset=["State", "Year", "Month"])
tropical_storm_data = tropical_storms.groupby("Year")["Weather_type"].count()
px.scatter(x=tropical_storm_data.keys(), y=tropical_storm_data.values, trendline='lowess')

excessive_heat = storm[storm["Weather_type"] == 'Excessive Heat']
excessive_heat = excessive_heat.drop_duplicates(subset=["State", "Year", "Month"])
excessive_heat_data = excessive_heat.groupby("Year")["Weather_type"].count()
px.scatter(x=excessive_heat_data.keys(), y=excessive_heat_data.values, trendline='lowess')

blizzards = storm[storm["Weather_type"] == 'Blizzard']
blizzards = blizzards.drop_duplicates(subset=["State", "Year", "Month"])
blizzard_data = blizzards.groupby("Year")["Weather_type"].count()
px.scatter(x=blizzard_data.keys(), y=blizzard_data.values, trendline='lowess')

droughts = storm[storm["Weather_type"] == 'Drought']
droughts = droughts.drop_duplicates(subset=["State", "Year", "Month"])
drought_data = droughts.groupby("Year")["Weather_type"].count()
px.scatter(x=drought_data.keys(), y=drought_data.values, trendline='lowess')

floods = storm[storm["Weather_type"] == 'Flood']
floods = floods.drop_duplicates(subset=["State", "Year", "Month"])
flood_data = floods.groupby("Year")["Weather_type"].count()
px.scatter(x=flood_data.keys(), y=flood_data.values, trendline='lowess')

fig5 = make_subplots(specs=[[{"secondary_y": True}]])

fig5.add_trace(
    go.Scatter(x=yearly_data_storm.keys(), y=yearly_data_storm.values, name='Global Emissions', mode='markers', line=dict(color="#FFC300")),
    secondary_y=False
)

fig5.add_trace(
    go.Scatter(x=flood_data.keys(), y=flood_data.values, name='Flood Frequencies', mode='markers', line=dict(color="#4462FA")),
    secondary_y=True
)

fig5.add_trace(
    go.Scatter(x=drought_data.keys(), y=drought_data.values, name='Drought Frequencies', mode='markers', line=dict(color="#66108B")),
    secondary_y=True
)

fig6 = px.scatter(x=yearly_data_storm.keys(), y=yearly_data_storm.values, trendline='lowess', trendline_color_override="#FFC300")
fig6.data[1].name = 'CO2 Emissions Trendline'
fig2.data[1].showlegend = True
fig7 = px.scatter(x=flood_data.keys(), y=flood_data.values, trendline='ols', trendline_color_override="#4462FA")
fig7.data[1].name = 'Flood Frequency Trendline'
fig7.data[1].showlegend = True
fig8 = px.scatter(x=drought_data.keys(), y=drought_data.values, trendline='ols', trendline_color_override="#66108B")
fig8.data[1].name = 'Drought Frequency Trendline'
fig8.data[1].showlegend = True

fig5.add_trace(fig6.data[1])
fig5.add_trace(fig7.data[1], secondary_y=True)
fig5.add_trace(fig8.data[1], secondary_y=True)

# Add figure title
fig5.update_layout(
    title_text="Global CO2 Emissions and US Storm Frequencies Together"
)

# Set x-axis title
fig5.update_xaxes(title_text="Year")

# Set y-axes titles
fig5.update_yaxes(title_text="Global CO2 Emissions (Million Tons)", secondary_y=False)
fig5.update_yaxes(title_text="Yearly Number of Storms in US", secondary_y=True)

fig5.update_layout(height=800, width=750, template='plotly_dark')

#figure 4
fig9 = make_subplots(specs=[[{"secondary_y": True}]])

fig9.add_trace(
    go.Scatter(x=yearly_data_storm.keys(), y=yearly_data_storm.values, name='Global Emissions', mode='markers', line=dict(color="#FFC300")),
    secondary_y=False
)

fig9.add_trace(
    go.Scatter(x=blizzard_data.keys(), y=blizzard_data.values, name='Blizzard Frequencies', mode='markers', line=dict(color="#24EBE7")),
    secondary_y=True
)

fig9.add_trace(
    go.Scatter(x=excessive_heat_data.keys(), y=excessive_heat_data.values, name='Excessive Heat Frequencies', mode='markers', line=dict(color="#2D9A0B")),
    secondary_y=True
)

fig10 = px.scatter(x=yearly_data_storm.keys(), y=yearly_data_storm.values, trendline='lowess', trendline_color_override="#FFC300")
fig10.data[1].name = 'CO2 Emissions Trendline'
fig10.data[1].showlegend = True
fig11 = px.scatter(x=blizzard_data.keys(), y=blizzard_data.values, trendline='ols', trendline_color_override="#24EBE7")
fig11.data[1].name = 'Blizzard Frequency Trendline'
fig11.data[1].showlegend = True
fig12 = px.scatter(x=excessive_heat_data.keys(), y=excessive_heat_data.values, trendline='ols', trendline_color_override="#2D9A0B")
fig12.data[1].name = 'Excessive Heat Frequency Trendline'
fig12.data[1].showlegend = True

fig9.add_trace(fig10.data[1])
fig9.add_trace(fig11.data[1], secondary_y=True)
fig9.add_trace(fig12.data[1], secondary_y=True)

# Add figure title
fig9.update_layout(
    title_text="Global CO2 Emissions and US Storm Frequencies Together"
)

# Set x-axis title
fig9.update_xaxes(title_text="Year")

# Set y-axes titles
fig9.update_yaxes(title_text="Global CO2 Emissions (Million Tons)", secondary_y=False)
fig9.update_yaxes(title_text="Yearly Number of Storms in US", secondary_y=True)

fig9.update_layout(height=800, width=750, template='plotly_dark')



#layout 

layout=dbc.Container([
 
    dbc.Row([dbc.Col ([
            dcc.Graph(
        id='temp-graph',
        figure=fig)
        ],  width={'size': 4},
        style={'width': '60%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

                                    }),
    
        dbc.Col ([
            dcc.Graph(
        id='temp-graph',
        figure=fig4)
        ],  width={'size': 4, 'offset': 4},
        style={'width': '60%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

        
                         }),
        dbc.Row([
        dbc.Col([
               dcc.Graph(
            id='storm-graph',
            figure=fig5)
        ], width={'size': 4}, 
            style={'width': '60%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'

                                 }),
                                     dbc.Row([
        dbc.Col([
               dcc.Graph(
            id='storm-graph2',
            figure=fig9)
        ], width={'size': 4, 'offset': 5}, 
            style={'width': '62%', 'display': 'inline-block',
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