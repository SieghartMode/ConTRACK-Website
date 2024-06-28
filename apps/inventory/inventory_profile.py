import json
from datetime import date
from urllib.parse import parse_qs, urlparse

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db
from apps.inventory import inventory_utils as util

layout = html.Div(
     className='profile-bg',

    children = [
        html.Div( 
            [
                dcc.Store(id='inventoryprof_toload', storage_type='memory', data=0),
                
                dcc.Store(id='inventoryprof_inventoryid', storage_type='memory', data=0),
                
                dcc.Store(id='inventoryprof_linetoedit', storage_type='memory', data=0),
            ]
        ),

        html.H2("Inventory Entry Details", className = 'page-header'),
        html.Hr(),

#####INPUT BOXES #######
html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        # Left Column
                        dbc.Row(
                            [
                                dbc.Label("Document No.", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type='text', 
                                        id='inventoryprof_docno',
                                        placeholder='DocType-000000'
                                    ),
                                    width=5
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Document Type", width=4),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='inventoryprof_type',
                                        placeholder='Select Document Type',
                                        options=[
                                            {'label': 'Sales Order', 'value': 'Sales Order'},
                                            {'label': 'Job Order', 'value': 'Job Order'},
                                            {'label': 'Beginning Balance', 'value': 'Beginning Balance'},
                                            {'label': 'Adjustment', 'value': 'Adjustment'},
                                            {'label': 'Production', 'value': 'Production'},
                                            {'label': 'Delivery', 'value': 'Delivery'},
                                        ]
                                    ),
                                    width=5
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Document Date", width=4),
                                dbc.Col(
                                    dcc.DatePickerSingle(
                                        id='inventoryprof_inventorydate',
                                        date=date.today()
                                    ),
                                    width=5,
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                    width=6
                ),

                dbc.Col(
                    [
                        # Right Column
                        dbc.Row(
                            [
                                dbc.Label("Customer", width=4),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='inventoryprof_cust',
                                        placeholder='Select Customer',
                                    ),
                                    width=5
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Status", width=4),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='inventoryprof_status',
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
                        dbc.Row(
                            [
                                dbc.Label("Entry Remarks", width=4, style={'margin-top':'-40px'}),
                                dbc.Col(
                                    dbc.Textarea(
                                        className="mb-3",
                                        placeholder="Add remarks",
                                        id='inventoryprof_remarks',
                                        style = {'margin-left':'-5px'}
                                    ),
                                    width=5,
                                ),
                            ],
                            className="mb-3",
                        ),
                    ],
                    width=6
                ),
            ]
        )
    ]
),



        html.Hr(),
        html.Div(
            [
                dbc.Alert("Please fill out the information above before proceeding", id='inventoryprof_alertmissingdata',
                          color='danger', is_open=False),
                dbc.Button("Add Line Item", id="inventoryprof_addlinebtn", 
                           color='primary', n_clicks=0, className = 'add-btn',
                           style={'display':'inline-block','border-radius':'5px'}
                ),  
                html.Br(),
                html.Br(),
                html.Div(
                    id='inventoryprof_lineitems'
                )
            ]    
        ),
        
        dbc.Modal(
            [
                dbc.ModalHeader("Add Line Item", id='inventoryprof_linemodalhead'),
                dbc.ModalBody(
                    [
                        dbc.Alert(id='inventoryprof_linealert', color='warning', is_open=False),
                        dbc.Row(
                            [
                                dbc.Label("Item", width=4),
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(
                                            id='inventoryprof_lineitem',
                                            clearable=True,
                                            searchable=True,
                                            options=[]
                                        ), 
                                        className="dash-bootstrap"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("IN", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="inventoryprof_linein", placeholder="Enter QTY IN", value='0'
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("OUT", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="inventoryprof_lineout", placeholder="Enter QTY OUT", value='0'
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("SO", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="inventoryprof_lineso", placeholder="Enter QTY SO", value='0'
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("JO", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="inventoryprof_linejo", placeholder="Enter QTY JO", value="0"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=4),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='inventoryprof_lineremove',
                                            options=[
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ],
                                            style={'fontWeight':'bold'}, 
                                        ),
                                        width=6,
                                        style={'margin': 'auto 0'}
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='inventoryprof_lineremove_div'
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        html.Div(
                            [
                                dbc.Button('Cancel', id='inventoryprof_cancellinebtn', ),
                                dbc.Button('Save Line Item', id='inventoryprof_savelinebtn', color='primary'),
                            ],
                            className='d-flex justify-content-between',
                            style={'flex': '1'}
                        )
                    ]
                )
            ],
            id='inventoryprof_modal',
            backdrop='static',
            centered=True
        ),
        
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='inventoryprof_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            style={'fontWeight':'bold'}, 
                        ),
                        width=6,
                        style={'margin': 'auto 0'}
                    ),
                ],
                className="mb-3",
            ),
            id='inventoryprof_removerecord_div'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Trying to leave the page...")),
                dbc.ModalBody("tempmessage", id='inventoryprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="inventoryprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="inventoryprof_modalsubmitted",
            is_open=False,
        ),
        html.Hr(),
        
        html.Div(
            [
                dbc.Button('Cancel', id='inventoryprof_cancelbtn', className='cancel-btn'),
                dbc.Button('Submit',  id='inventoryprof_savebtn', className='submit-btn'),
            ],
            className='d-flex justify-content-center',
            style={'flex': '1'}
        )
    ]
)

@app.callback(
    [
        Output('inventoryprof_toload', 'data'),
        Output('inventoryprof_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') 
    ]
)
def pageLoadOperations(pathname, search):
    
    if pathname == '/inventory/inventory_profile':
                
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate

    return [to_load, removediv_style]

@app.callback(
    [
        Output('inventoryprof_docno', 'value'),
        Output('inventoryprof_type', 'value'),
        Output('inventoryprof_inventorydate', 'date'),
        Output('inventoryprof_cust', 'value'),
        Output('inventoryprof_status', 'value'),
        Output('inventoryprof_remarks', 'value'),
    ],
    [
        Input('inventoryprof_toload', 'modified_timestamp'),
    ],
    [
        State('inventoryprof_toload', 'data'),
        State('url', 'search') 
    ]
)
def populateTRData(timestamp, toload, search):
    if toload == 1:
        
        parsed = urlparse(search)
        inv_id = int(parse_qs(parsed.query)['id'][0])
        
        sql = """SELECT inv_docno, inv_type, inv_date, i.cust_id, inv_status, inv_remarks
        FROM inventory i 
        INNER JOIN customer c ON c.cust_id = i.cust_id
        WHERE inv_id = %s"""
        val = [inv_id]
        col = ['docno', 'type', 'date', 'custname', 'status', 'remarks']
       
        df = db.querydatafromdatabase(sql, val, col)
        
        docno, type, inventorydate, custname, status, remarks = [df[i][0] for i in col]
        
    else:
        raise PreventUpdate
    
    return [docno, type, inventorydate, custname, status, remarks]

@app.callback(
    [
        Output('inventoryprof_modal', 'is_open'),
        Output('inventoryprof_alertmissingdata', 'is_open'),
        Output('inventoryprof_lineremove_div', 'className'),
        Output('inventoryprof_inventoryid', 'data'),
        
        Output('inventoryprof_lineitem', 'options'),
        Output('inventoryprof_linealert', 'children'),
        Output('inventoryprof_linealert', 'is_open'),
        Output('inventoryprof_linetoedit', 'data'),
        
        Output('inventoryprof_lineitems', 'children'),
        Output('inventoryprof_linemodalhead', 'children'),
        Output('inventoryprof_savelinebtn', 'children'),
    ],
    [
        Input('inventoryprof_addlinebtn', 'n_clicks'),
        Input('inventoryprof_savelinebtn', 'n_clicks'),
        Input('inventoryprof_cancellinebtn', 'n_clicks'),
        Input({'index': ALL, 'type': 'inventoryprof_editlinebtn'}, 'n_clicks'),
        
        Input('inventoryprof_toload', 'modified_timestamp'),
        
    ],
    [
        State('url', 'search'),
        State('inventoryprof_docno', 'value'),
        State('inventoryprof_type', 'value'),
        State('inventoryprof_inventorydate', 'date'),
        State('inventoryprof_cust', 'value'),
        State('inventoryprof_status', 'value'),
        State('inventoryprof_remarks', 'value'),

        State('inventoryprof_inventoryid', 'data'),
        
        State('inventoryprof_lineitem', 'options'),
        State('inventoryprof_lineitem', 'value'),
        State('inventoryprof_linein', 'value'),
        State('inventoryprof_lineout', 'value'),
        State('inventoryprof_lineso', 'value'),
        State('inventoryprof_linejo', 'value'),
        State('inventoryprof_linetoedit', 'data'),
        
        State('inventoryprof_lineremove', 'value'),
        State('inventoryprof_lineitems', 'children'),
        State('inventoryprof_toload', 'data'),
        State('inventoryprof_linemodalhead', 'children'),
        
        State('inventoryprof_savelinebtn', 'children'),
    ]
)
def toggleModal(addlinebtn, savebtn, cancelbtn, editlinebtn,
                toload_timestamp,
                
                search, docno, type, inventorydate, custname, status, remarks, inv_id,
                item_options, itemid, itemin, itemout, itemso, itemjo, linetoedit,
                removeitem, linetable, toload, linemodalhead,
                addlinebtntxt):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        parsed = urlparse(search)
        
        openmodal = False
        openalert_missingdata = False
        lineremove_class = 'd-none' 
        
        linealert_message = ''
        updatetable = False 
    else:
        raise PreventUpdate
    
    TR_requireddata = [
        docno, type, inventorydate, custname, status, remarks
    ]
    
    if eventid == 'inventoryprof_addlinebtn' and addlinebtn and all(TR_requireddata):
        openmodal = True
        item_options = util.getItemDropdown('add', inv_id)
        linetoedit = 0
        
        linemodalhead = 'Add Line Item'
        addlinebtntxt = 'Save Line Item'
    
    elif eventid == 'inventoryprof_addlinebtn' and addlinebtn and not all(TR_requireddata):
        openalert_missingdata = True
        
    elif eventid == 'inventoryprof_cancellinebtn' and cancelbtn:
        pass
    
    elif 'inventoryprof_editlinebtn' in eventid and any(editlinebtn):
        
        openmodal = True
        lineremove_class = '' 
        linetoedit = int(json.loads(eventid)['index'])
        item_options = util.getItemDropdown('edit', inv_id)
        
        linemodalhead = 'Edit Line Item'
        addlinebtntxt = 'Update Line Item'
        
    elif eventid == 'inventoryprof_toload' and toload == 1:
        updatetable = True
        inv_id = int(parse_qs(parsed.query)['id'][0])
    
        
    elif eventid == 'inventoryprof_savelinebtn' and savebtn:
        inputs = [
            itemid, 
            util.converttoint(itemin)>=0,
            util.converttoint(itemout)>=0,
            util.converttoint(itemso)>=0,
            util.converttoint(itemjo)>=0
        ]
        
        if not all(inputs):
            linealert_message = "Please ensure that fields are filled in and inputs are correct."
        
        else:
            
            newline = {
                'itemid': itemid,
                'itemin': itemin,
                'itemout': itemout,
                'itemso': itemso,
                'itemjo': itemjo,
            }
            
            if linetoedit == 0:
                if not inv_id:
                    inv_id = util.createTRrecord(docno, type, inventorydate, custname, status, remarks)
                
                util.manageTRLineItem(inv_id, newline)
            
            else:
                if removeitem:
                    util.removeLineItem(linetoedit)
                else:
                    util.manageTRLineItem(inv_id, newline)
            
            updatetable = True
    
    else:
        raise PreventUpdate
    
    
    if updatetable:
        df = util.queryTRLineItems(inv_id)
        
        if df.shape[0]:
            linetable = util.formatTRtable(df)
        else:
            linetable = html.Div('No records to display', style={'color':'#777', 'padding-left': '2em'})

    openalert_linealert = bool(linealert_message)
    
    return [
        openmodal, 
        openalert_missingdata, 
        lineremove_class,
        inv_id,
        
        item_options,
        linealert_message,
        openalert_linealert,
        linetoedit,
        
        linetable,
        linemodalhead,
        addlinebtntxt
    ]

@app.callback(
    [
        Output('inventoryprof_lineitem', 'value'),
        Output('inventoryprof_linein', 'value'),
        Output('inventoryprof_lineout', 'value'),
        Output('inventoryprof_lineso', 'value'),
        Output('inventoryprof_linejo', 'value'),
        Output('inventoryprof_lineremove', 'value'),
    ],
    [
        Input('inventoryprof_addlinebtn', 'n_clicks'),
        Input('inventoryprof_linetoedit', 'modified_timestamp'),
    ],
    [
        State('inventoryprof_linetoedit', 'data'),
        State('inventoryprof_lineitem', 'value'),
        State('inventoryprof_linein', 'value'),
        State('inventoryprof_lineout', 'value'),
        State('inventoryprof_lineso', 'value'),
        State('inventoryprof_linejo', 'value'),
        State('inventoryprof_lineremove', 'value'),
    ]
)
def clearFields(addlinebtn, line_timestamp, 
                
                linetoedit, itemid, itemin, itemout, itemso, itemjo, removeitem):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    
    if eventid == 'inventoryprof_addlinebtn' and addlinebtn:
        itemid, itemin, itemout, itemso, itemjo = None, None, None, None, None
        removeitem = []
        
    elif eventid == 'inventoryprof_linetoedit' and linetoedit:
        itemid, itemin, itemout, itemso, itemjo = util.getTRLineData(linetoedit)
        removeitem = []
        
    else:
        raise PreventUpdate
    
    return [itemid, itemin, itemout, itemso, itemjo, removeitem]

@app.callback(
    [
        Output('inventoryprof_modalsubmitted', 'is_open'),
        Output('inventoryprof_feedback_message', 'children'),
        Output('inventoryprof_closebtn', 'href'),
    ],
    [
        Input('inventoryprof_savebtn', 'n_clicks'),
        Input('inventoryprof_cancelbtn', 'n_clicks'),
        Input('inventoryprof_closebtn', 'n_clicks'),
    ],
    [
        State('inventoryprof_inventoryid', 'data'),
        State('inventoryprof_removerecord', 'value'),
        State('inventoryprof_toload', 'data') 
    ]
)
def finishTransaction(submitbtn, cancelbtn, closebtn,
                      
                      inv_id, removerecord, iseditmode):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate
    
    if eventid == 'inventoryprof_savebtn' and submitbtn:
        openmodal = True
        
        if not inv_id:
            feedbackmessage = "You have not filled out the form."
            
        elif not util.checkTRLineItems(inv_id):
            feedbackmessage = "Please add line items"
            
        elif removerecord:
            util.deleteTR(inv_id)
            feedbackmessage = "Record has been deleted. Click OK to go back to Transactions Home."
            okay_href = '/inventory'
            
        else:
            feedbackmessage = "Transactions is saved. Click OK to go back to Transactions Home."
            okay_href = '/inventory'
            
    elif eventid == 'inventoryprof_cancelbtn' and cancelbtn:
        openmodal = True
        
        if not inv_id:
            feedbackmessage = "Click OK to go back to Transaction Home."
            okay_href = '/inventory'
        elif iseditmode and inv_id:
            feedbackmessage = "Changes have been discarded. Click OK to go back to Transaction Home."
            okay_href = '/inventory'
        else:
            feedbackmessage = "Click OK to go back to Transaction Home."
            okay_href = '/inventory'
            
    
    elif eventid == 'inventoryprof_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]

@app.callback(
    Output('inventoryprof_cust', 'options'),
    [Input('inventoryprof_toload', 'modified_timestamp')]
)

def update_customer_options(timestamp):
    sql = "SELECT cust_id, cust_name FROM customer WHERE cust_delete = false"
    df = db.querydatafromdatabase(sql, [], ['cust_id', 'cust_name'])

    options = [{'label': row['cust_name'], 'value': str(row['cust_id'])} for index, row in df.iterrows()]

    return options