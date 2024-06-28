import pandas as pd
import psycopg2


def getdblocation():
    db = psycopg2.connect(
        host='localhost',
        database='contrack_db',
        user='postgres',
        port=5432,
        password='0Macaroni'
    )

    return db


def modifydatabase(sql, values):
    db = getdblocation()
    cursor = db.cursor()
    print("Values before execute:", values)

    cursor.execute(sql, values)
    db.commit()
    db.close()


def querydatafromdatabase(sql, values, dfcolumns):
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows


def modifydatabasereturnid(sqlcommand, values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    key = cursor.fetchone()[0]
    db.commit()
    db.close()
    return key