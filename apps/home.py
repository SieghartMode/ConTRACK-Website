import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.exceptions import PreventUpdate
import dash_table
import plotly.express as px  
import locale

locale.setlocale(locale.LC_ALL, 'en_PH.UTF-8')

from app import app
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import webbrowser
from app import app
import apps.dbconnect as db
from apps import commonmodules as cm
from apps import home

from apps.commonmodules import navbar  
from apps import login
from apps.login import loginprocess

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
#for DB needs
from apps import dbconnect as db

CONTENT_STYLE = {
    "margin-top": "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        navbar, 
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

layout = html.Div([
    # FIRST ROWWWWWW
    dbc.Row([
        # Left Column
        dbc.Col([
            html.Div(id='pending-ip-meet'),
        ], width=2),
        dbc.Col([
            html.Div(id='check-loi'),
        ], width=2),
        dbc.Col([
            html.Div(id='ip-revision'),
        ], width=2),
        dbc.Col([
            html.Div(id='upscale-finalize'),
        ], width=2),
        dbc.Col([
            html.Div(id='ovpla-approval'),
        ], width=2),
        dbc.Col([
            html.Div(id='ovpla-signing'),
        ], width=2),
    ], style={'margin-bottom': '40px'}),  
    html.Div(
            className='home-bg',
            children=[
                dbc.Row([
                    dbc.Col(html.H2('Pending Contract Actions', className='head-title')), 
                    dbc.Col(dbc.Button(
                        'Add Contract',
                        className='head-add-btn',
                        color="secondary",
                        href='/contracts/contracts_profile?mode=add'
                    )),
                ]),
                html.Hr()
            ]
        ),

        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.CardHeader([
                                    html.H4('Find Contracts', className='find-title'),
                                ], 
                                style={'background-color': '#ffffff'}
                                ),

                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Contract Name", width=3, style={'margin-right':'-100px'}),
                                                html.Br(),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractshome_namefilter1',
                                                        placeholder='Contract Name'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                            style={'margin-top': '20px'},
                                            className='mb-3'
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with contracts will go here.",
                                    id='contractshome_contractslist1'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
], className='full-width'),

@app.callback(
    [
        Output('contractshome_contractslist1', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('contractshome_namefilter1', 'value'),
    ]
)
def contractshome_loadcontractslist(pathname, searchterm):
    print("Callback triggered with pathname:", pathname)
    print("Search term:", searchterm)
    if pathname == '/home':

        sql = """ SELECT ac_id, ac_ups_title, ac_ups_type, ac_ups_desc, ac_ups_ipname, ac_percent
            FROM contracts c
            WHERE
                NOT ac_delete 
        """
        values = []
        cols = ["ID", "Title", "Type", "Description", "IP Name", "Progress"]
        if searchterm:
            sql += """ AND (
                        LOWER(ac_ups_title) ILIKE LOWER(%s) OR
                        LOWER(ac_ups_type) ILIKE LOWER(%s) OR
                        LOWER(ac_ups_desc) ILIKE LOWER(%s) OR
                        LOWER(ac_ups_ipname) ILIKE LOWER(%s) OR
                        LOWER(ac_percent) ILIKE LOWER(%s)
                    )"""

            values += ['%' + searchterm + '%'] * 5
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:

            buttons = []
            for contracts_id in df['ID']:
                print(contracts_id)
                buttons += [
                    html.Div(
                        dbc.Button('Details',
                                   href=f'/contracts/contracts_profile?mode=edit&id={contracts_id}',
                                   size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]

            df['Action'] = buttons

            # Create progress bars for the Progress column
            progress_bars = []
            for percent in df['Progress']:
                percent_float = float(percent)  # Convert to float
                progress_bars.append(
                    dbc.Progress(value=percent_float, max=1, style={'height': '20px', 'color': '#000000'}, className="mb-3", label=f"{percent_float*100:.0f}%")
                )

            df['Progress'] = progress_bars

            df = df[["ID", "Title", "Type", "Description", "IP Name", "Progress", "Action"]]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm', style={'text-align': 'left'})
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('pending-ip-meet', 'children'),
        Output('check-loi', 'children'),
        Output('ip-revision', 'children'),
        Output('upscale-finalize', 'children'),
        Output('ovpla-approval', 'children'),
        Output('ovpla-signing', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ]
)
def update_counts(pathname):
    if pathname == '/home':
        # Define the ranges and their corresponding labels
        ranges = [
            ('Pending IP Meet', 0, 0.17),
            ('Check LOI', 0.17, 0.24),
            ('IP Revision', 0.24, 0.86),
            ('UPSCALE Finalize', 0.86, 0.9),
            ('OVPLA Approval', 0.9, 0.95),
            ('OVPLA Signing', 0.95, 1.0)
        ]
        
        children = []
        
        for label, min_percent, max_percent in ranges:
            sql = """ 
                SELECT COUNT(*) FROM contracts 
                WHERE CAST(ac_percent AS FLOAT) > %s 
                AND CAST(ac_percent AS FLOAT) <= %s 
                AND NOT ac_delete 
            """
            values = [min_percent, max_percent]
            df = db.querydatafromdatabase(sql, values, ["count"])
            count = df['count'][0] if df.shape[0] > 0 else 0
            children.append(html.Div([
                dbc.Label(label),
                html.H4(count),
            ], className='add-container'))

        return children
    else:
        raise PreventUpdate