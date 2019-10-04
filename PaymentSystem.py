# -*- coding: utf-8 -*-

# %% Import and Data Cleaning

import pandas as pd

df = pd.read_csv('data.csv').loc[:,'Types of Transaction':'Type of Transaction']
df = df.dropna()
df['YrMo'] = df['Month'] + ' ' + df['Year'].astype(int).astype(str)
df['YrMo'] = pd.to_datetime(df['YrMo'], format='%b %Y')

#Yearly
df_3rd_yr = df[df['Type of Transaction']=='3rd Party'].groupby('Year').sum()
df_bsp_yr = df[df['Type of Transaction']=='BSP'].groupby('Year').sum()
df_tot_yr = df.groupby('Year').sum()

df_3rd_yr['Period'] = df_3rd_yr.index.astype(int)
df_bsp_yr['Period'] = df_bsp_yr.index.astype(int)
df_tot_yr['Period'] = df_tot_yr.index.astype(int)

#Monthly
df_3rd_mo = df[df['Type of Transaction']=='3rd Party'].groupby(df['YrMo']).sum()
df_bsp_mo = df[df['Type of Transaction']=='BSP'].groupby(df['YrMo']).sum()
df_tot_mo = df.groupby(df['YrMo']).sum()

df_3rd_mo['Period'] = df_3rd_mo.index.strftime('%Y %b')
df_bsp_mo['Period'] = df_bsp_mo.index.strftime('%Y %b')
df_tot_mo['Period'] = df_tot_mo.index.strftime('%Y %b')

#Quarterly
df_3rd_qtr = df[df['Type of Transaction']=='3rd Party'].resample('Q', on='YrMo').sum()
df_bsp_qtr = df[df['Type of Transaction']=='BSP'].resample('Q', on='YrMo').sum()
df_tot_qtr = df.resample('Q', on='YrMo').sum()

df_3rd_qtr['Period'] = df_3rd_qtr.index.strftime('%Y %b')
df_bsp_qtr['Period'] = df_bsp_qtr.index.strftime('%Y %b')
df_tot_qtr['Period'] = df_tot_qtr.index.strftime('%Y %b')

# %% Dashboard

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Dash Codes
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.title = 'Payment System Dash'
app.layout = html.Div(children=[
    html.H1('Payment System'),
    
    html.Div([
        html.H5('Time Periods:'),
        dcc.RadioItems(
            id='radio',
            options=[
                {'label':'Yearly', 'value':'yr'},
                {'label':'Monthly', 'value':'mo'},
                {'label':'Quarterly', 'value':'qtr'}
            ], labelStyle={'display': 'inline-block'}, value='yr'),
        ]),
    
    html.Div([
        html.Div([dcc.Graph(id = '3rd-party-amt')], className='four columns'),
        html.Div([dcc.Graph(id = '3rd-party-vol')], className='four columns'),
        html.Div([dcc.Graph(id = '3rd-party-pie')], className='four columns')
    ], className='row'),
    
    html.Div([
        html.Div([dcc.Graph(id = 'bsp-amt')], className='four columns'),
        html.Div([dcc.Graph(id = 'bsp-vol')], className='four columns'),
        html.Div([dcc.Graph(id = 'bsp-pie')], className='four columns')
    ], className='row'),
    
    html.Div([
        html.Div([dcc.Graph(id = 'tot-amt')], className='four columns'),
        html.Div([dcc.Graph(id = 'tot-vol')], className='four columns'),
        html.Div([dcc.Graph(id = 'tot-pie')], className='four columns')
    ], className='row')
])


@app.callback(
    dash.dependencies.Output('3rd-party-amt', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph1(value):
    if value == 'yr':
        dff = df_3rd_yr
    elif value == 'mo':
        dff = df_3rd_mo
    elif value == 'qtr':
        dff = df_3rd_qtr
    figure = {
        'data': [
            go.Bar(x=dff['Period'], y=dff['Amount'], name='3rd Party by Amount')
        ],
        'layout': go.Layout(
            title = '3rd Party by Amount',
        )
    }
    return figure

@app.callback(
    dash.dependencies.Output('3rd-party-vol', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph2(value):
    if value == 'yr':
        dff = df_3rd_yr
    elif value == 'mo':
        dff = df_3rd_mo
    elif value == 'qtr':
        dff = df_3rd_qtr
    figure = {
        'data': [
            go.Bar(x=dff['Period'], y=dff['Volume'], name='3rd Party by Volume')
        ],
        'layout': go.Layout(
            title = '3rd Party by Volume',
        )
    }
    return figure

@app.callback(
    dash.dependencies.Output('3rd-party-pie', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph3(value):
    if value == 'yr':
        dff = df_3rd_yr
    elif value == 'mo':
        dff = df_3rd_mo
    elif value == 'qtr':
        dff = df_3rd_qtr
    figure = {
        'data': [
            go.Pie(values=dff['Volume'],labels=dff['Period'], name='3rd Party by Volume'),
        ],
        'layout': go.Layout(
            title = '3rd Party by Volume',
        )
    }
    return figure

@app.callback(
    dash.dependencies.Output('bsp-amt', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph4(value):
    if value == 'yr':
        dff = df_bsp_yr
    elif value == 'mo':
        dff = df_bsp_mo
    elif value == 'qtr':
        dff = df_bsp_qtr
    figure = {
        'data': [
            go.Bar(x=dff['Period'], y=dff['Amount'], name='BSP by Amount')
        ],
        'layout': go.Layout(
            title = 'BSP by Amount',
        )
    }
    return figure

@app.callback(
    dash.dependencies.Output('bsp-vol', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph5(value):
    if value == 'yr':
        dff = df_bsp_yr
    elif value == 'mo':
        dff = df_bsp_mo
    elif value == 'qtr':
        dff = df_bsp_qtr
    figure = {
        'data': [
            go.Bar(x=dff['Period'], y=dff['Volume'], name='BSP by Volume')
        ],
        'layout': go.Layout(
            title = 'BSP by Volume',
        )
    }
    return figure

@app.callback(
    dash.dependencies.Output('bsp-pie', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph6(value):
    if value == 'yr':
        dff = df_bsp_yr
    elif value == 'mo':
        dff = df_bsp_mo
    elif value == 'qtr':
        dff = df_bsp_qtr
    figure = {
        'data': [
            go.Pie(values=dff['Volume'],labels=dff['Period'], name='BSP by Volume'),
        ],
        'layout': go.Layout(
            title = 'BSP by Volume',
        )
    }
    return figure

@app.callback(
    dash.dependencies.Output('tot-amt', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph7(value):
    if value == 'yr':
        dff = df_tot_yr
    elif value == 'mo':
        dff = df_tot_mo
    elif value == 'qtr':
        dff = df_tot_qtr
    figure = {
        'data': [
            go.Bar(x=dff['Period'], y=dff['Amount'], name='Total by Amount')
        ],
        'layout': go.Layout(
            title = 'Total by Amount',
        )
    }
    return figure

@app.callback(
    dash.dependencies.Output('tot-vol', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph8(value):
    if value == 'yr':
        dff = df_tot_yr
    elif value == 'mo':
        dff = df_tot_mo
    elif value == 'qtr':
        dff = df_tot_qtr
    figure = {
        'data': [
            go.Bar(x=dff['Period'], y=dff['Volume'], name='Total by Volume')
        ],
        'layout': go.Layout(
            title = 'Total by Volume',
        )
    }
    return figure

@app.callback(
    dash.dependencies.Output('tot-pie', 'figure'),
    [dash.dependencies.Input('radio', 'value')])
def show_graph9(value):
    if value == 'yr':
        dff = df_tot_yr
    elif value == 'mo':
        dff = df_tot_mo
    elif value == 'qtr':
        dff = df_tot_qtr
    figure = {
        'data': [
            go.Pie(values=dff['Volume'],labels=dff['Period'], name='Total by Volume'),
        ],
        'layout': go.Layout(
            title = 'Total by Volume',
        )
    }
    return figure



if __name__ == '__main__':
    app.run_server(debug=False)
