import dash
import dash_bootstrap_components as dbc
from dash import html

from apps import dbconnect as db

def getItemDropdown(mode='add', inv_id=0, invet_id=None):
    sql = """SELECT it_id as value,
                    it_name as label
             FROM item
             WHERE TRUE
          """
    val = []

    if mode == 'add' and not inv_id:
        pass

    elif mode == 'add' and inv_id:
        sql += """ AND it_id NOT IN (
                        SELECT it_id 
                        FROM inventory_detail d
                        WHERE inv_id = %s
                            AND NOT inv_delete
                    )"""
        val += [inv_id]

    else:
        sql += """ AND it_id NOT IN (
                        SELECT it_id 
                        FROM inventory_detail d
                        WHERE inv_id = %s
                            AND d.invet_id <> %s
                            AND NOT d.inv_delete
                    )"""
        val += [inv_id, invet_id]

    df = db.querydatafromdatabase(sql, val, ['value', 'label'])

    return df.to_dict('records')

def converttoint(num):
    try:
        num = int(num)
        if num > 0:
            return num
        else:
            return 0
    except:
        return 0
    

def createTRrecord(docno, type, inventorydate, custname, status, remarks):
    sql = """INSERT INTO inventory(inv_docno, inv_type, inv_date, cust_id, inv_status, inv_remarks)
    VALUES (%s, %s, %s, %s, %s, %s) 
    RETURNING inv_id"""
    
    values = [docno, type, inventorydate, custname, status, remarks]
    
    inv_id = db.modifydatabasereturnid(sql, values)
    
    return inv_id

#------------------------------------------------------------------------------------------------------
def manageTRLineItem(inv_id, newline):
    itemin = newline.get('itemin', 0)
    itemout = newline.get('itemout', 0)
    itemso = newline.get('itemso', 0)
    itemjo = newline.get('itemjo', 0)

    sql = """INSERT INTO inventory_detail(inv_id, it_id, inv_in, inv_out, inv_so, inv_jo)
    VALUES (%(inv_id)s, %(itemid)s, %(itemin)s, %(itemout)s, %(itemso)s, %(itemjo)s) 
    ON CONFLICT (inv_id, it_id) DO 
    UPDATE 
        SET 
            inv_delete = false,
            inv_in = %(itemin)s,
            inv_out = %(itemout)s,
            inv_so = %(itemso)s,
            inv_jo = %(itemjo)s"""
    
    values = {
        'inv_id': inv_id,
        'itemid': newline['itemid'],
        'itemin': itemin,
        'itemout': itemout,
        'itemso': itemso,
        'itemjo': itemjo
    }
    
    db.modifydatabase(sql, values)

def removeLineItem(invet_id):
    sql = """UPDATE inventory_detail
    SET inv_delete = true
    WHERE invet_id = %s"""
    
    val = [invet_id]
    db.modifydatabase(sql, val)
    

def queryTRLineItems(inv_id):
    sql = """SELECT
        i.it_name,
        pi.inv_in,
        pi.inv_out,
        pi.inv_so,
        pi.inv_jo,
        pi.invet_id  
    FROM inventory_detail pi
        INNER JOIN item i ON i.it_id = pi.it_id
    WHERE 
        NOT pi.inv_delete AND
        pi.inv_id = %s
    """
    val = [inv_id]
    cols = ['Item', 'IN', 'OUT', 'SO', 'JO', 'id']

    return db.querydatafromdatabase(sql, val, cols)

def formatTRtable(df):
    df['IN'] = df['IN'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right') if num is not None else 0)
    df['OUT'] = df['OUT'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right') if num is not None else 0)
    df['SO'] = df['SO'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right') if num is not None else 0)
    df['JO'] = df['JO'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right') if num is not None else 0)

    buttons = []
    for id in df['id']:
        buttons += [
            html.Div(
                dbc.Button('Edit', id={'index': id, 'type': 'inventoryprof_editlinebtn'},
                            size='sm', color='warning'),
                style={'text-align': 'center'}
            )
        ]

    df['Action'] = buttons

    df.insert(
        loc=0,
        column='Item #',
        value=[html.Div(i + 1, className='text-center') for i in range(len(df.index))]
    )

    df.drop(['id'], axis=1, inplace=True)

    return dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                     hover=True, size='sm')
    
def getTRLineData(lineid):
    sql = """SELECT
        it_id,
        inv_in,
        inv_out,
        inv_so,
        inv_jo
    FROM inventory_detail pi
    WHERE 
        invet_id = %s
    """
    val = [lineid]
    cols = ['item', 'In', 'Out', 'So', 'Jo']
    
    df = db.querydatafromdatabase(sql, val, cols)
    
    return [df[i][0] for i in cols]

def checkTRLineItems(inv_id):
    sql = """SELECT COUNT(*)
    FROM inventory_detail
    WHERE NOT inv_delete
        AND inv_id = %s"""
    val = [inv_id]
    col = ['count']
    
    df = db.querydatafromdatabase(sql, val, col)
    
    return df['count'][0]

def deleteTR(inv_id):
    sql = """UPDATE inventory
    SET inv_delete = true
    WHERE inv_id = %s"""
    
    val = [inv_id]
    db.modifydatabase(sql, val)
