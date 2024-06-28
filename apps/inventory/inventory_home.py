import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dcc
from app import app
from apps import dbconnect as db

external_stylesheets = ['otherpages.css']

layout = html.Div(
    [
        html.Div(
            className='home-bg',
            children=[
                dbc.Row([
                    dbc.Col(html.H2('Inventory Management', className='head-title')),  # Page Header
                    dbc.Col(dbc.Button(
                        'Add Entry',
                        className='head-add-btn',
                        color="secondary",
                        href='/inventory/inventory_profile?mode=add'
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
                                    html.H4('Filter Inventory Records', className='find-title'),
                                ],
                                    style={'background-color': '#ffffff'}
                                ),

                                html.Div(
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("Search Entry", width=3, style={'margin-right': '-100px'}),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            type='text',
                                                            id="inventory_filter_inventoryid",
                                                            placeholder="Enter filter"
                                                        ),
                                                        width=5
                                                    )
                                                ],
                                                style={'margin-top': '20px'},
                                                className='mb-3'
                                            ),

                                            dbc.Row(
                                                [
                                                    dbc.Label("Start Date", width=2),
                                                    dbc.Col(
                                                        dcc.DatePickerSingle(
                                                            id='start_date_picker',
                                                            display_format='MM-DD-YYYY',
                                                            placeholder='MM-DD-YYYY',
                                                        ),
                                                        width=2,
                                                    ),
                                                    dbc.Label("End Date", width=2),
                                                    dbc.Col(
                                                        dcc.DatePickerSingle(
                                                            id='end_date_picker',
                                                            display_format='MM-DD-YYYY',
                                                            placeholder='MM-DD-YYYY',
                                                        ),
                                                        width=2,
                                                    ),
                                                ],
                                                className="mb-3",
                                            ),
                                        ]
                                    )
                                ),
                                html.Div(
                                    "No inventory records to show",
                                    id='inventory_inventoryrecords'
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
        Output('inventory_inventoryrecords', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('inventory_filter_inventoryid', 'value'),
        Input('start_date_picker', 'date'),
        Input('end_date_picker', 'date'),
        State('currentrole', 'data'),  
    ]
)
def inventoryhome_loadinventorylist(pathname, searchterm, start_date, end_date, userrole):
    if pathname == '/inventory':
        
        sql = """ SELECT i.inv_id, i.inv_docno, i.inv_type, to_char(CAST(i.inv_date AS DATE), 'MM-DD-YYYY'), c.cust_name, i.inv_status, 
                to_char(CAST(i.inv_lastupd AS DATE), 'MM-DD-YYYY'), i.inv_remarks
            FROM inventory i INNER JOIN customer c ON c.cust_id = i.cust_id
            WHERE NOT i.inv_delete
        """
        values = [] 
        cols = ['Transaction ID', 'Doc #', 'Doc Type', 'Date Created', 'Customer', 'Status', 'Last Updated', 'Remarks']
        
        if searchterm:
            sql += """ AND (
                        LOWER(CAST(i.inv_id AS TEXT)) ILIKE LOWER(%s) OR
                        LOWER(i.inv_docno) ILIKE LOWER(%s) OR
                        LOWER(i.inv_type) ILIKE LOWER(%s) OR
                        LOWER(c.cust_name) ILIKE LOWER(%s) OR
                        LOWER(i.inv_status) ILIKE LOWER(%s) OR
                        LOWER(i.inv_remarks) ILIKE LOWER(%s)
                    )"""
                    
            values += ['%' + searchterm + '%'] * 6
        
        if start_date and end_date:
            sql += " AND inv_date >= %s AND inv_date <= %s"
            values += [start_date, end_date]

        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: 
            buttons = []
            for inv_id in df['Transaction ID']:
                disabled = True if userrole == 'Secretary' else False
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'inventory/inventory_profile?mode=edit&id={inv_id}',
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