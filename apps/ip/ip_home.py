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

from dash.dependencies import Input, Output, State
from apps import dbconnect as db

layout = html.Div(
    [
        html.Div(
            className='home-bg',
            children = [
            
            
            dbc.Row([
                dbc.Col(html.H2('IP Management', className='head-title')), 
                dbc.Col(dbc.Button(
                    'Add IP',
                    className='head-add-btn',
                    color="secondary",
                        href='/ip/ip_profile?mode=add'
                )),
            ]),
            html.Hr()
        ]),

        dbc.Card( 
            [
                dbc.CardBody( 
                    [
                        html.Div( 
                            [
                                 dbc.CardHeader([
                                    html.H4('Find IP', className='find-title'),
                                    ], 
                                    style={'background-color': '#ffffff'}
                                
                                ),

                                
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search IP Name", width=3, style={'margin-right':'-100px'}),
                                                html.Br(),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='iphome_namefilter',
                                                        placeholder='IP Name'
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
                                    "Table with Industry Partners will go here.",
                                    id='iphome_iplist'
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
        Output('iphome_iplist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('iphome_namefilter', 'value'), 
    ]
    
)
def iphome_loadiplist(pathname, searchterm):
    print("Callback triggered with pathname:", pathname)
    print("Search term:", searchterm)
    if pathname == '/ip':
       
        sql = """ SELECT ip_id, ip_name, ip_ind, ip_person, ip_phone, ip_email, ip_remarks
            FROM indpartners i
            WHERE
                NOT ip_delete 
        """
        values = []
        cols = ["ID", "Name", "Industry", "Contact", "Number", "Email", "Remarks"]
        if searchterm:
            sql += """ AND (
                        LOWER(ip_name) ILIKE LOWER(%s) OR
                        LOWER(ip_ind) ILIKE LOWER(%s) OR
                        LOWER(ip_person) ILIKE LOWER(%s) OR
                        LOWER(ip_phone) ILIKE LOWER(%s) OR
                        LOWER(ip_email) ILIKE LOWER(%s) OR
                        LOWER(ip_remarks) ILIKE LOWER(%s)
                    )"""
                        
            values += ['%' + searchterm + '%'] * 6
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: 
            
            buttons = []
            for ip_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                    href=f'/ip/ip_profile?mode=edit&id={ip_id}',
                                    size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
      
            df['Action'] = buttons
        
            df = df[["ID", "Name", "Industry", "Contact", "Number", "Email", "Remarks", "Action"]]
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate
