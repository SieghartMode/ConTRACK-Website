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
                dbc.Col(html.H2('User Management', className='head-title')), 
                dbc.Col(dbc.Button(
                    'Add User',
                    className='head-add-btn',
                    color="secondary",
                        href='/users/users_profile?mode=add'
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
                                    html.H4('Find User', className='find-title'),
                                    ], 
                                    style={'background-color': '#ffffff'}
                                
                                ),

                                
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search User Name", width=3, style={'margin-right':'-100px'}),
                                                html.Br(),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='userhome_namefilter',
                                                        placeholder='User Name'
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
                                    "Table with users will go here.",
                                    id='userhome_userlist'
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
        Output('userhome_userlist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('userhome_namefilter', 'value'), 
    ]
    
)
def userhome_loaduserlist(pathname, searchterm):
    print("Callback triggered with pathname:", pathname)
    print("Search term:", searchterm)
    if pathname == '/users':
       
        sql = """ SELECT user_id, user_fname, user_lname, user_email, user_cname, user_access, user_pwd
            FROM users u
            WHERE
                NOT user_delete 
        """
        values = []
        cols = ["ID", "Fullname", "Lastname", "Email", "Cname", "Access", "pwd"]
        if searchterm:
            sql += """ AND (
                        LOWER(user_fname) ILIKE LOWER(%s) OR
                        LOWER(user_lname) ILIKE LOWER(%s) OR
                        LOWER(user_email) ILIKE LOWER(%s) OR
                        LOWER(user_cname) ILIKE LOWER(%s) OR
                        LOWER(user_access) ILIKE LOWER(%s)
                    )"""
                        
            values += ['%' + searchterm + '%'] * 5
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: 
            
            buttons = []
            for user_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                    href=f'/users/users_profile?mode=edit&id={user_id}',
                                    size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
      
            df['Action'] = buttons
        
            df = df[["Fullname", "Lastname", "Email", "Cname", "Access", "Action"]]
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate
