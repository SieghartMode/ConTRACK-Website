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

layout = html.Div(
    [
        html.Div(
            className='home-bg',
            children=[
                dbc.Row([
                    dbc.Col(html.H2('Contracts Database', className='head-title')), 
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
                                                        id='contractshome_namefilter',
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
                                    id='contractshome_contractslist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
),

@app.callback(
    [
        Output('contractshome_contractslist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('contractshome_namefilter', 'value'),
    ]
)
def contractshome_loadcontractslist(pathname, searchterm):
    print("Callback triggered with pathname:", pathname)
    print("Search term:", searchterm)
    if pathname == '/contracts':

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
                progress_bars.append(
                    dbc.Progress(value=percent, max=1, style={'height': '20px'}, className="mb-3")
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
