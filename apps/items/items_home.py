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

external_stylesheets = ['otherpages.css']

layout = html.Div(
    [
        html.Div(
            className='home-bg',
            children = [
            
            
            dbc.Row([
                dbc.Col(html.H2('Item Management', className='head-title')),  # Page Header
                dbc.Col(dbc.Button(
                                    'Add Item',
                                    color="secondary",
                                    href='/items/items_profile?mode=add',
                                    className='head-add-btn'
                                ),),
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
                                    html.H4('Filter Items', className='find-title'),
                                    ], 
                                    style={'background-color': '#ffffff'}
                                
                                ),

                                
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Item Name", width=3, style={'margin-right':'-100px'}),
                                                html.Br(),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='itemhome_namefilter',
                                                        placeholder='Item Name'
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
                                    "Table with items will go here.",
                                    id='itemhome_itemlist'
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
        Output('itemhome_itemlist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('itemhome_namefilter', 'value'),
        State('currentrole', 'data'),  
    ]
)
def itemhome_loaditemlist(pathname, searchterm, current_role):
    print("Callback triggered with pathname:", pathname)
    print("Search term:", searchterm)
    print("Current Role:", current_role)
    
    if pathname == '/items':
        sql = """ SELECT it_id, it_name, it_mm, it_srp, it_cost, it_stklvl
            FROM item i
            WHERE
                NOT it_delete 
        """
        values = []
        cols = ["ID", "Name", "MMSize", "SRP", "Cost", "Stock Level"]
        if searchterm:
            sql += """ AND (
                        LOWER(it_name) ILIKE LOWER(%s) OR
                        LOWER(it_mm) ILIKE LOWER(%s) OR
                        LOWER(CAST(it_srp AS TEXT)) ILIKE LOWER(%s) OR
                        LOWER(CAST(it_cost AS TEXT)) ILIKE LOWER(%s) OR
                        LOWER(CAST(it_stklvl AS TEXT)) ILIKE LOWER(%s)
                    )"""
                        
            values += ['%' + searchterm + '%'] * 5
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape: 
                        
            buttons = []
            for it_id in df['ID']:
                disabled = True if current_role == 'Secretary' else False
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                    href=f'/items/items_profile?mode=edit&id={it_id}',
                                    size='sm', color='warning', disabled=disabled),  
                        style={'text-align': 'center'}
                    )
                ]
                
            df['Action'] = buttons
        
            df = df[['Name', "MMSize", "SRP", "Cost", "Stock Level", "Action"]]
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate