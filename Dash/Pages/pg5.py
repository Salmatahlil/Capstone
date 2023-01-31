import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import numpy as np

import joblib
import io
import base64
from base64 import b64encode

import xgboost as xgb
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

dash.register_page(__name__, name= 'ML algorithims')
# loaded_model = joblib.load('finalized_model.sav')

# print(loaded_model)

temperature_data = pd.read_csv('cleaned_temperature_data_US.csv')
temperature_data = temperature_data[temperature_data["year"] <= 2021]
temps = temperature_data.groupby('year')['net_difference'].mean()
emissions_data = pd.read_csv('GCB2022v27_MtCO2_flat.csv')
emissions_data = emissions_data[emissions_data['Year'] >= 1950]
emissions_data = emissions_data[emissions_data['Country'] == 'Global']
emissions_data["temperature_diffs"] = temps.values
# set up X without target variable, make y only target
X = emissions_data.drop(["Country", "ISO 3166-1 alpha-3", "Other", "temperature_diffs", "Year"], axis = 1)
y = emissions_data["temperature_diffs"]

# set seed for reproducibility, then create training and testing splits
seed = 1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=seed)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_train = pd.DataFrame(X_train, columns=X.columns)
X_test = pd.DataFrame(X_test, columns=X.columns)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


reg = xgb.XGBRegressor(n_estimators=1000)
reg.fit(X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=False,
    ) # Change verbose to True if you want to see it train


reg_yhat = reg.predict(X_test)
clf = svm.SVR(C=100, kernel = 'rbf')
clf.fit(X_train, y_train)
clf_yhat = clf.predict(X_test)

lr = LinearRegression()
lr.fit(X_train, y_train)
lr_yhat = lr.predict(X_test)

def residuals_XG():
    residuals = reg_yhat - y_test
    residuals.sort_index(ascending=True, inplace=True)


    fig = px.line(x=residuals.keys(), y=residuals.values, title='Residuals of XGBoost Model')

    fig2 = px.scatter(x=residuals.keys(), y=residuals.values, trendline='ols', trendline_color_override='#C70039')
    fig2.data[1].name = 'Residual Trendline'
    fig2.data[1].showlegend = True

    fig.add_trace(fig2.data[1])

    fig.update_layout(height=600, width=600, template='plotly_dark')

    return fig

def y_test_sorted():
    y_test_sorted= y_test.sort_index(ascending=True)
    fig = make_subplots()
    fig.add_trace(
        go.Scatter(x=y_test_sorted.keys(), y=y_test_sorted.values, name='Actual Values', mode='lines', line=dict(color="#FFC300"))
    )
    fig.add_trace(
        go.Scatter(x=y_test_sorted.keys(), y=reg_yhat, name='Predicted Values', mode='lines', line=dict(color="#4462FA"))
    )
    # Add figure title
    fig.update_layout(
        title_text="XGBoost Test Set"
    )
    # Set x-axis title
    fig.update_xaxes(title_text="Index")
    # Set y-axes titles
    fig.update_yaxes(title_text="Net Temperature Difference", secondary_y=False)
    fig.update_layout(height=600, width=1200, template='plotly_dark')
    return fig

def residuals_SVM():
    residuals = clf_yhat - y_test
    residuals.sort_index(ascending=True, inplace=True)

    fig = px.line(x=residuals.keys(), y=residuals.values, title='Residuals of SVM Model')
    fig2 = px.scatter(x=residuals.keys(), y=residuals.values, trendline='ols', trendline_color_override='#C70039')
    fig2.data[1].name = 'Residual Trendline'
    fig2.data[1].showlegend = True
    fig.add_trace(fig2.data[1])
    fig.update_layout(height=600, width=600, template='plotly_dark')

    return fig

def y_test_SVM():
    y_test_sorted= y_test.sort_index(ascending=True)
    fig = make_subplots()

    fig.add_trace(
        go.Scatter(x=y_test_sorted.keys(), y=y_test_sorted.values, name='Actual Values', mode='lines', line=dict(color="#FFC300"))
    )

    fig.add_trace(
        go.Scatter(x=y_test_sorted.keys(), y=clf_yhat, name='Predicted Values', mode='lines', line=dict(color="#4462FA"))
    )
    # Add figure title
    fig.update_layout(
        title_text="Support Vector Machine Test Set"
    )
    # Set x-axis title
    fig.update_xaxes(title_text="Index")
    # Set y-axes titles
    fig.update_yaxes(title_text="Net Temperature Difference", secondary_y=False)
    fig.update_layout(height=600, width=1200, template='plotly_dark')

    return fig

def residuals_LR():
    residuals = lr_yhat - y_test
    residuals.sort_index(ascending=True, inplace=True)

    fig = px.line(x=residuals.keys(), y=residuals.values, title='Residuals of LR Model')
    # print(fig.data[1])
    # fig.data[1].showlegend = True

    fig2 = px.scatter(x=residuals.keys(), y=residuals.values, trendline='ols', trendline_color_override='#C70039')
    fig2.data[1].name = 'Residual Trendline'
    fig2.data[1].showlegend = True

    fig.add_trace(fig2.data[1])

    fig.update_layout(height=600, width=600, template='plotly_dark')
    
    return fig

def linear():
    y_test_sorted= y_test.sort_index(ascending=True)
    fig = make_subplots()
    fig.add_trace(
        go.Scatter(x=y_test_sorted.keys(), y=y_test_sorted.values, name='Actual Values', mode='lines', line=dict(color="#FFC300"))
    )
    fig.add_trace(
        go.Scatter(x=y_test_sorted.keys(), y=lr_yhat, name='Predicted Values', mode='lines', line=dict(color="#4462FA"))
    )
    # Add figure title
    fig.update_layout(
        title_text="Linear Regression Test Set"
    )
    # Set x-axis title
    fig.update_xaxes(title_text="Index")
    # Set y-axes titles
    fig.update_yaxes(title_text="Net Temperature Difference", secondary_y=False)
    fig.update_layout(height=600, width=1200, template='plotly_dark')

    return fig




layout = dbc.Container([
    dbc.Col ([
    html.Div([
    dcc.RadioItems(
        id='render-option',
        options=['image'],
        value='image'
    ),
    html.Div(id='output')],
        style={'width': '53%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),
 
    dbc.Row([dbc.Col ([
            dcc.Graph(
        id='temp-graph',
        figure=residuals_XG())
        ],  width={'size': 4, 'offset': 6},
        style={'width': '47%', 'display': 'inline-block',
                                 'border-radius': '15px',
                                 'box-shadow': '8px 8px 8px grey',
                                 'background-color': 'black',
                                 'padding': '10px',
                                 'margin-bottom': '10px'
                                 }),
    dbc.Col ([
        dcc.Graph(
            id='y_test',
            figure= y_test_sorted())
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
            id='residual2',
            figure= residuals_SVM())
            ],  width={'size': 5, 'offset': 0},
            style={'width': '47%', 'display': 'inline-block',
                                    'border-radius': '15px',
                                    'box-shadow': '8px 8px 8px grey',
                                    'background-color': 'black',
                                    'padding': '10px',
                                    'margin-bottom': '10px'
                                    }),  
    dbc.Col ([
        dcc.Graph(
            id='y_test2',
            figure= y_test_SVM())
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
            id='residual',
            figure= residuals_LR())
            ],  width={'size': 5, 'offset': 0},
            style={'width': '47%', 'display': 'inline-block',
                                    'border-radius': '15px',
                                    'box-shadow': '8px 8px 8px grey',
                                    'background-color': 'black',
                                    'padding': '10px',
                                    'margin-bottom': '10px'
                                    }),
    dbc.Col ([
        dcc.Graph(
            id='linear_graph',
            figure= linear())
            ],  width={'size': 5, 'offset': 0},
            style={'width': '93%', 'display': 'inline-block',
                                    'border-radius': '15px',
                                    'box-shadow': '8px 8px 8px grey',
                                    'background-color': 'black',
                                    'padding': '10px',
                                    'margin-bottom': '10px'
                                    }),                       
    ])
    ])
])

@callback(
    Output("output", "children"), 
    Input('render-option', 'value'))
def savefile(render_option):
    fig = plot_importance(reg,height=0.9)
    if render_option == 'image':
        buf = io.BytesIO() # in-memory files
        plt.savefig(buf, format = "png")
        data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
        img_b64 = "data:image/png;base64,{}".format(data)
        return html.Img(src=img_b64, style={'height': '500px'})
    else:
        return dcc.Graph(figure= fig)
    

# def savefile():
#     fig = plot_importance(reg,height=0.9)
    
#     buf = io.BytesIO() # in-memory files
#     plt.savefig(buf, format = "png")
#     data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
#     img_b64 = "data:image/png;base64,{}".format(data)
#     return html.Img(src=img_b64, style={'height': '500px'})
    

# layout= html.Div(children=[
#     html.H1(children='Hello Dash. Wills Dashboard!.'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='fig-1',
#         figure=savefile()
#     )])
