# Dash related dependencies
# To open browser upon running your app
import webbrowser

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Importing your app definition from app.py so we can use it
from app import app
from apps import commonmodules as cm
from apps import home, login, signup
from apps.contracts import contracts_home, contracts_profile
from apps.users import users_home,users_profile
from apps.ip import ip_home, ip_profile
from apps.draftable import draftable_home, draftable_profile
from apps import commonmodules
CONTENT_STYLE = {
    "margin-top": "1em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),
        
        
        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        dcc.Store(id='currentuserfname', data=-1, storage_type='session'),
        dcc.Store(id='currentuserlname', data=-1, storage_type='session'),
        dcc.Store(id='currentuseremail', data=-1, storage_type='session'),
        dcc.Store(id='currentusercname', data=-1, storage_type='session'),

        # Adding the navbar
        html.Div(
            cm.navbar,
            id='navbar_div'
        ),

        # Page Content -- Div that contains page layout
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)


@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('navbar_div', 'className'),
    ],
    [
        # If the path (i.e. part after the website name; 
        # in url = youtube.com/watch, path = '/watch') changes, 
        # the callback is triggered
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('currentrole', 'data'),
    ]
)
def displaypage (pathname, sessionlogout, userid, userrole):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if userid < 0: # if logged out
                if pathname == '/':
                    returnlayout = login.layout
                elif pathname == '/signup':
                    returnlayout = signup.layout
                else:
                    returnlayout = '404: request not found'
            
            else:    
                if pathname == '/logout':
                    returnlayout = login.layout
                    sessionlogout = True
                    
                elif pathname == '/' or pathname == '/home':
                    # From the imported module 'home', we get the layout variable
                    returnlayout = home.layout
                
                elif pathname == '/contracts':
                    returnlayout = contracts_home.layout
                elif pathname == '/contracts/contracts_profile':
                    returnlayout = contracts_profile.layout

                elif pathname == '/users':
                        returnlayout = users_home.layout
                elif pathname == '/users/users_profile':
                        returnlayout = users_profile.layout
                   
                elif pathname == '/ip':
                    returnlayout = ip_home.layout
                elif pathname == '/ip/ip_profile':
                    returnlayout = ip_profile.layout
                
                elif pathname == '/draftable':
                    returnlayout = draftable_home.layout
                elif pathname == '/draftable/draftable_profile':
                    returnlayout = draftable_profile.layout

                else:
                    returnlayout = '404: request not found'
                    
                
            # decide sessionlogout value
            logout_conditions = [
                pathname in ['/', '/logout'],
                userid == -1,
                not userid
            ]
            sessionlogout = any(logout_conditions)
            
            # hide navbar if logged-out; else, set class/style to default
            navbar_classname = 'd-none' if sessionlogout else ''
        
        else:
            raise PreventUpdate
	
        return [returnlayout, sessionlogout, navbar_classname]
    else:
        raise PreventUpdate


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', autoraise=False)
    app.run_server(debug=False)
