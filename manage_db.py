
# There are  types of reports:
# Taken - There are people in this room - 'taken'
# I'm taking it - Self-reporting of taking - 'usertake'
# Locked - I couldn't enter the room - 'locked'

import sqlite3

def create_flag_table():
    con = sqlite3.Connection("./reports.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE reports IF NOT EXISTS (id INTEGER PRIMARY KEY, flag TEXT, location TEXT, datetime TEXT);")
    cur.close()
    con.close()

def add_report(flag, locationName, dt):
    use = dt.replace(day=1, month=1, year=1900)

    con = sqlite3.Connection("./reports.db")
    cur = con.cursor()

    cur.execute("INSERT INTO reports VALUES ({f}, {l}, {d});".format(f=flag, l=locationName, d=use))

    cur.close()
    con.close()

def 

