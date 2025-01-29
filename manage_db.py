
# There are  types of reports:
# Taken - There are people in this room - 'taken'
# I'm taking it - Self-reporting of taking - 'usertake'
# Locked - I couldn't enter the room - 'locked'

import sqlite3
import datetime

def create_flag_table():
    con = sqlite3.Connection("./reports.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS reports (flag TEXT, location TEXT, datetime TEXT);")
    con.commit()
    con.close()

def add_report(flag, locationName, dt):
    con = sqlite3.Connection("./reports.db")
    cur = con.cursor()

    cur.execute("INSERT INTO reports VALUES ('{f}', '{l}', '{d}');".format(f=flag, l=locationName, d=use))

    cur.close()
    con.commit()
    con.close()

def get_report(locationName):
    con = sqlite3.Connection("./reports.db")
    cur = con.cursor()
    
    cur.execute("SELECT * FROM reports WHERE location = '{l}'".format(l=locationName))

    out = cur.fetchall()
    con.commit()
    con.close()
    return out

def get_all_reports():
    con = sqlite3.Connection("./reports.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM reports")

    out = cur.fetchall()
    con.commit()
    con.close()

    return out

def dtrp_to_dt(dtrp):
    form = "%Y-%m-%d %H:%M:%S.%f"

    return datetime.datetime.strptime(dtrp, form)