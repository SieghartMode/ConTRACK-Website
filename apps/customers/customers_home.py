import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd


from app import app
from apps import dbconnect as db

from dash.dependencies import Input, Output, State
from apps import dbconnect as db

external_stylesheets = ['otherpages.css']

layout = html.Div(
    [
        html.Div(
            className='home-bg',
            children = [
            
            
            dbc.Row([
                dbc.Col(html.H2('Customer Management', className='head-title')),  # Page Header
                dbc.Col(dbc.Button(
                    'Add Customer',
                    className='head-add-btn',
                    href='/customers/customers_profile?mode=add'
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
                                    html.H4('Find Customer', className='find-title'),
                                    ], 
                                    style={'background-color': '#ffffff'}
                                
                                ),

                                
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Customer Name", width=3, style={'margin-right':'-100px'}),
                                                html.Br(),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='customerhome_namefilter',
                                                        placeholder='Customer Name'
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
                                    "Table with customers will go here.",
                                    id='customerhome_customerlist'
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
        Output('customerhome_customerlist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('customerhome_namefilter', 'value'),  
        State('currentrole', 'data'),  
    ]
)
def customerhome_loadcustomerlist(pathname, searchterm, current_role):
    print("Callback triggered with pathname:", pathname)
    print("Search term:", searchterm)
    if pathname == '/customers':
        sql = """ SELECT cust_id, cust_name, cust_addr, cust_status, cust_terms, cust_con, cust_remarks
            FROM customer c
            WHERE
                NOT cust_delete 
        """
        values = []
        cols = ["ID", "Name", "Address", "Status", "Terms", "Contact", "Remarks"]
        if searchterm:
            sql += """ AND (
                        LOWER(cust_name) ILIKE LOWER(%s) OR
                        LOWER(cust_addr) ILIKE LOWER(%s) OR
                        LOWER(cust_status) ILIKE LOWER(%s) OR
                        LOWER(cust_terms) ILIKE LOWER(%s) OR
                        LOWER(cust_con) ILIKE LOWER(%s) OR
                        LOWER(cust_remarks) ILIKE LOWER(%s)
                    )"""
                        
            values += ['%' + searchterm + '%'] * 6
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: 
            
            buttons = []
            for cust_id in df['ID']:
                disabled = True if current_role == 'Secretary' else False
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                    href=f'/customers/customers_profile?mode=edit&id={cust_id}',
                                    size='sm', color='warning', disabled=disabled), 
                        style={'text-align': 'center'}
                    )
                ]
      
            df['Action'] = buttons
            df = df[["Name", "Address", "Status", "Terms", "Contact", "Remarks", "Action"]]
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate