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
                dcc.Store(id='ipprofile_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2('User Details', className='page-header'),
        html.Hr(),
        dbc.Alert(id='ipprofile_alert', is_open=False),
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
                                                dbc.Label("IP Name", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='ipprofile_name',
                                                        placeholder="Enter IP Name"
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Industry", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='ipprofile_ind',
                                                        placeholder="Enter IP Industry"
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Contact Person", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='ipprofile_person',
                                                        placeholder="Enter Full Name"
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
                                                dbc.Label("IP Phone Number", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='ipprofile_phone',
                                                        placeholder="Enter Number"
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Email", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='ipprofile_email',
                                                        placeholder="Enter IP Email"
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("IP Remarks", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='ipprofile_remarks',
                                                        placeholder="Enter any remarks."
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
                            id='ipprofile_removerecord',
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
            id='ipprofile_removerecord_div'
        ),
        dbc.Button(
            'Cancel',
            id='ipprofile_cancel',
            className='cancel-btn',
            href='/ip'
        ),
        dbc.Button(
            'Submit',
            id='ipprofile_submit',
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
                    ], id='ipprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/ip/ip_home',
                        id='ipprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='ipprofile_successmodal',
            backdrop='static'
        )
    ]
)

@app.callback(
    [
        Output('ipprofile_toload', 'data'),
        Output('ipprofile_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def ipprof_loaddropdown(pathname, search):
    if pathname == '/ip/ip_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [to_load, removediv_style]

@app.callback(
    [
        Output('ipprofile_alert', 'color'),
        Output('ipprofile_alert', 'children'),
        Output('ipprofile_alert', 'is_open'),
        Output('ipprofile_successmodal', 'is_open'),
        Output('ipprofile_feedback_message', 'children'),
        Output('ipprofile_btn_modal', 'href'),
    ],
    [
        Input('ipprofile_submit', 'n_clicks'),
        Input('ipprofile_btn_modal', 'n_clicks'),
    ],
    [
        State('ipprofile_name', 'value'),
        State('ipprofile_ind', 'value'),
        State('ipprofile_person', 'value'),
        State('ipprofile_phone', 'value'),
        State('ipprofile_email', 'value'),
        State('ipprofile_remarks', 'value'),
        State('url', 'search'),
        State('ipprofile_removerecord', 'value'),
    ]
)
def ipprofile_saveprofile(submitbtn, closebtn, name, ind, person, phone, email, remarks, search, removerecord):
    ctx = dash.callback_context
    feedbackmessage = ""  # Initialize feedbackmessage
    okay_href = ""  # Initialize okay_href

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        print(eventid)
        if eventid == 'ipprofile_submit' and submitbtn:

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            if not name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please state the IP Name.'
            elif not ind:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please state the IP Industry.'
            elif not person:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please state the IP Contact Person.'
            elif not phone:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please state the IP Phone Number.'
            elif not email:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please state the IP email.'
            
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                print('here')
                if create_mode == 'add':
                    sql = '''
                        INSERT INTO indpartners (ip_name, ip_ind, ip_person, ip_phone, ip_email, ip_remarks)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    '''
                    values = [name, ind, person, phone, email, remarks]
                    db.modifydatabase(sql, values)
                    feedbackmessage = "IP has been saved."
                    okay_href = '/ip'
                    modal_open = True
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    ip_id = parse_qs(parsed.query)['id'][0]
                    print("ID of IP: ", ip_id)
                    sqlcode = """UPDATE indpartners
                    SET
                        ip_name = %s,
                        ip_ind = %s,
                        ip_person = %s,
                        ip_phone = %s,
                        ip_email = %s,
                        ip_remarks = %s,
                        ip_delete = %s
                    WHERE
                        ip_id = %s
                    """
                    to_delete = bool(removerecord)
                    values = [name, ind, person, phone, email, remarks, to_delete, ip_id]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "IP has been updated."
                    okay_href = '/ip'
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
        Output('ipprofile_name', 'value'),
        Output('ipprofile_ind', 'value'),
        Output('ipprofile_person', 'value'),
        Output('ipprofile_phone', 'value'),
        Output('ipprofile_email', 'value'),
        Output('ipprofile_remarks', 'value'),
    ],
    [
        Input('ipprofile_toload', 'modified_timestamp')
    ],
    [
        State('ipprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def ipprofile_loadprofile(timestamp, toload, search):
    print(f'toload: {toload}')
    if toload:
        parsed = urlparse(search)
        ip_id = parse_qs(parsed.query)['id'][0]
        print("ID of IP: ", ip_id)
        sql = """
            SELECT ip_name, ip_ind, ip_person, ip_phone, ip_email, ip_remarks
            FROM indpartners
            WHERE ip_id = %s
        """
        values = [ip_id]
        col = ['Name', 'Industry', 'Contact Person', 'Phone Number', 'Email', 'Remarks']
        df = db.querydatafromdatabase(sql, values, col)

        name = df['Name'][0]
        ind = df['Industry'][0]
        person = df['Contact Person'][0]
        phone = df['Phone Number'][0]
        email = df['Email'][0]
        remarks = df['Remarks'][0]

        return [name, ind, person, phone, email, remarks]
    else:
        raise PreventUpdate
