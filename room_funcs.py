import pandas as pd
import datetime

def get_buildings():
    matches = pd.read_csv("matches.csv")
    
    return list(matches["latlong"].unique())

def get_rooms_open_in_building(latlongname, dt, dayofweek):
    use = dt.replace(day=1, month=1, year=1900)

    sections = pd.read_csv("all_data.csv", parse_dates=["startTime", "endTime"])
    
    all_classes_in_building = sections.query("@latlongname == latlong")
    invalid_rooms = all_classes_in_building.query("endTime > @use and startTime < @use and @dayofweek in wordDays")[["locationName"]].drop_duplicates()
    next_class = all_classes_in_building.query("startTime > @use and @dayofweek in wordDays")
    all_rooms = all_classes_in_building[["locationName"]].drop_duplicates()
    print("INVALID ROOMS: ", len(invalid_rooms), len(all_rooms))
    next_class_by_room = next_class[["locationName", "startTime"]].groupby(by="locationName").agg(min)

    valid = pd.concat([all_rooms, invalid_rooms]).drop_duplicates(keep=False)
    print(valid.keys())

    return valid.merge(next_class_by_room, how="left", on="locationName").sort_values(by="locationName")

def get_building_locations():
    return pd.read_csv("locations.csv")


if __name__ == "__main__":
    res = get_rooms_open_in_building("Dwinelle Hall", datetime.datetime(1900, 1, 1, 16, 30), "W")
    res.to_csv("tmp.csv", index=False)
    print(res)
    print(len(res))