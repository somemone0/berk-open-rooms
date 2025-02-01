from flask import Flask, request, Response
import pandas as pd
import room_funcs as rf
import manage_db as mdb
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/buildings")
def get_buildings():
    
    return rf.get_buildings()

@app.route("/openrooms/<building_id>")
def open_buildings(building_id):
    if not building_id.isdigit():
        return Response(400)
    
    days_of_week = ["M", "Tu", "W", "Th", "F", "Sa", "Su"]
    
    #return rf.get_rooms_open_in_building(int(building_id), datetime.now(), days_of_week[datetime.now().weekday()]).to_json()
    return rf.get_rooms_open_in_building(int(building_id), datetime.now(), days_of_week[datetime.now().weekday()])


@app.route("/getalerts")
def get_alerts():
    
    alerts = mdb.get_all_reports()
    two_hours_ago = datetime.now() - timedelta(hours=2)

    valid = [i for i in alerts if mdb.dtrp_to_dt(i[2]) > two_hours_ago]

    return valid

@app.route("/addalert/<type>", methods=["POST"])
def add_alert(type):
    room = request.data.decode("utf-8")
    valid_types = ["taken", "usertake", "locked"]
    if type not in valid_types:
        return Response(400)

    mdb.add_report(type, room, datetime.now())

    return mdb.get_report(room)

@app.route("/getschedule/<room>")
def getschedule(room):
    dayofweek = request.args.get("dayofweek")

    all = pd.read_csv("all_data.csv") 
    q = all.query("@room == locationName")
    q2 = [dict(r[1])
           for r in q.iterrows() if dayofweek in r[1]["wordDays"]]
    print(q2)

    return q2

if __name__ == "__main__":
    mdb.create_flag_table()

    app.run(host="0.0.0.0", port=8080)