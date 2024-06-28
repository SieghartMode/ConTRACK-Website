from dash import dcc
from dash import html 
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import webbrowser

from app import app
#for DB needs
from apps import dbconnect as db

from urllib.parse import urlparse, parse_qs
layout = html.Div(
    className='profile-bg',

    children= [
        html.Div( 
            [
                dcc.Store(id='itemprofile_toload', storage_type='memory', data=0),
            ]
        ),

        html.H2('Item Details', className = 'page-header'), 
        html.Hr(),
dbc.Alert(id='itemprofile_alert', is_open=False), # For feedback purposes
        
        
#####INPUT BOXES #######        
html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Left Column
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Item Name", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text', 
                                                id='itemprofile_name',
                                                placeholder="Item Name"
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("MM Size", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text', 
                                                id='itemprofile_mm',
                                                placeholder='Item Millimeter Size'
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("SRP", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text', 
                                                id='itemprofile_srp',
                                                placeholder='Item SRP'
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                            ]
                        ),
                    ],
                    width=6
                ),
                
                dbc.Col(
                    [
                        # Right Column
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Cost", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text', 
                                                id='itemprofile_cost',
                                                placeholder='Item Cost'
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Stock Level", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text',
                                                id='itemprofile_stklvl',
                                                placeholder='Item Stock Level'
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                            ]
                        ),
                    ],
                    width=6
                ),
            ]
        )
    ]
),        

        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='itemprofile_removerecord',
                            options=[
                                {
                                'label': "Mark for Deletion",
                                'value': 1
                                }
                            ],
                            style={'fontWeight':'bold'},
                        ),
                        width=5,
                    ),
                ],
                className="mb-3",
            ),
            id='itemprofile_removerecord_div'
        ),
        dbc.Button(
            'Cancel',
            id='itemprofile_cancel',
            className='cancel-btn',
            href='/items'  
        ),
        dbc.Button(
            'Submit',
            id='itemprofile_submit',
            className = 'submit-btn',
            n_clicks=0 
        ),
        dbc.Modal( 
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    [
                        'Message here! Edit me please!'
                    ], id = 'itemprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/items/items_home', 
                        id = 'itemprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='itemprofile_successmodal',
            backdrop='static' 
        )
    ]
)
@app.callback(
    [
        Output('itemprofile_toload', 'data'),
        Output('itemprofile_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') 
    ]

)
def itemprof_loaddropdown(pathname, search):
    if pathname == '/items/items_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [to_load, removediv_style]

@app.callback(
    [
        Output('itemprofile_alert', 'color'),
        Output('itemprofile_alert', 'children'),
        Output('itemprofile_alert', 'is_open'),
        Output('itemprofile_successmodal', 'is_open'),
        Output('itemprofile_feedback_message', 'children'),
        Output('itemprofile_btn_modal', 'href'),
    ],
    [
        Input('itemprofile_submit', 'n_clicks'),
        Input('itemprofile_btn_modal', 'n_clicks'),
    ],
    [
       
        State('itemprofile_name', 'value'),
        State('itemprofile_mm', 'value'),
        State('itemprofile_srp', 'value'),
        State('itemprofile_cost', 'value'),
        State('itemprofile_stklvl', 'value'),
        State('url', 'search'),
        State('itemprofile_removerecord', 'value'),
    ]
)
def movieprofile_saveprofile(submitbtn,closebtn, name, mm, srp, cost, stklvl, search,
                            removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        print(eventid)
        if eventid == 'itemprofile_submit' and submitbtn:
            
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            if not name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the item name.'
            elif not mm:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the item mm size.'
            elif not srp:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the item srp.'
            elif not cost:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the item cost.'
            elif not stklvl:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the item stock level.'
            else: 
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                print('here')
                if create_mode == 'add':
                    sql = '''
                        INSERT INTO item (it_name, it_mm, it_srp, it_cost, it_stklvl)
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                    values = [name, mm, srp, cost, stklvl]
                    db.modifydatabase(sql, values)
                    feedbackmessage = "Item has been saved."
                    okay_href = '/items'
                    modal_open = True
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    it_id = parse_qs(parsed.query)['id'][0]
                    print("ID of item: ", it_id)
                    sqlcode = """UPDATE item
                    SET
                        it_name = %s,
                        it_mm = %s,
                        it_srp = %s,
                        it_cost = %s,
                        it_stklvl = %s,
                        it_delete = %s
                    WHERE
                        it_id = %s
                    """
                    to_delete = bool(removerecord)
                    values = [name, mm, srp, cost, stklvl, to_delete, it_id]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "Item has been updated."
                    okay_href = '/items'
                    modal_open = True
                else:
                    raise PreventUpdate
            return [alert_color, alert_text, alert_open, modal_open,
                    feedbackmessage, okay_href]
        else: 
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('itemprofile_name', 'value'),
        Output('itemprofile_mm', 'value'),
        Output('itemprofile_srp', 'value'),
        Output('itemprofile_cost', 'value'),
        Output('itemprofile_stklvl', 'value'),
    ],
    [
       
        Input('itemprofile_toload', 'modified_timestamp')
    ],
    [
       
        State('itemprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def itemprofile_loadprofile(timestamp, toload, search):
    print(f'toload: {toload}')
    if toload: 
        
        parsed = urlparse(search)
        it_id = parse_qs(parsed.query)['id'][0]
        print("ID of item: ", it_id)
        sql = """
            SELECT it_name, it_mm, it_srp, it_cost, it_stklvl
            FROM item
            WHERE it_id = %s
        """
        values = [it_id]
        col = ['name', 'mm', 'srp', 'cost', 'stklvl']
        df = db.querydatafromdatabase(sql, values, col)

        name = df['name'][0]
        mm = df['mm'][0]
        srp = df['srp'][0]
        cost = df['cost'][0]
        stklvl = df['stklvl'][0]

        
        return [name, mm, srp, cost, stklvl]
    else:
        raise PreventUpdate