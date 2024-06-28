import dash
import dash_bootstrap_components as dbc
from dash import html

from apps import dbconnect as db

def getItemDropdown(mode='add', tr_id=0, trdt_id=None):
    sql = """SELECT it_id as value,
                    it_name as label
             FROM item
             WHERE TRUE
          """
    val = []

    if mode == 'add' and not tr_id:
        pass

    elif mode == 'add' and tr_id:
       
        sql += """ AND it_id NOT IN (
                        SELECT it_id 
                        FROM transaction_detail d
                        WHERE tr_id = %s
                            AND NOT tr_delete
                    )"""
        val += [tr_id]

    else:
        
        sql += """ AND it_id NOT IN (
                        SELECT it_id 
                        FROM transaction_detail d
                        WHERE tr_id = %s
                            AND d.trdt_id <> %s
                            AND NOT d.tr_delete
                    )"""
        val += [tr_id, trdt_id]

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
    

def createTRrecord(docno, transactiondate, custname, status, total, remarks):
    sql = """INSERT INTO transaction(tr_docno, tr_date, cust_id, tr_status, tr_total, tr_remarks)
    VALUES (%s, %s, %s, %s, %s, %s) 
    RETURNING tr_id"""
    
    values = [docno, transactiondate, custname, status, total, remarks]
    
    tr_id = db.modifydatabasereturnid(sql, values)
    
    return tr_id

#------------------------------------------------------------------------------------------------------
def manageTRLineItem(tr_id, newline):
    qty = newline.get('itemqty', 0)
    prc = newline.get('itemprc', 0)

    tr_total = qty * prc

    sql = """INSERT INTO transaction_detail(tr_id, it_id, tr_prc, tr_qty, tr_total)
    VALUES (%(tr_id)s, %(itemid)s, %(prc)s, %(qty)s, %(tr_total)s) 
    ON CONFLICT (tr_id, it_id) DO 
    UPDATE 
        SET 
            tr_delete = false,
            tr_qty = %(qty)s,
            tr_prc = %(prc)s,
            tr_total = %(tr_total)s"""
    
    values = {
        'tr_id': tr_id,
        'itemid': newline['itemid'],
        'qty': qty,
        'prc': prc,
        'tr_total': tr_total
    }
    
    db.modifydatabase(sql, values)

def removeLineItem(trdt_id):
    sql = """UPDATE transaction_detail
    SET tr_delete = true
    WHERE trdt_id = %s"""
    
    val = [trdt_id]
    db.modifydatabase(sql, val)
    

def queryTRLineItems(tr_id):
    sql = """SELECT
        i.it_name,
        pi.tr_qty,
        pi.tr_prc,
        pi.tr_total,
        pi.trdt_id  
    FROM transaction_detail pi
        INNER JOIN item i ON i.it_id = pi.it_id
    WHERE 
        NOT pi.tr_delete AND
        pi.tr_id = %s
    """
    val = [tr_id]
    cols = ['Item', 'Qty', 'tr_price', 'tr_total', 'id']

    return db.querydatafromdatabase(sql, val, cols)

def formatTRtable(df):
    df['Qty'] = df['Qty'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right'))
    df['Price'] = df['tr_price'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right'))
    df['Total'] = df['tr_total'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right'))

    buttons = []
    for id in df['id']:
        buttons += [
            html.Div(
                dbc.Button('Edit', id={'index': id, 'type': 'transactionsprof_editlinebtn'},
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

    df.rename(columns={'tr_qty': 'Qty'}, inplace=True)

    return dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                     hover=True, size='sm')
    
def getTRLineData(lineid):
    sql = """SELECT
        it_id,
        tr_qty,
        tr_prc
    FROM transaction_detail pi
    WHERE 
        trdt_id = %s
    """
    val = [lineid]
    cols = ['item', 'qty', 'prc']
    
    df = db.querydatafromdatabase(sql, val, cols)
    
    return [df[i][0] for i in cols]

def checkTRLineItems(tr_id):
    sql = """SELECT COUNT(*)
    FROM transaction_detail
    WHERE NOT tr_delete
        AND tr_id = %s"""
    val = [tr_id]
    col = ['count']
    
    df = db.querydatafromdatabase(sql, val, col)
    
    return df['count'][0]

def deleteTR(tr_id):
    sql = """UPDATE transaction
    SET tr_delete = true
    WHERE tr_id = %s"""
    
    val = [tr_id]
    db.modifydatabase(sql, val)
