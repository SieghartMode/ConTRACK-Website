import hashlib
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs
import pandas as pd
import webbrowser

from app import app
from apps import dbconnect as db

layout = html.Div(
    className='profile-bg',
    children=[
        html.Div(
            [
                dcc.Store(id='contractsprofile_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2('Contract Details', className='page-header'),
        html.Hr(),
        dbc.Alert(id='contractsprofile_alert', is_open=False),
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
                                                dbc.Label("Title", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_title',
                                                        placeholder="Enter Contract Title"
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Type", width=4),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id='contractsprofile_type',
                                                        placeholder='Select Contract Type',
                                                        options=[
                                                            {'label': 'Collaborative Agreement', 'value': 'Collaborative Agreement'},
                                                            {'label': 'Licensing', 'value': 'Licensing'},
                                                            {'label': 'Research Use', 'value': 'Research Use'},
                                                        ]
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Description", width=4),
                                                dbc.Col(
                                                    dbc.Textarea(
                                                        id='contractsprofile_desc',
                                                        placeholder='Contract Description'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Name", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ipname',
                                                        placeholder='IP Name'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("UPSCALExIP Meeting Sched", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_sc1',
                                                        placeholder='Enter Meeting Sched'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Meeting Scheduled?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_sched1done',
                                                        placeholder='Meeting Scheduled?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Upload Client LOI", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_loi',
                                                        placeholder='Upload LOI'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("LOI Approved?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_aloi',
                                                        placeholder='LOI Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Contract Draft", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_con',
                                                        placeholder='Upload Contract Draft'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Contract Draft Feedback R1 (IP)", width=4),
                                                dbc.Col(
                                                    dbc.Textarea(
                                                        id='contractsprofile_ip_fb1',
                                                        placeholder='IP Feedback 1'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Approved R1?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ip_fbd1',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Revised Contract R1", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_ip_doc1',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Contract Draft Feedback R1 (UPSCALE)", width=4),
                                                dbc.Col(
                                                    dbc.Textarea(
                                                        id='contractsprofile_ups_fb1',
                                                        placeholder='UPSCALE Feedback 1'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("UPSCALE Approved R1?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ups_fbd1',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("UPSCALE Revised Contract R1", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_ups_doc1',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Contract Draft Feedback R2 (IP)", width=4),
                                                dbc.Col(
                                                    dbc.Textarea(
                                                        id='contractsprofile_ip_fb2',
                                                        placeholder='IP Feedback 2'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Approved R2?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ip_fbd2',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Revised Contract R2", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_ip_doc2',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Contract Draft Feedback R2 (UPSCALE)", width=4),
                                                dbc.Col(
                                                    dbc.Textarea(
                                                        id='contractsprofile_ups_fb2',
                                                        placeholder='UPSCALE Feedback 2'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("UPSCALE Approved R2?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ups_fbd2',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("UPSCALE Revised Contract R2", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_ups_doc2',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        
                                    ]
                                ),
                            ],
                            width=5
                        ),
                        dbc.Col(
                            [
                                # Right Column
                                dbc.Form(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Contract Draft Feedback R3 (IP)", width=4),
                                                dbc.Col(
                                                    dbc.Textarea(
                                                        id='contractsprofile_ip_fb3',
                                                        placeholder='IP Feedback 3'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Approved R3?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ip_fbd3',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Revised Contract R3", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_ip_doc3',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Contract Draft Feedback R3 (UPSCALE)", width=4),
                                                dbc.Col(
                                                    dbc.Textarea(
                                                        id='contractsprofile_ups_fb3',
                                                        placeholder='UPSCALE Feedback 1'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("UPSCALE Approved R3?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ups_fbd3',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("UPSCALE Revised Contract R3", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_ups_doc3',
                                                        placeholder='Contract Approved?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Final Contract Approval", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ip_final',
                                                        placeholder='IP Approve Contract?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("UPSCALE Final Contract Approval", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ups_final',
                                                        placeholder='UPSCALE Approve Contract?'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Final Meeting Schedule", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ups_meet',
                                                        placeholder='Enter Meeting Schedule'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Final Meeting Done?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ups_meetd',
                                                        placeholder='Enter if meeting is done.'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("OVPLA Signed?", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ovpla_sign',
                                                        placeholder='Enter if OVPLA signed'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("OVPLA Signed Contract", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='file',
                                                        id='contractsprofile_ovpla_docfin',
                                                        placeholder='Upload final signed contract.'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("OVPLA Approve sign contract", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='contractsprofile_ovpla_docfind',
                                                        placeholder='Enter if OVPLA approves this.'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Progress %", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        min='0',
                                                        max='1',
                                                        id='contractsprofile_percent',
                                                        placeholder='Enter the latest contract percent.'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                    ]
                                ),
                            ],
                            width=5
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
                            id='contractsprofile_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            style={'fontWeight': 'bold'},
                        ),
                        width=5,
                    ),
                ],
                className="mb-3",
            ),
            id='contractsprofile_removerecord_div'
        ),
        dbc.Button(
            'Cancel',
            id='contractsprofile_cancel',
            className='cancel-btn',
            href='/contracts'
        ),
        dbc.Button(
            'Submit',
            id='contractsprofile_submit',
            className='submit-btn',
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
                    ], id='contractsprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/contracts/contracts_home',
                        id='contractsprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='contractsprofile_successmodal',
            backdrop='static'
        )
    ]
)

@app.callback(
    [
        Output('contractsprofile_toload', 'data'),
        Output('contractsprofile_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def contractsprof_loaddropdown(pathname, search):
    if pathname == '/contracts/contracts_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [to_load, removediv_style]

@app.callback(
    [
        Output('contractsprofile_alert', 'color'),
        Output('contractsprofile_alert', 'children'),
        Output('contractsprofile_alert', 'is_open'),
        Output('contractsprofile_successmodal', 'is_open'),
        Output('contractsprofile_feedback_message', 'children'),
        Output('contractsprofile_btn_modal', 'href'),
    ],
    [
        Input('contractsprofile_submit', 'n_clicks'),
        Input('contractsprofile_btn_modal', 'n_clicks'),
    ],
    [
        State('contractsprofile_title', 'value'),
        State('contractsprofile_type', 'value'),
        State('contractsprofile_desc', 'value'),
        State('contractsprofile_ipname', 'value'),
        State('contractsprofile_sc1', 'value'),
        State('contractsprofile_sc1done', 'value'),
        State('contractsprofile_loi', 'value'),
        State('contractsprofile_aloi', 'value'),
        State('contractsprofile_con', 'value'),
        State('contractsprofile_ip_fb1', 'value'),
        State('contractsprofile_ip_fbd1', 'value'),
        State('contractsprofile_ip_doc1', 'value'),
        State('contractsprofile_ups_fb1', 'value'),
        State('contractsprofile_ups_fbd1', 'value'),
        State('contractsprofile_ups_doc1', 'value'),
        State('contractsprofile_ip_fb2', 'value'),
        State('contractsprofile_ip_fbd2', 'value'),
        State('contractsprofile_ip_doc2', 'value'),
        State('contractsprofile_ups_fb2', 'value'),
        State('contractsprofile_ups_fbd2', 'value'),
        State('contractsprofile_ups_doc2', 'value'),
        State('contractsprofile_ip_fb3', 'value'),
        State('contractsprofile_ip_fbd3', 'value'),
        State('contractsprofile_ip_doc3', 'value'),
        State('contractsprofile_ups_fb3', 'value'),
        State('contractsprofile_ups_fbd3', 'value'),
        State('contractsprofile_ups_doc3', 'value'),
        State('contractsprofile_ip_final', 'value'),
        State('contractsprofile_ups_final', 'value'),
        State('contractsprofile_ups_meet', 'value'),
        State('contractsprofile_ups_meetd', 'value'),
        State('contractsprofile_ovpla_sign', 'value'),
        State('contractsprofile_ovpla_docfin', 'value'),
        State('contractsprofile_ovpla_docfind', 'value'),
        State('contractsprofile_percent', 'value'),
        State('url', 'search'),
        State('contractsprofile_removerecord', 'value'),
    ]
)
def contractsprofile_saveprofile(submitbtn, closebtn, title, type, desc, ipname, sc1, sc1done, 
                                 loi, aloi, con, ip_fb1, ip_fbd1, ip_doc1, ups_fb1, ups_fbd1, ups_doc1,
                                 ip_fb2, ip_fbd2, ip_doc2, ups_fb2, ups_fbd2, ups_doc2, 
                                 ip_fb3, ip_fbd3, ip_doc3, ups_fb3, ups_fbd3, ups_doc3, ip_final, ups_final, 
                                 ups_meet, ups_meetd, ovpla_sign, ovpla_docfin, ovpla_docfind, percent,
                                 search, removerecord):
    ctx = dash.callback_context
    feedbackmessage = ""  # Initialize feedbackmessage
    okay_href = ""  # Initialize okay_href

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        print(eventid)
        if eventid == 'contractsprofile_submit' and submitbtn:

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            if not title:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the Contract title.'
            elif not type:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the Contract Type.'
            elif not desc:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the Contract Description.'
            elif not ipname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the Contract IP Name.'
            elif not percent:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the Contract Progress %.'
            
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                print('here')
                if create_mode == 'add':
                    sql = '''
                        INSERT INTO contracts (ac_ups_title, ac_ups_type, ac_ups_desc, ac_ups_ipname, ac_ups_sc1, 
                        ac_ups_sched1done, ac_ip_loi, ac_ups_aloi, ac_ups_con, 
                        ac_ip_fb1, ac_ip_fbd1, ac_ip_doc1, ac_ups_fb1, ac_ups_fbd1, ac_ups_doc1, 
                        ac_ip_fb2, ac_ip_fbd2, ac_ip_doc2, ac_ups_fb2, ac_ups_fbd2, ac_ups_doc2,
                        ac_ip_fb3, ac_ip_fbd3, ac_ip_doc3, ac_ups_fb3, ac_ups_fbd3, ac_ups_doc3, 
                        ac_ip_final, ac_ups_final, ac_ups_meet, ac_ups_meetd, ac_ovpla_sign, ac_ovpla_docfin, 
                        ac_ovpla_docfind, ac_percent)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)
                    '''
                    encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()

                    values = [title, type, desc, ipname, sc1, sc1done, 
                                 loi, aloi, con, ip_fb1, ip_fbd1, ip_doc1, ups_fb1, ups_fbd1, ups_doc1,
                                 ip_fb2, ip_fbd2, ip_doc2, ups_fb2, ups_fbd2, ups_doc2, 
                                 ip_fb3, ip_fbd3, ip_doc3, ups_fb3, ups_fbd3, ups_doc3, ip_final, ups_final, 
                                 ups_meet, ups_meetd, ovpla_sign, ovpla_docfin, ovpla_docfind, percent]
                    db.modifydatabase(sql, values)
                    feedbackmessage = "Contract Details have been saved."
                    okay_href = '/home'
                    modal_open = True
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    contracts_id = parse_qs(parsed.query)['id'][0]
                    print("ID of contracts: ", contracts_id)
                    sqlcode = """UPDATE contracts
                    SET
                        ac_ups_title = %s,
                        ac_ups_type = %s,
                        ac_ups_desc = %s,
                        ac_ups_ipname = %s,
                        ac_ups_sc1 = %s,
                        ac_ups_sched1done = %s,
                        ac_ip_loi = %s,
                        ac_ups_aloi = %s,
                        ac_ups_con = %s,
                        ac_ip_fb1 = %s,
                        ac_ip_fbd1 = %s,
                        ac_ip_doc1 = %s,
                        ac_ups_fb1 = %s,
                        ac_ups_fbd1 = %s,
                        ac_ups_doc1 = %s,
                        ac_ip_fb2 = %s,
                        ac_ip_fbd2 = %s,
                        ac_ip_doc2 = %s,
                        ac_ups_fb2 = %s,
                        ac_ups_fbd2 = %s,
                        ac_ups_doc2 = %s,
                        ac_ip_fb3 = %s,
                        ac_ip_fbd3 = %s,
                        ac_ip_doc3 = %s,
                        ac_ups_fb3 = %s,
                        ac_ups_fbd3 = %s,
                        ac_ups_doc3 = %s,
                        ac_ip_final = %s,
                        ac_ups_final = %s,
                        ac_ups_meet = %s,
                        ac_ups_meetd = %s,
                        ac_ovpla_sign = %s,
                        ac_ovpla_docfin = %s,
                        ac_ovpla_docfind = %s,
                        ac_percent = %s,
                        ac_delete = %s
                    WHERE
                        ac_id = %s
                    """

                    encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()

                    to_delete = bool(removerecord)
                    values = [title, type, desc, ipname, sc1, sc1done, 
                                 loi, aloi, con, ip_fb1, ip_fbd1, ip_doc1, ups_fb1, ups_fbd1, ups_doc1,
                                 ip_fb2, ip_fbd2, ip_doc2, ups_fb2, ups_fbd2, ups_doc2, 
                                 ip_fb3, ip_fbd3, ip_doc3, ups_fb3, ups_fbd3, ups_doc3, ip_final, ups_final, 
                                 ups_meet, ups_meetd, ovpla_sign, ovpla_docfin, ovpla_docfind, percent,
                                   to_delete, contracts_id]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "Contract has been updated."
                    okay_href = '/contracts'
                    modal_open = True
                else:
                    raise PreventUpdate
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('contractsprofile_title', 'value'),
        Output('contractsprofile_type', 'value'),
        Output('contractsprofile_desc', 'value'),
        Output('contractsprofile_ipname', 'value'),
        Output('contractsprofile_sc1', 'value'),
        Output('contractsprofile_sc1done', 'value'),
        Output('contractsprofile_loi', 'value'),
        Output('contractsprofile_aloi', 'value'),
        Output('contractsprofile_con', 'value'),
        Output('contractsprofile_ip_fb1', 'value'),
        Output('contractsprofile_ip_fbd1', 'value'),
        Output('contractsprofile_ip_doc1', 'value'),
        Output('contractsprofile_ups_fb1', 'value'),
        Output('contractsprofile_ups_fbd1', 'value'),
        Output('contractsprofile_ups_doc1', 'value'),
        Output('contractsprofile_ip_fb2', 'value'),
        Output('contractsprofile_ip_fbd2', 'value'),
        Output('contractsprofile_ip_doc2', 'value'),
        Output('contractsprofile_ups_fb2', 'value'),
        Output('contractsprofile_ups_fbd2', 'value'),
        Output('contractsprofile_ups_doc2', 'value'),
        Output('contractsprofile_ip_fb3', 'value'),
        Output('contractsprofile_ip_fbd3', 'value'),
        Output('contractsprofile_ip_doc3', 'value'),
        Output('contractsprofile_ups_fb3', 'value'),
        Output('contractsprofile_ups_fbd3', 'value'),
        Output('contractsprofile_ups_doc3', 'value'),
        Output('contractsprofile_ip_final', 'value'),
        Output('contractsprofile_ups_final', 'value'),
        Output('contractsprofile_ups_meet', 'value'),
        Output('contractsprofile_ups_meetd', 'value'),
        Output('contractsprofile_ovpla_sign', 'value'),
        Output('contractsprofile_ovpla_docfin', 'value'),
        Output('contractsprofile_ovpla_docfind', 'value'),
        Output('contractsprofile_percent', 'value'),
    ],
    [
        Input('contractsprofile_toload', 'modified_timestamp')
    ],
    [
        State('contractsprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def contractsprofile_loadprofile(timestamp, toload, search):
    print(f'toload: {toload}')
    if toload:
        parsed = urlparse(search)
        contracts_id = parse_qs(parsed.query)['id'][0]
        print("ID of contracts: ", contracts_id)
        sql = """
            SELECT ac_ups_title, ac_ups_type, ac_ups_desc, ac_ups_ipname, ac_ups_sc1, 
                        ac_ups_sched1done, ac_ip_loi, ac_ups_aloi, ac_ups_con, 
                        ac_ip_fb1, ac_ip_fbd1, ac_ip_doc1, ac_ups_fb1, ac_ups_fbd1, ac_ups_doc1, 
                        ac_ip_fb2, ac_ip_fbd2, ac_ip_doc2, ac_ups_fb2, ac_ups_fbd2, ac_ups_doc2,
                        ac_ip_fb3, ac_ip_fbd3, ac_ip_doc3, ac_ups_fb3, ac_ups_fbd3, ac_ups_doc3, 
                        ac_ip_final, ac_ups_final, ac_ups_meet, ac_ups_meetd, ac_ovpla_sign, ac_ovpla_docfin, 
                        ac_ovpla_docfind, ac_percent
            FROM contracts
            WHERE ac_id = %s
        """
        values = [contracts_id]
        col = ['Title', 'Type', 'Description', 'IP Name', 'scmeet', 'scmeetd', 'loi', 'aloi', 'con', 
               'ip_fb1', 'ip_fbd1', 'ip_doc1', 'ups_fb1', 'ups_fbd1', 'ups_doc1', 
               'ip_fb2', 'ip_fbd2', 'ip_doc2', 'ups_fb2', 'ups_fbd2', 'ups_doc2', 
               'ip_fb3', 'ip_fbd3', 'ip_doc3', 'ups_fb3', 'ups_fbd3', 'ups_doc3', 'ip_final', 'ups_final',
               'ups_meet', 'ups_meetd', 'ovpla_sign', 'ovpla_docfin', 'ovpla_docfind', 'percent'
            ]
        df = db.querydatafromdatabase(sql, values, col)

        title = df['Title'][0]
        type = df['Type'][0]
        desc = df['Description'][0]
        ipname = df['IP Name'][0]
        scmeet = df['scmeet'][0]
        scmeetd = df['scmeetd'][0]
        loi = df['loi'][0]
        aloi = df['aloi'][0]
        con = df['con'][0]
        ip_fb1 = df['ip_fb1'][0]
        ip_fbd1 = df['ip_fbd1'][0]
        ip_doc1 = df['ip_doc1'][0]
        ups_fb1 = df['ups_fb1'][0]
        ups_fbd1 = df['ups_fbd1'][0]
        ups_doc1 = df['ups_doc1'][0]
        ip_fb2 = df['ip_fb2'][0]
        ip_fbd2 = df['ip_fbd2'][0]
        ip_doc2 = df['ip_doc2'][0]
        ups_fb2 = df['ups_fb2'][0]
        ups_fbd2 = df['ups_fbd2'][0]
        ups_doc2 = df['ups_doc2'][0]
        ip_fb3 = df['ip_fb3'][0]
        ip_fbd3 = df['ip_fbd3'][0]
        ip_doc3 = df['ip_doc3'][0]
        ups_fb3 = df['ups_fb3'][0]
        ups_fbd3 = df['ups_fbd3'][0]
        ups_doc3 = df['ups_doc3'][0]
        ip_final = df['ip_final'][0]
        ups_final = df['ac_final'][0]
        ups_meet = df['ups_meet'][0]
        ups_meetd = df['ups_meetd'][0]
        ovpla_sign = df['ovpla_sign'][0]
        ovpla_docfin = df['ovpla_docfin'][0]
        ovpla_docfind = df['ovpla_docfind'][0]
        percent = df['percent'][0]

        return [title, type, desc, ipname, scmeet, scmeetd, 
                                 loi, aloi, con, ip_fb1, ip_fbd1, ip_doc1, ups_fb1, ups_fbd1, ups_doc1,
                                 ip_fb2, ip_fbd2, ip_doc2, ups_fb2, ups_fbd2, ups_doc2, 
                                 ip_fb3, ip_fbd3, ip_doc3, ups_fb3, ups_fbd3, ups_doc3, ip_final, ups_final, 
                                 ups_meet, ups_meetd, ovpla_sign, ovpla_docfin, ovpla_docfind, percent]
    else:
        raise PreventUpdate
