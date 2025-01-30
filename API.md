## API Reference

### GET /buildings
Inputs: No inputs

Returns a list of buildings, each represented as dictionaries with the following values:
 - name: Name of building
 - id: ID of building
 - lat: Latitude of bilding
 - long: Longitude of building

### GET /openrooms/<building_id>
Inputs:
 - building_id: ID of building

Returns a list of open rooms, each represented as dictionaries with the following values:
 - locationName: Room name
 - next: Datetime of next class, or null if no class.

### GET /getalerts
Inputs: No inputs

Returns a list of alerts, each represented by a list. 
 - *Index 0* -- *flag*. Represents the type of alert. The possible flags are:
 - - "taken": The user finds that the rooms is already taken
 - - "usertake": The user takes the room themselves
 - - "locked": The user cannot enter the room
 - *Index 1* -- *location*. Represents the room that this alert takes place in
 - *Index 2* -- *datetime*. Datetime object representing time alert has taken

### POST /addalert/<type>
Inputs: 
 - type: One of the three flags:
  - - "taken": The user finds that the rooms is already taken
 - - "usertake": The user takes the room themselves
 - - "locked": The user cannot enter the room
 - Body: room name, in plain text

Outputs:
 - That rooms current alerts

### GET /getschedule/<room>
Inputs:
 - room: Room name
 - dayofweek: Query parameter of either {M, Tu, W, Th, F, Sa, Su}

Returns a list of classes that room has on that day of the week

