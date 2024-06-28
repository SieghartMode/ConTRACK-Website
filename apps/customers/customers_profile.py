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
from apps import dbconnect as db

from urllib.parse import urlparse, parse_qs

external_stylesheets = ['otherpages.css']

layout = html.Div(
    className='profile-bg',

    children = [
        html.Div( 
            [
                dcc.Store(id='customerprofile_toload', storage_type='memory', data=0),
            ]
        ),

        html.H2('Customer Details', className = 'page-header'), 
        html.Hr(),
dbc.Alert(id='customerprofile_alert', is_open=False),
        
#####INPUT BOXES #######       
html.Div(
    dbc.Row(
        [
            dbc.Col(
                dbc.Form(
                    [
                        ########### FIRST COL ###############
                        dbc.Row(
                            [
                                dbc.Label("Customer Name", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type='text', 
                                        id='customerprofile_name',
                                        placeholder="Customer Name"
                                    ),
                                    width=6
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Address", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type='text', 
                                        id='customerprofile_addr',
                                        placeholder='Customer Address'
                                    ),
                                    width=6
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Status", width=2),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='customerprofile_status',
                                        placeholder='Select Status',
                                        options=[
                                            {'label': 'Active', 'value': 'Active'},
                                            {'label': 'Inactive', 'value': 'Inactive'},
                                            # Add more options as needed
                                        ], style={'margin-left': '50px'},
                                    ),
                                    width=5
                                )
                            ],
                            className='mb-3'
                        ),
                    ],
                ),
                width=6
            ),

            dbc.Col(
                dbc.Form(
                    [
                        ########### SECOND COL ###############
                        dbc.Row(
                            [
                                dbc.Label("Terms", width=2),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='customerprofile_terms',
                                        placeholder='Select Terms',
                                        options=[
                                            {'label': 'COD', 'value': 'COD'},
                                            {'label': 'PDC', 'value': 'PDC'},
                                            {'label': 'PDC 30', 'value': 'PDC 30'},
                                            {'label': 'PDC 60', 'value': 'PDC 60'},
                                            {'label': 'PDC 90', 'value': 'PDC 90'},
                                            {'label': 'PDC 120', 'value': 'PDC 120'},
                                        ]
                                    ), style={'margin-left': '95px'},
                                    width=5
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Contact #", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type='text',
                                        id='customerprofile_con',
                                        placeholder='Customer Contact Number'
                                    ),
                                    width=6
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Remarks", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type='text',
                                        id='customerprofile_remarks',
                                        placeholder='Customer Remarks'
                                    ),
                                    width=6
                                )
                            ],
                            className='mb-3'
                        ),
                    ],
                ),
                width=6
            )
        ]
    ),
    
),

        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='customerprofile_removerecord',
                            options=[
                                {
                                'label': "Mark for Deletion",
                                'value': 1
                                }
                            ],
                            # I want the label to be bold
                            style={'fontWeight':'bold'},
                        ),
                        width=5,
                    ),
                ],
                className="mb-3",
            ),
            id='customerprofile_removerecord_div'
        ),
        dbc.Button(
            'Cancel',
            id='itemprofile_cancel',
            className='cancel-btn',
            href='/customers'  
        ),
        dbc.Button(
            'Submit',
            id='customerprofile_submit',
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
                    ], id = 'customerprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/customers/customers_home', 
                        id = 'customerprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='customerprofile_successmodal',
            backdrop='static' 
        )
    ]
)
@app.callback(
    [
        Output('customerprofile_toload', 'data'),
        Output('customerprofile_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') 
    ]

)
def customerprof_loaddropdown(pathname, search):
    if pathname == '/customers/customers_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [to_load, removediv_style]

@app.callback(
    [
        Output('customerprofile_alert', 'color'),
        Output('customerprofile_alert', 'children'),
        Output('customerprofile_alert', 'is_open'),
        Output('customerprofile_successmodal', 'is_open'),
        Output('customerprofile_feedback_message', 'children'),
        Output('customerprofile_btn_modal', 'href'),
    ],
    [
        Input('customerprofile_submit', 'n_clicks'),
        Input('customerprofile_btn_modal', 'n_clicks'),
    ],
    [
       
        State('customerprofile_name', 'value'),
        State('customerprofile_addr', 'value'),
        State('customerprofile_status', 'value'),
        State('customerprofile_terms', 'value'),
        State('customerprofile_con', 'value'),
        State('customerprofile_remarks', 'value'),
        State('url', 'search'), 
        State('customerprofile_removerecord', 'value'), #add this
    ]
)
def customerprofile_saveprofile(submitbtn,closebtn, name, addr, status, terms, con, remarks, search,
                            removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        print(eventid)
        if eventid == 'customerprofile_submit' and submitbtn:
            
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            if not name: 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the customer name.'
            elif not addr:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the customer address.'
            elif not status:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the customer status.'
            elif not terms:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the customer terms.'
            elif not con:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the customer contact number.'
            elif not remarks:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the customer remarks.'
            else: 
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                print('here')
                if create_mode == 'add':
                    sql = '''
                        INSERT INTO customer (cust_name, cust_addr, cust_status, cust_terms, cust_con, cust_remarks)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    '''
                    values = [name, addr, status, terms, con, remarks]
                    db.modifydatabase(sql, values)
                    feedbackmessage = "Customer has been saved."
                    okay_href = '/customers'
                    modal_open = True
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    cust_id = parse_qs(parsed.query)['id'][0]
                    print("ID of customers: ", cust_id)
                    sqlcode = """UPDATE customer
                    SET
                        cust_name = %s,
                        cust_addr = %s,
                        cust_status = %s,
                        cust_terms = %s,
                        cust_con = %s,
                        cust_remarks = %s,
                        cust_delete = %s
                    WHERE
                        cust_id = %s
                    """
                    to_delete = bool(removerecord)
                    values = [name, addr, status, terms, con, remarks, to_delete, cust_id]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "Customer has been updated."
                    okay_href = '/customers'
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
        Output('customerprofile_name', 'value'),
        Output('customerprofile_addr', 'value'),
        Output('customerprofile_status', 'value'),
        Output('customerprofile_terms', 'value'),
        Output('customerprofile_con', 'value'),
        Output('customerprofile_remarks', 'value'),
    ],
    [
        Input('customerprofile_toload', 'modified_timestamp')
    ],
    [
        State('customerprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def customersprofile_loadprofile(timestamp, toload, search):
    print(f'toload: {toload}')
    if toload: 
        parsed = urlparse(search)
        cust_id = parse_qs(parsed.query)['id'][0]
        print("ID of customers: ", cust_id)
        sql = """
            SELECT cust_name, cust_addr, cust_status, cust_terms, cust_con, cust_remarks
            FROM customer
            WHERE cust_id = %s
        """
        values = [cust_id]
        col = ['name', 'addr', 'status', 'terms', 'con', 'remarks']
        df = db.querydatafromdatabase(sql, values, col)

        name = df['name'][0]
        addr = df['addr'][0]
        status = df['status'][0]
        terms = df['terms'][0]
        con = df['con'][0]
        remarks = df['remarks'][0]
   
        return [name, addr, status, terms, con, remarks]
    else:
        raise PreventUpdate