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
    
    children=[
        html.Div(
            [
                dcc.Store(id='supplierprofile_toload', storage_type='memory', data=0),
            ]
        ),

        html.H2('Supplier Details', className = 'page-header'),
        html.Hr(),
dbc.Alert(id='supplierprofile_alert', is_open=False),
        
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
                                        dbc.Label("Supplier Name", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text', 
                                                id='supplierprofile_name',
                                                placeholder="Supplier Name"
                                            ),
                                            width=6
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Supplier Address", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text', 
                                                id='supplierprofile_addr',
                                                placeholder='Supplier Address'
                                            ),
                                            width=6
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Supplier Status", width=4),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='supplierprofile_status',
                                                placeholder='Select Status',
                                                options=[
                                                    {'label': 'Active', 'value': 'Active'},
                                                    {'label': 'Inactive', 'value': 'Inactive'},
                                                ]
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
                                        dbc.Label("Terms", width=2),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='supplierprofile_terms',
                                                placeholder='Select Terms',
                                                options=[
                                                    {'label': 'COD', 'value': 'COD'},
                                                    {'label': 'PDC', 'value': 'PDC'},
                                                    {'label': 'PDC 30', 'value': 'PDC 30'},
                                                    {'label': 'PDC 60', 'value': 'PDC 60'},
                                                    {'label': 'PDC 90', 'value': 'PDC 90'},
                                                    {'label': 'PDC 120', 'value': 'PDC 120'},
                                                ], style={'margin-left': '50px'}
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Supplier Contact #", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text',
                                                id='supplierprofile_con',
                                                placeholder='Supplier Contact #'
                                            ),
                                            width=6
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Supplier Remarks", width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text',
                                                id='supplierprofile_remarks',
                                                placeholder='Supplier Remarks'
                                            ),
                                            width=6
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
                            id='supplierprofile_removerecord',
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
            id='supplierprofile_removerecord_div'
        ),
        dbc.Button(
            'Cancel',
            id='itemprofile_cancel',
            className='cancel-btn',
            href='/suppliers' 
        ),
        dbc.Button(
            'Submit',
            id='supplierprofile_submit',
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
                    ], id = 'supplierprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/suppliers/suppliers_home',
                        id = 'supplierprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='supplierprofile_successmodal',
            backdrop='static'
        )
    ]
)
@app.callback(
    [
       
        Output('supplierprofile_toload', 'data'),
        Output('supplierprofile_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') 
    ]

)
def supplierprof_loaddropdown(pathname, search):
    if pathname == '/suppliers/suppliers_profile':
        
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [to_load, removediv_style]

@app.callback(
    [
        Output('supplierprofile_alert', 'color'),
        Output('supplierprofile_alert', 'children'),
        Output('supplierprofile_alert', 'is_open'),
        Output('supplierprofile_successmodal', 'is_open'),
        Output('supplierprofile_feedback_message', 'children'),
        Output('supplierprofile_btn_modal', 'href'),
    ],
    [
        Input('supplierprofile_submit', 'n_clicks'),
        Input('supplierprofile_btn_modal', 'n_clicks'),
    ],
    [
        
        State('supplierprofile_name', 'value'),
        State('supplierprofile_addr', 'value'),
        State('supplierprofile_status', 'value'),
        State('supplierprofile_terms', 'value'),
        State('supplierprofile_con', 'value'),
        State('supplierprofile_remarks', 'value'),
        State('url', 'search'), 
        State('supplierprofile_removerecord', 'value'), #add this
    ]
)
def movieprofile_saveprofile(submitbtn,closebtn, name, addr, status, terms, con, remarks, search,
                            removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        print(eventid)
        if eventid == 'supplierprofile_submit' and submitbtn:
            
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
           
            if not name: 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the supplier name.'
            elif not addr:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the supplier address.'
            elif not status:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the supplier status.'
            elif not terms:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the supplier terms.'
            elif not con:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the supplier contact number.'
            elif not remarks:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the supplier remarks.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                print('here')
                if create_mode == 'add':
                    sql = '''
                        INSERT INTO supplier (sup_name, sup_addr, sup_status, sup_terms, sup_con, sup_remarks)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    '''
                    values = [name, addr, status, terms, con, remarks]
                    db.modifydatabase(sql, values)
                    feedbackmessage = "supplier has been saved."
                    okay_href = '/suppliers'
                    modal_open = True
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    sup_id = parse_qs(parsed.query)['id'][0]
                    print("ID of supplier: ", sup_id)
                    sqlcode = """UPDATE supplier
                    SET
                        sup_name = %s,
                        sup_addr = %s,
                        sup_status = %s,
                        sup_terms = %s,
                        sup_con = %s,
                        sup_remarks = %s,
                        sup_delete = %s
                    WHERE
                        sup_id = %s
                    """
                    to_delete = bool(removerecord)
                    values = [name, addr, status, terms, con, remarks, to_delete, sup_id]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "Supplier has been updated."
                    okay_href = '/suppliers'
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
        Output('supplierprofile_name', 'value'),
        Output('supplierprofile_addr', 'value'),
        Output('supplierprofile_status', 'value'),
        Output('supplierprofile_terms', 'value'),
        Output('supplierprofile_con', 'value'),
        Output('supplierprofile_remarks', 'value'),
    ],
    [
        
        Input('supplierprofile_toload', 'modified_timestamp')
    ],
    [
        
        State('supplierprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def supplierprofile_loadprofile(timestamp, toload, search):
    print(f'toload: {toload}')
    if toload: 
        
        parsed = urlparse(search)
        sup_id = parse_qs(parsed.query)['id'][0]
        print("ID of supplier: ", sup_id)
        sql = """
            SELECT sup_name, sup_addr, sup_status, sup_terms, sup_con, sup_remarks
            FROM supplier
            WHERE sup_id = %s
        """
        values = [sup_id]
        col = ['name', 'addr', 'status', 'terms', 'contactnumber', 'remarks']
        df = db.querydatafromdatabase(sql, values, col)

        name = df['name'][0]
        addr = df['addr'][0]
        status = df['status'][0]
        terms = df['terms'][0]
        contactnumber = df['contactnumber'][0]
        remarks = df['remarks'][0]
   
        return [name, addr, status, terms, contactnumber, remarks]
    else:
        raise PreventUpdate