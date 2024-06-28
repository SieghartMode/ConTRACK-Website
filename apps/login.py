import hashlib
import dash_bootstrap_components as dbc
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

external_stylesheets = [dbc.themes.BOOTSTRAP, '/assets/lgs.css']

layout = html.Div(
    [
    html.Img(src=app.get_asset_url('logo2.png'), style={'width': '60%'}),
    html.Hr(className='linespace'),

    html.H2('User Login', className='login-title'),
    dbc.Alert('Username or Password is incorrect.', color="danger", id='login_alert', is_open=False),

    #dbc.Row([
        #dbc.Col(html.Img(src=app.get_asset_url('user_icon.png'), className="pass-icon")),
        #dbc.Col(dbc.Input(type="text", id="login_username", placeholder="Enter username", className="input-boxes"))
    #], className="mb-3"),

    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('user_icon.png'), className="common-box user-icon"), width="auto"),
        dbc.Col(dbc.Input(type="text", id="login_username", placeholder="Enter username", className="common-box input-boxes")),
    ], className="mb-3", style={'margin-left': '15px'}),  # Added margin-left

    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('pass_icon.png'), className="common-box pass-icon"), width="auto"),
        dbc.Col(dbc.Input(type="password", id="login_password", placeholder="Enter password", className="common-box input-boxes")),
    ], className="mb-3", style={'margin-left': '15px'}),  # Added margin-left


    dbc.Button('Login', color="primary", id='login_loginbtn', className='login-btn'),
],

    className='login-container login-page-bg'  
)


@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
        Output('currentuserfname', 'data'),
        Output('currentusercname', 'data'),
        Output('currentuseremail', 'data'),
        Output('currentuserlname', 'data'),
        Output('currentrole', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks'),
        Input('sessionlogout', 'modified_timestamp'),
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),   
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'), 
        State('url', 'pathname'), 
    ]
)
def loginprocess(loginbtn, sessionlogout_time,
                 
                 username, password,
                 sessionlogout, currentuserid,
                 pathname):
    
    openalert = False
    currentuserfname = None
    currentusercname = None
    currentuseremail = None
    currentuserlname = None
    currentrole = None
    
    ctx = callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    if eventid == 'login_loginbtn':
    
        if loginbtn and username and password:
            sql = """SELECT user_id, user_fname, user_cname, user_email, user_lname, user_access
            FROM users
            WHERE 
                user_cname = %s AND
                user_pwd = %s AND
                NOT user_delete"""
            
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
            
            #values = [username, password]
            values = [username, encrypt_string(password)]
            cols = ['userid', 'user_fname', 'user_cname', 'user_email', 'user_lname', 'user_access']
            df = db.querydatafromdatabase(sql, values, cols)
            
            if df.shape[0]:
                currentuserid = df['userid'][0]
                currentuserfname = df['user_fname'][0]
                currentusercname = df['user_cname'][0]
                currentuseremail = df['user_email'][0]
                currentuserlname = df['user_lname'][0]
                currentrole = df['user_access'][0]
            else:
                currentuserid = -1
                openalert = True
    elif eventid == 'sessionlogout' and pathname == '/logout':
        currentuserid = -1
    else:
        raise PreventUpdate
    
    return [openalert, currentuserid, currentuserfname, currentusercname, currentuseremail, currentuserlname, currentrole]


@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'), 
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]