import pandas as pd
import datetime

def get_buildings():
    matches = pd.read_csv("matches.csv")
    locations = pd.read_csv("locations.csv")
    
    ml = matches[["latlong", "secs"]].merge(locations, how="left", left_on="latlong", right_on="name")
    ml.drop(["latlong", "secs"], axis=1, inplace=True)

    return ml.to_json(orient="records")
    # return [{"id": r[1]["id"], "latlong": r[1]["latlong"]} for r in matches[["latlong", "id"]].iterrows()]

def get_rooms_open_in_building(latlongid, dt, dayofweek):
    use = dt.replace(day=1, month=1, year=1900)

    sections = pd.read_csv("all_data.csv", parse_dates=["startTime", "endTime"])
    
    all_classes_in_building = sections.query("@latlongid == building_id")

    valid = []
    gb = all_classes_in_building.groupby(by="locationName")
    for name, classes in gb:
        if any([r[1]["endTime"] > use and r[1]["startTime"] < use and dayofweek in r[1]["wordDays"] for r in classes.iterrows()]):
            continue
        valid.append({"locationName": name})

        next_class = [r[1]["startTime"] for r in classes.iterrows() if r[1]["startTime"] > use]
        if len(next_class) > 0:
            valid[-1]["next"] = min(next_class)
        else:
            valid[-1]["next"] = None
        

    #invalid_rooms = all_classes_in_building.query("endTime > @use and startTime < @use and @dayofweek in wordDays", engine="python")[["locationName"]].drop_duplicates()
    #next_class = all_classes_in_building.query("startTime > @use and @dayofweek in wordDays")
    #all_rooms = all_classes_in_building[["locationName"]].drop_duplicates()
    #print("INVALID ROOMS: ", len(invalid_rooms), len(all_rooms))
    #next_class_by_room = next_class[["locationName", "startTime"]].groupby(by="locationName").agg(min)

    #valid = pd.concat([all_rooms, invalid_rooms]).drop_duplicates(keep=False)
    #print(valid.keys())

    #return valid.merge(next_class_by_room, how="left", on="locationName").sort_values(by="locationName")
    return valid

def get_building_locations():
    return pd.read_csv("locations.csv")


if __name__ == "__main__":
    res = get_rooms_open_in_building("Dwinelle Hall", datetime.datetime(1900, 1, 1, 16, 30), "W")
    res.to_csv("tmp.csv", index=False)
    print(res)
    print(len(res))