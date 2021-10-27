#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:56:21 2021

@author: montilla
"""

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)





app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])
#subset states for illustration purposes
states = ['California', 'New York', 'Texas'] 

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "Disease", "value": "Disease"},
                     {"label": "Other", "value": "Other"},
                     {"label": "Pesticides", "value": "Pesticides"},
                     {"label": "Pests_excl_Varroa", "value": "Pests_excl_Varroa"},
                     {"label": "Unknown", "value": "Unknown"},
                     {"label": "Varroa_mites", "value": "Varroa_mites"}],
                 multi=False,
                 value="Pesticides",
                 style={'width': "40%"}
                 ),
      # dcc.Checklist(
      #    id="checklist",
      #    options=[{"label": x, "value": x} 
      #             for x in states],
      #    value=states,
      #    labelStyle={'display': 'inline-block'}),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_line', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_line', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Currently showing bee-killer: {}".format(option_slctd)
    
    dff = df.copy()
    dff = dff[dff['State'].isin(states)]
    dff = dff[dff["Affected by"] == option_slctd]

    # Plotly Express
    fig = px.line(dff, x='Year', y='Pct of Colonies Impacted', color='State')
    fig.update_xaxes(dtick=1)

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)