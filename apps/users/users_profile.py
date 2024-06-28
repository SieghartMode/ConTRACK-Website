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
                dcc.Store(id='userprofile_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2('User Details', className='page-header'),
        html.Hr(),
        dbc.Alert(id='userprofile_alert', is_open=False),
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
                                                dbc.Label("First Name", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='userprofile_fname',
                                                        placeholder="First Name"
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Last Name", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='userprofile_lname',
                                                        placeholder='Last Name'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Email", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='userprofile_email',
                                                        placeholder='User Email'
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
                                                dbc.Label("Username", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='userprofile_cname',
                                                        placeholder='Username'
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Access Type", width=4),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id='userprofile_access',
                                                        placeholder='Select User Access Type',
                                                        options=[
                                                            {'label': 'Admin', 'value': 'Admin'},
                                                            {'label': 'Manager', 'value': 'Manager'},
                                                            {'label': 'Secretary', 'value': 'Secretary'},
                                                        ]
                                                    ),
                                                    width=6
                                                )
                                            ],
                                            className='mb-3'
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Password", width=4),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='userprofile_pwd',
                                                        placeholder='User Password'
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
                            id='userprofile_removerecord',
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
            id='userprofile_removerecord_div'
        ),
        dbc.Button(
            'Cancel',
            id='userprofile_cancel',
            className='cancel-btn',
            href='/users'
        ),
        dbc.Button(
            'Submit',
            id='userprofile_submit',
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
                    ], id='userprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/users/users_home',
                        id='userprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='userprofile_successmodal',
            backdrop='static'
        )
    ]
)

@app.callback(
    [
        Output('userprofile_toload', 'data'),
        Output('userprofile_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def userprof_loaddropdown(pathname, search):
    if pathname == '/users/users_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [to_load, removediv_style]

@app.callback(
    [
        Output('userprofile_alert', 'color'),
        Output('userprofile_alert', 'children'),
        Output('userprofile_alert', 'is_open'),
        Output('userprofile_successmodal', 'is_open'),
        Output('userprofile_feedback_message', 'children'),
        Output('userprofile_btn_modal', 'href'),
    ],
    [
        Input('userprofile_submit', 'n_clicks'),
        Input('userprofile_btn_modal', 'n_clicks'),
    ],
    [
        State('userprofile_fname', 'value'),
        State('userprofile_lname', 'value'),
        State('userprofile_email', 'value'),
        State('userprofile_cname', 'value'),
        State('userprofile_access', 'value'),
        State('userprofile_pwd', 'value'),
        State('url', 'search'),
        State('userprofile_removerecord', 'value'),
    ]
)
def userprofile_saveprofile(submitbtn, closebtn, fname, lname, email, cname, access, pwd, search, removerecord):
    ctx = dash.callback_context
    feedbackmessage = ""  # Initialize feedbackmessage
    okay_href = ""  # Initialize okay_href

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        print(eventid)
        if eventid == 'userprofile_submit' and submitbtn:

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            if not fname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the first name.'
            elif not lname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the last name.'
            elif not email:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the user status.'
            elif not cname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the user email.'
            elif not access:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the user access level.'
            elif not pwd:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the user password.'
            else:
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                print('here')
                if create_mode == 'add':
                    sql = '''
                        INSERT INTO users (user_fname, user_lname, user_email, user_cname, user_access, user_pwd)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    '''
                    encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()

                    values = [fname, lname, email, cname, access, encrypt_string(pwd)]
                    db.modifydatabase(sql, values)
                    feedbackmessage = "User has been saved."
                    okay_href = '/users'
                    modal_open = True
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    user_id = parse_qs(parsed.query)['id'][0]
                    print("ID of users: ", user_id)
                    sqlcode = """UPDATE users
                    SET
                        user_fname = %s,
                        user_lname = %s,
                        user_email = %s,
                        user_cname = %s,
                        user_access = %s,
                        user_pwd = %s,
                        user_delete = %s
                    WHERE
                        user_id = %s
                    """

                    encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()

                    to_delete = bool(removerecord)
                    values = [fname, lname, email, cname, access, encrypt_string(pwd), to_delete, user_id]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "User has been updated."
                    okay_href = '/users'
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
        Output('userprofile_fname', 'value'),
        Output('userprofile_lname', 'value'),
        Output('userprofile_email', 'value'),
        Output('userprofile_cname', 'value'),
        Output('userprofile_access', 'value'),
    ],
    [
        Input('userprofile_toload', 'modified_timestamp')
    ],
    [
        State('userprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def userprofile_loadprofile(timestamp, toload, search):
    print(f'toload: {toload}')
    if toload:
        parsed = urlparse(search)
        user_id = parse_qs(parsed.query)['id'][0]
        print("ID of users: ", user_id)
        sql = """
            SELECT user_fname, user_lname, user_email, user_cname, user_access
            FROM users
            WHERE user_id = %s
        """
        values = [user_id]
        col = ['fname', 'lname', 'email', 'cname', 'access']
        df = db.querydatafromdatabase(sql, values, col)

        fname = df['fname'][0]
        lname = df['lname'][0]
        email = df['email'][0]
        cname = df['cname'][0]
        access = df['access'][0]

        return [fname, lname, email, cname, access]
    else:
        raise PreventUpdate
