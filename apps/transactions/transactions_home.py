import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dcc
from app import app
from apps import dbconnect as db

external_stylesheets = ['otherpages.css']

layout = html.Div([
        html.Div(
            className='home-bg',
            children=[
                dbc.Row([
                    dbc.Col(html.H2('Contracts Database', className='head-title')),  
                    dbc.Col(dbc.Button(
                        'Add Contracts',
                        className='head-add-btn',
                        color="secondary",
                        href='/transactions/transactions_profile?mode=add'
                    )),
                ]),
                html.Hr()
            ]),
        dbc.Card([
                dbc.CardBody([
                        html.Div([
                                dbc.CardHeader([
                                    html.H4('Filter Contract Records', className='find-title'),
                                ], style={'background-color': '#ffffff'}
                                ),
                                html.Div(
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("Search Contract Detail", width=3, style={'margin-right': '-100px'}),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            type='text',
                                                            id="transactions_filter_transactionsid", 
                                                            placeholder="Enter filter"
                                                        ),
                                                        width=5
                                                    )],
                                                style={'margin-top': '20px'},
                                                className='mb-3'
                                            ),
                                            dbc.Row([
                                                    dbc.Label("Start Date", width=2),
                                                    dbc.Col(
                                                        dcc.DatePickerSingle(
                                                            id='start_date_picker',
                                                            display_format='MM-DD-YYYY',
                                                            placeholder='MM-DD-YYYY',
                                                        ),
                                                        width=2,),
                                                    dbc.Label("End Date", width=2),
                                                    dbc.Col(
                                                        dcc.DatePickerSingle(
                                                            id='end_date_picker',
                                                            display_format='MM-DD-YYYY',
                                                            placeholder='MM-DD-YYYY',
                                                        ),
                                                        width=2,
                                                    ),],
                                                className="mb-3",
                                            ),
                                        ]
                                    )
                                ),
                                html.Div(
                                    "No records to show",
                                    id='transactions_transactionsrecords'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('transactions_transactionsrecords', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('transactions_filter_transactionsid', 'value'),
        Input('start_date_picker', 'date'),
        Input('end_date_picker', 'date'),
        State('currentrole', 'data'),  
    ]
)
def transactionshome_loadtransactionslist(pathname, searchterm, start_date, end_date, userrole):
    if pathname == '/transactions':
        
        sql = """ SELECT ac_id, ac_ups_title, ac_ups_type, to_char(CAST(ac_tin AS DATE), 'MM-DD-YYYY'), ac_ups_ipname, ac_ups_desc, ac_percent
            FROM contracts c
            WHERE NOT ac_delete
        """
        values = [] 
        cols = ['Contract ID', 'Title', 'Type', 'Date Start', 'IP Name', 'Description', 'Progress', '']
        
        if searchterm:
            sql += """ AND (
                        LOWER(CAST(ac_id AS TEXT)) ILIKE LOWER(%s) OR
                        LOWER(ac_ups_title) ILIKE LOWER(%s) OR
                        LOWER(ac_ups_type) ILIKE LOWER(%s) OR
                        LOWER(ac_ups_ipname) ILIKE LOWER(%s) OR
                        LOWER(CAST(ac_ups_desc AS TEXT)) ILIKE LOWER(%s) OR
                        LOWER(ac_percent) ILIKE LOWER(%s)
                    )"""
                    
            values += ['%' + searchterm + '%'] * 6
        
       
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: 
            buttons = []
            for tr_id in df['Contract ID']:
                disabled = True if userrole == 'Secretary' else False
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'transactions/transactions_profile?mode=edit&id={tr_id}',
                                   size='sm', color='warning', disabled=disabled), 
                        style={'text-align': 'center'}
                    )
                ]
            
            df['Action'] = buttons
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        else:
            return ["No records to show"]
        
    else:
        raise PreventUpdate