import pandas as pd
import requests

def update_sections():
    response = requests.post("https://berkeleytime.com/api/graphql", json={
    "operationName": "GetCoursesForFilter",
    "variables": {
        "playlists": "UGxheWxpc3RUeXBlOjMyNTU3"
    },
    "query": "query GetCoursesForFilter($playlists: String!) {\n  allCourses(inPlaylists: $playlists) {\n    edges {\n      node {\n        ...CourseOverview\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CourseOverview on CourseType {\n  id\n  abbreviation\n  courseNumber\n  description\n  title\n  gradeAverage\n  letterAverage\n  openSeats\n  enrolledPercentage\n  enrolled\n  enrolledMax\n  units\n  __typename\n}\n"
    })

    print(response.status_code)
    class_data = response.json()

    classes = [a["node"] for a in class_data["data"]["allCourses"]["edges"]]

    df = pd.DataFrame(classes)

    df.to_csv("classes.csv")

    sections = []

    line = 1
    for cse in classes:
        query = {
            "operationName": "GetCourseForName",
            "variables": {
                "abbreviation": cse["abbreviation"],
                "courseNumber": cse["courseNumber"],
                "semester": "spring",
                "year": "2025"
            },
            "query": "query GetCourseForName($abbreviation: String!, $courseNumber: String!, $year: String, $semester: String) {\n  allCourses(abbreviation: $abbreviation, courseNumber: $courseNumber, first: 1) {\n    edges {\n      node {\n        ...Course\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Course on CourseType {\n  title\n  units\n  waitlisted\n  openSeats\n  letterAverage\n  gradeAverage\n  lastUpdated\n  id\n  hasEnrollment\n  gradeAverage\n  enrolledPercentage\n  enrolledMax\n  courseNumber\n  department\n  description\n  enrolled\n  abbreviation\n  prerequisites\n  playlistSet {\n    edges {\n      node {\n        category\n        id\n        name\n        semester\n        year\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  sectionSet(year: $year, semester: $semester) {\n    edges {\n      node {\n        ...Section\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Section on SectionType {\n  id\n  ccn\n  kind\n  instructor\n  startTime\n  endTime\n  enrolled\n  enrolledMax\n  locationName\n  waitlisted\n  waitlistedMax\n  days\n  wordDays\n  disabled\n  sectionNumber\n  isPrimary\n  __typename\n}\n"
            }
        
        response = requests.post("https://berkeleytime.com/api/graphql", json=query).json()
        for i in response["data"]["allCourses"]["edges"][0]["node"]["sectionSet"]["edges"]:
            node = i["node"]
            node["abbreviation"] = cse["abbreviation"]
            node["courseNumber"] = cse["courseNumber"]

            sections.append(node)

        if line % 100 == 0:
            print(line)

    sections_df = pd.DataFrame(sections)
    room_names = sections_df["locationName"]

    room_locations = [" ".join(str(s).split(" ")[:-1]).strip() for s in list(room_names)]

    sections_df["building"] = room_locations

    sections_df.to_csv("sections.csv", index=False)

    matches = pd.read_csv("matches.csv")
    locations = pd.read_csv("locations.csv")

    sm = sections_df.merge(matches, how="left", left_on="building", right_on="secs")
    sml = sm.merge(locations, how="left", left_on="latlong", right_on="name")

    sml.drop("building", inplace=True)
    sml.drop("name", inplace=True)
    
    sml.to_csv("all_data.csv", index=False)

    
