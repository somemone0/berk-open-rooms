from flask import Flask, request, Response
import room_funcs as rf
from datetime import datetime

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)