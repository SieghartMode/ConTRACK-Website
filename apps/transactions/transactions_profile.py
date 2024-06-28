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
from apps.transactions import transactions_utils as util


#### CSS FOR ALL THE STANDARD PAGES ######
external_stylesheets = ['assets/otherpages.css']

layout = html.Div(
    className='profile-bg', 

    children = [
        html.Div( 
            [
                dcc.Store(id='transactionsprof_toload', storage_type='memory', data=0),
                
                dcc.Store(id='transactionsprof_transactionsid', storage_type='memory', data=0),
                
                dcc.Store(id='transactionsprof_linetoedit', storage_type='memory', data=0),
            ]
        ),

        html.H2("Transaction Details", className = 'page-header'),
        html.Hr(),

#####INPUT BOXES #######
html.Div(
    
    [

        dbc.Row(
            [
                ########### FIRST COL ###############
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Label("Document No.", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type='text', 
                                        id='transactionsprof_docno',
                                        placeholder='DocType-000000'
                                    ),
                                    width=5
                                )
                            ],
                            className='mb-3'
                        ),

                        dbc.Row(
                            [
                                dbc.Label("Transaction Date", width=4),
                                dbc.Col(
                                    dcc.DatePickerSingle(
                                        id='transactionsprof_transactiondate',
                                        date=date.today()
                                    ),
                                    width=3,
                                ),
                            ],
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Label("Customer", width=2),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='transactionsprof_cust',
                                        placeholder='Select Customer', style={'margin-left': '50px'}
                                    ),
                                    width=8
                                )
                            ],
                            className='mb-3'
                        ),
                    ],
                    width=6,
                ),  

                ########### SECOND COL ###############
                dbc.Col(
                    [
                        dbc.Row(
                    [
                        dbc.Label("Status", width=4),
                        dbc.Col(
                            dcc.Dropdown(
                                id='transactionsprof_status',
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
                        dbc.Label("Total", width=4),
                        dbc.Col(
                            dbc.Input(
                                type='number', 
                                id='transactionsprof_total',
                                placeholder='Enter Transaction Total'
                            ),
                            width=5
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Transaction Remarks", width=4, style={'margin-top':'-40px'}),
                        dbc.Col(
                            dbc.Textarea(
                                className="mb-3",
                                placeholder="Add remarks",
                                id='transactionsprof_remarks',
                                style = {'margin-left':'-5px'}
                            ),
                            width=5,
                        ),
                    ],
                    className="mb-3",
                ),
                    ],
                    width=6,
                )
            ]
        )
    ]
),
html.Hr(),

        html.Div(
            [
                dbc.Alert("Please fill out the information above before proceeding", id='transactionsprof_alertmissingdata',
                          color='danger', is_open=False),
                
                

                dbc.Button("Add Line Item", id="transactionsprof_addlinebtn", 
                           color='primary', n_clicks=0,
                           className = 'add-btn'
                           #style={'display':'inline-block','border-radius':'5px', 'margin-right':'20px'}
                ),
              
                html.Br(),
                html.Br(),
                html.Div(
                    id='transactionsprof_lineitems'
                )
            ]    
        ),
        
        dbc.Modal(
            [
                dbc.ModalHeader("Add Line Item", id='transactionsprof_linemodalhead'),
                dbc.ModalBody(
                    [
                        dbc.Alert(id='transactionsprof_linealert', color='warning', is_open=False),
                        dbc.Row(
                            [
                                dbc.Label("Item", width=4),
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(
                                            id='transactionsprof_lineitem',
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
                                dbc.Label("Qty", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="transactionsprof_lineqty", placeholder="Enter qty"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Price", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="transactionsprof_lineprc", placeholder="Enter price"
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
                                            id='transactionsprof_lineremove',
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
                            id='transactionsprof_lineremove_div'
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        #####CANCEL AND SAVE BUTTONS######
                        html.Div(
                            [
                                dbc.Button('Cancel', id='transactionsprof_cancellinebtn', color='secondary'),
                                dbc.Button('Save Line Item', id='transactionsprof_savelinebtn', color='primary'),
                            ],
                            className='d-flex justify-content-between',
                            style={'flex': '1'}
                        )
                    ]
                )
            ],
            id='transactionsprof_modal',
            backdrop='static',
            centered=True
        ),
        
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='transactionsprof_removerecord',
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
            id='transactionsprof_removerecord_div'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Trying to leave the page...")),
                dbc.ModalBody("tempmessage", id='transactionsprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="transactionsprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="transactionsprof_modalsubmitted",
            is_open=False,
        ),
        html.Hr(),
        

        ###### CANCEL AND SUBMIT BUTTONS (REAL) #####
        html.Div(
                [
                    ######ADD LINE ITEM BUTTON#######
                    dbc.Button('Cancel', id='transactionsprof_cancelbtn', className='cancel-btn'),
                    dbc.Button('Submit', id='transactionsprof_savebtn', className='submit-btn'),
                ],
                className='d-flex justify-content-center', 
                style={'margin-top': '20px', 'padding-bottom': '20px'} 
        )

    ]
)

@app.callback(
    [
        Output('transactionsprof_toload', 'data'),
        Output('transactionsprof_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') 
    ]
)
def pageLoadOperations(pathname, search):
    
    if pathname == '/transactions/transactions_profile':
                
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate

    return [to_load, removediv_style]

@app.callback(
    [
        Output('transactionsprof_docno', 'value'),
        Output('transactionsprof_transactiondate', 'date'),
        Output('transactionsprof_cust', 'value'),
        Output('transactionsprof_status', 'value'),
        Output('transactionsprof_total', 'value'),
        Output('transactionsprof_remarks', 'value'),
    ],
    [
        Input('transactionsprof_toload', 'modified_timestamp'),
       
    ],
    [
        State('transactionsprof_toload', 'data'),
        State('url', 'search') 
    ]
)
def populateTRData(timestamp, toload, search):
    if toload == 1:
        
        parsed = urlparse(search)
        tr_id = int(parse_qs(parsed.query)['id'][0])
        
        sql = """SELECT tr_docno, tr_date, cust_name, tr_status, tr_total, tr_remarks
        FROM transaction t 
        INNER JOIN customer c ON c.cust_id = t.cust_id
        WHERE tr_id = %s"""
        val = [tr_id]
        col = ['docno', 'date', 'custname', 'status', 'total', 'remarks']
       
        df = db.querydatafromdatabase(sql, val, col)
        
        docno, transactiondate, custname, status, total, remarks = [df[i][0] for i in col]
        
    else:
        raise PreventUpdate
    
    return [docno, transactiondate, custname, status, total, remarks]

@app.callback(
    [
        Output('transactionsprof_modal', 'is_open'),
        Output('transactionsprof_alertmissingdata', 'is_open'),
        Output('transactionsprof_lineremove_div', 'className'),
        Output('transactionsprof_transactionsid', 'data'),
        
        Output('transactionsprof_lineitem', 'options'),
        Output('transactionsprof_linealert', 'children'),
        Output('transactionsprof_linealert', 'is_open'),
        Output('transactionsprof_linetoedit', 'data'),
        
        Output('transactionsprof_lineitems', 'children'),
        Output('transactionsprof_linemodalhead', 'children'),
        Output('transactionsprof_savelinebtn', 'children'),
    ],
    [
        Input('transactionsprof_addlinebtn', 'n_clicks'),
        Input('transactionsprof_savelinebtn', 'n_clicks'),
        Input('transactionsprof_cancellinebtn', 'n_clicks'),
        Input({'index': ALL, 'type': 'transactionsprof_editlinebtn'}, 'n_clicks'),
        
        Input('transactionsprof_toload', 'modified_timestamp'),
        
    ],
    [
        State('url', 'search'),
        State('transactionsprof_docno', 'value'),
        State('transactionsprof_transactiondate', 'date'),
        State('transactionsprof_cust', 'value'),
        State('transactionsprof_status', 'value'),
        State('transactionsprof_total', 'value'),
        State('transactionsprof_remarks', 'value'),

        State('transactionsprof_transactionsid', 'data'),
        
        State('transactionsprof_lineitem', 'options'),
        State('transactionsprof_lineitem', 'value'),
        State('transactionsprof_lineqty', 'value'),
        State('transactionsprof_lineprc', 'value'),
        State('transactionsprof_linetoedit', 'data'),
        
        State('transactionsprof_lineremove', 'value'),
        State('transactionsprof_lineitems', 'children'),
        State('transactionsprof_toload', 'data'),
        State('transactionsprof_linemodalhead', 'children'),
        
        State('transactionsprof_savelinebtn', 'children'),
    ]
)
def toggleModal(addlinebtn, savebtn, cancelbtn, editlinebtn,
                toload_timestamp,
                
                search, docno, transactiondate, custname, status, total, remarks, tr_id,
                item_options, itemid, itemqty, itemprc, linetoedit,
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
        docno, transactiondate, custname, status, total, remarks
    ]
    
    if eventid == 'transactionsprof_addlinebtn' and addlinebtn and all(TR_requireddata):
        openmodal = True
        item_options = util.getItemDropdown('add', tr_id)
        linetoedit = 0
        
        linemodalhead = 'Add Line Item'
        addlinebtntxt = 'Save Line Item'
    
    elif eventid == 'transactionsprof_addlinebtn' and addlinebtn and not all(TR_requireddata):
        openalert_missingdata = True
        
    elif eventid == 'transactionsprof_cancellinebtn' and cancelbtn:
        pass
    
    elif 'transactionsprof_editlinebtn' in eventid and any(editlinebtn):
        
        openmodal = True
        lineremove_class = '' 
        linetoedit = int(json.loads(eventid)['index'])
        item_options = util.getItemDropdown('edit', tr_id)
        
        linemodalhead = 'Edit Line Item'
        addlinebtntxt = 'Update Line Item'
        
    elif eventid == 'transactionsprof_toload' and toload == 1:
        updatetable = True
        tr_id = int(parse_qs(parsed.query)['id'][0])
    
        
    elif eventid == 'transactionsprof_savelinebtn' and savebtn:
        inputs = [
            itemid, 
            util.converttoint(itemqty)>0,
            util.converttoint(itemprc)>0
        ]
        
        if not all(inputs):
            linealert_message = "Please ensure that fields are filled in and inputs are correct."
        
        else:
            
            newline = {
                'itemid': itemid,
                'itemqty': itemqty,
                'itemprc': itemprc,
            }
            
            if linetoedit == 0:
                if not tr_id:
                    tr_id = util.createTRrecord(docno, transactiondate, custname, status, total, remarks)
                
                util.manageTRLineItem(tr_id, newline)
            
            else:
                if removeitem:
                    util.removeLineItem(linetoedit)
                else:
                    util.manageTRLineItem(tr_id, newline)
            
            updatetable = True
    
    else:
        raise PreventUpdate
    
    
    if updatetable:
        df = util.queryTRLineItems(tr_id)
        
        if df.shape[0]:
            linetable = util.formatTRtable(df)
        else:
            linetable = html.Div('No records to display', style={'color':'#777', 'padding-left': '2em'})

    openalert_linealert = bool(linealert_message)
    
    return [
        openmodal, 
        openalert_missingdata, 
        lineremove_class,
        tr_id,
        
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
        Output('transactionsprof_lineitem', 'value'),
        Output('transactionsprof_lineqty', 'value'),
        Output('transactionsprof_lineprc', 'value'),
        Output('transactionsprof_lineremove', 'value'),
    ],
    [
        Input('transactionsprof_addlinebtn', 'n_clicks'),
        Input('transactionsprof_linetoedit', 'modified_timestamp'),
    ],
    [
        State('transactionsprof_linetoedit', 'data'),
        State('transactionsprof_lineitem', 'value'),
        State('transactionsprof_lineqty', 'value'),
        State('transactionsprof_lineprc', 'value'),
        State('transactionsprof_lineremove', 'value'),
    ]
)
def clearFields(addlinebtn, line_timestamp, 
                
                linetoedit, itemid, itemqty, itemprc, removeitem):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    
    if eventid == 'transactionsprof_addlinebtn' and addlinebtn:
        itemid, itemqty, itemprc= None, None, None
        removeitem = []
        
    elif eventid == 'transactionsprof_linetoedit' and linetoedit:
        itemid, itemqty, itemprc = util.getTRLineData(linetoedit)
        removeitem = []
        
    else:
        raise PreventUpdate
    
    return [itemid, itemqty, itemprc, removeitem]

@app.callback(
    [
        Output('transactionsprof_modalsubmitted', 'is_open'),
        Output('transactionsprof_feedback_message', 'children'),
        Output('transactionsprof_closebtn', 'href'),
    ],
    [
        Input('transactionsprof_savebtn', 'n_clicks'),
        Input('transactionsprof_cancelbtn', 'n_clicks'),
        Input('transactionsprof_closebtn', 'n_clicks'),
    ],
    [
        State('transactionsprof_transactionsid', 'data'),
        State('transactionsprof_removerecord', 'value'),
        State('transactionsprof_toload', 'data') 
    ]
)
def finishTransaction(submitbtn, cancelbtn, closebtn,
                      
                      tr_id, removerecord, iseditmode):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate
    
    if eventid == 'transactionsprof_savebtn' and submitbtn:
        openmodal = True
        
        if not tr_id:
            feedbackmessage = "You have not filled out the form."
            
        elif not util.checkTRLineItems(tr_id):
            feedbackmessage = "Please add line items"
            
        elif removerecord:
            util.deleteTR(tr_id)
            feedbackmessage = "Record has been deleted. Click OK to go back to Transactions Home."
            okay_href = '/transactions'
            
        else:
            feedbackmessage = "Transactions is saved. Click OK to go back to Transactions Home."
            okay_href = '/transactions'
            
    elif eventid == 'transactionsprof_cancelbtn' and cancelbtn:
        openmodal = True
        
        if not tr_id:
            feedbackmessage = "Click OK to go back to Transaction Home."
            okay_href = '/transactions'
        elif iseditmode and tr_id:
            feedbackmessage = "Changes have been discarded. Click OK to go back to Transaction Home."
            okay_href = '/transactions'
        else:
            feedbackmessage = "Click OK to go back to Transaction Home."
            okay_href = '/transactions'
            
    
    elif eventid == 'transactionsprof_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]

@app.callback(
    Output('transactionsprof_cust', 'options'),
    [Input('transactionsprof_toload', 'modified_timestamp')]
)
def update_customer_options(timestamp):
    sql = "SELECT cust_id, cust_name FROM customer WHERE cust_delete = false"
    df = db.querydatafromdatabase(sql, [], ['cust_id', 'cust_name'])

    options = [{'label': row['cust_name'], 'value': str(row['cust_id'])} for index, row in df.iterrows()]

    return options