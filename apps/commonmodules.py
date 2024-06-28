# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app

navlink_style = {
    'color': '#091324',
    'font-weight': 'bold'
}

# external_stylesheets = [dbc.themes.BOOTSTRAP, '/assets/lgs.css']
external_stylesheets = ['lgs.css']



navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("ConTrack", className='ms-2', style={'color': '#7a34eb', 'font-family': 'Montserrat, sans-serif', 'font-weight': 'bold'})),
                ],
                align="center", style={'margin-left': '10px'},
                className='g-0'  
            ),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Contracts", href="/contracts", style=navlink_style),
        dbc.NavLink("IPs", href="/ip", style=navlink_style),
        dbc.NavLink("2Compare", href="/draftable", style=navlink_style),
        dbc.NavLink("Users", href="/users", style=navlink_style),
      
        ###### USERNAME AT NAVBAR #############
    html.Div(
        [
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.Img(src=app.get_asset_url("user_icon.png"), 
                                style={'width': '30px', 
                                        'height': '30px', 
                                        'margin-bottom': '5px'}
                        ),
                        dbc.NavLink(id="user-name-display", 
                                    style={'display': 'inline-block', 
                                        'margin-right': '10px',
                                        'margin-left': '-10px', 'color': '#091324'
                                        },
                        ),
                    ],
                    id='username-navlink',
                    className='username-navlink',
                ),
            ),

            dbc.Button("Logout", href="/logout", color="primary",
                    style={'background-color': 'red',
                            'color': '#FFFFFF',
                            'margin-left': 'auto',
                            'margin-right': '20px',
                            'margin-top':'7px',
                            'height': '40px'
                            },
                    className='logout'
                    ),

        ],
        style={'margin-left': 'auto',
               'display':'flex'
               }  
    ),

    ],
    style={'background-color': 'rgba(255, 255, 255, 0.90)'}

)
def generate_navlinks(user_role):
    common_navlinks = [
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Contracts", href="/contracts", style=navlink_style),
        dbc.NavLink("IPs", href="/ip", style=navlink_style),
        dbc.NavLink("2Compare", href="/draftable", style=navlink_style),
        dbc.NavLink("Users", href="/users", style=navlink_style),
    ]

    admin_navlinks = [
        dbc.NavItem(
            dbc.DropdownMenu(
                [
                    dbc.NavLink("Item Stock Tracker", id="item-stock-tracker", n_clicks_timestamp=0, href="/inventory_tracker", style=navlink_style),
                    dbc.NavLink("Sales Tracker", id="sales-tracker", n_clicks_timestamp=0, href="/sales_tracker", style=navlink_style),
                    dbc.NavLink("Tracker 3", id="tracker-3", n_clicks_timestamp=0, href="/reports", style=navlink_style),
                ],
                label="Reports",
                nav=True,
                in_navbar=True,
                color="primary",
                style={'color': 'white', 'font-weight': 'bold'},
            ),
        ),
    ]

    if user_role == "Admin":
        return common_navlinks + admin_navlinks
    else:
        return common_navlinks

@app.callback(
    Output('navbar', 'children'),
    [Input('currentrole', 'data')]
)
def update_navbar(user_role):
    return generate_navlinks(user_role)
@app.callback(
    Output("user-access-div", "children"),
    [
        Input('currentrole', 'data'),
    ]
)
def update_user_access_display(user_access):
    return f"User Access: {user_access}"

@app.callback(
    Output("user-name-display", "children"),
    [
        Input('currentuserfname', 'data'),
    ]
)
def update_user_name_display(user_name):
    return user_name
