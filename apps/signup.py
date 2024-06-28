import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Enter the details'),
        html.Hr(),
        dbc.Alert('Please supply details.', color="danger", id='signup_alert',
                  is_open=False),
        dbc.Row(
            [
                dbc.Label("First Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_user_fname", placeholder="Enter your First Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Last Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_user_lname", placeholder="Enter your Last Name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Email", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_user_email", placeholder="Enter your email"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Username", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_user_cname", placeholder="Enter a username"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("User Access", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_user_access", placeholder="Enter the user's access level"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_user_pwd", placeholder="Enter a password"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label(" Confirm Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_passwordconf", placeholder="Re-type the password"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Button('Sign up', color="secondary", id='singup_signupbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("User Saved")),
                dbc.ModalBody("User has been saved", id='signup_confirmation'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", href='/'
                    )
                ),
            ],
            id="signup_modal",
            is_open=False,
        ),
    ]
)

@app.callback(
    [
        Output('singup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
    
    enablebtn = password and passwordconf and password == passwordconf

    return [not enablebtn]

# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open')   
    ],
    [
        Input('singup_signupbtn', 'n_clicks')
    ],
    [
        State('signup_user_fname','value'),
        State('signup_user_lname','value'),
        State('signup_user_email','value'),
        State('signup_user_cname','value'),
        State('signup_user_pwd','value'),
        State('signup_user_access','value')
    ]
)
def saveuser(loginbtn, fname, lname, email, cname, pwd, access):
    openalert = openmodal = False
    if loginbtn:
        if fname and lname and email and cname and pwd and access:
            sql = """INSERT INTO users (user_fname, user_lname, user_email, user_cname, user_pwd, user_access)
            VALUES (%s, %s, %s, %s, %s, %s)"""  
            
            
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
            
            values = [fname, lname, email, cname, encrypt_string(pwd), access]
            db.modifydatabase(sql, values)
            
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]
