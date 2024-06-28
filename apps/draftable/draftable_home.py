import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db

from dash.dependencies import Input, Output, State
from apps import dbconnect as db

#import draftable
#from draftable.api import Client

# Initialize the Draftable API client
#client = draftable.Client('wnFIzC-test','fef2606097b1d3569ea22ed83d4324c4')

external_stylesheets = ['/assets/otherpages.css']


layout = html.Div(
    [
        html.H1("Document Comparison Tool"),
    html.Div(
        [
            dcc.Upload(
                id='upload-doc1',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Document 1')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'font-size': '0.75rem',
                    'backgroundColor': 'rgba(255, 255, 255, 0.8)'  # White background with 80% opacity
                }
            ),
            dcc.Upload(
                id='upload-doc2',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Document 2')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'font-size': '0.75rem',
                    'backgroundColor': 'rgba(255, 255, 255, 0.8)'  # White background with 80% opacity
                }
            )
        ],
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center'
        }
    ),
    html.Button("Compare Documents", id="compare-button", style={'backgroundColor': 'blue', 'color': 'white'}),
    html.Div(id='comparison-result')
    ]
),

@app.callback(
    [
        Output('supplierhome_supplierlist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('supplierhome_namefilter', 'value'),
        State('currentrole', 'data'),  
    ]
)
def supplierhome_loadsupplierlist(pathname, searchterm, current_role):
    print("Callback triggered with pathname:", pathname)
    print("Search term:", searchterm)
    if pathname == '/suppliers':
       
        sql = """ SELECT sup_id, sup_name, sup_addr, sup_status, sup_terms, sup_con, sup_remarks
            FROM supplier s
            WHERE
                NOT sup_delete 
        """
        values = []
        cols = ["ID", "Name", "Address", "Status", "Terms", "Contact", "Remarks"]
        if searchterm:
            sql += """ AND (
                        LOWER(sup_name) ILIKE LOWER(%s) OR
                        LOWER(sup_addr) ILIKE LOWER(%s) OR
                        LOWER(sup_status) ILIKE LOWER(%s) OR
                        LOWER(sup_terms) ILIKE LOWER(%s) OR
                        LOWER(sup_con) ILIKE LOWER(%s) OR
                        LOWER(sup_remarks) ILIKE LOWER(%s)
                    )"""
                        
            values += ['%' + searchterm + '%'] * 6
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: 
            
            buttons = []
            for sup_id in df['ID']:
                disabled = True if current_role == 'Secretary' else False
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                                    href=f'/suppliers/suppliers_profile?mode=edit&id={sup_id}',
                                    size='sm', color='warning', disabled=disabled), 
                        style={'text-align': 'center'}
                    )
                ]
      
            df['Action'] = buttons
        
            df = df[["Name", "Address", "Status", "Terms", "Contact", "Remarks", "Action"]]
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate
    
import base64
import os

@app.callback(
    Output('comparison-result', 'children'),
    Input('compare-button', 'n_clicks'),
    State('upload-doc1', 'contents'),
    State('upload-doc2', 'contents'),
    State('upload-doc1', 'filename'),
    State('upload-doc2', 'filename')
)
def compare_documents(n_clicks, doc1_contents, doc2_contents, doc1_filename, doc2_filename):
    if n_clicks is None:
        raise PreventUpdate
    
    if doc1_contents is None or doc2_contents is None:
        return "Please upload both documents."

    def save_file(contents, filename):
        data = contents.encode("utf8").split(b";base64,")[1]
        with open(filename, "wb") as fp:
            fp.write(base64.decodebytes(data))
        return filename

    doc1_path = save_file(doc1_contents, doc1_filename)
    doc2_path = save_file(doc2_contents, doc2_filename)
    
    try:
        # Create a new comparison
        comparison = client.create_comparison(doc1_path, doc2_path)
        comparison_id = comparison['data']['comparison']['identifier']

        # Retrieve the comparison result URL
        comparison_result_url = f"https://compare.draftable.com/comparison/{comparison_id}"
        
        return html.A('View Comparison Result', href=comparison_result_url, target="_blank")
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        # Clean up the uploaded files
        os.remove(doc1_path)
        os.remove(doc2_path)

