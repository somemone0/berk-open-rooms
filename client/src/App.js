import React, { useState, useEffect } from 'react';
import { 
  Container,
  Card,
  CardContent,
  Typography,
  Select,
  MenuItem,
  Button,
  Grid,
  Box,
  useMediaQuery
} from '@mui/material';
import { makeStyles } from '@mui/styles';
import { formatDistanceToNow } from 'date-fns';

const useStyles = makeStyles((theme) => ({
  fixedSelect: {
    position: 'fixed',
    top: 0,
    width: '100%',
    zIndex: 1000,
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(2)
  },
  content: {
    marginTop: 80,
    maxWidth: 600,
    marginLeft: 'auto',
    marginRight: 'auto'
  },
  card: {
    marginBottom: theme.spacing(2)
  }
}));

function App() {
  const classes = useStyles();
  const [buildings, setBuildings] = useState([]);
  const [currentBuildingID, setCurrentBuildingID] = useState(null);
  const [openRooms, setOpenRooms] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const isDesktop = useMediaQuery('(min-width:600px)');

  // Fetch buildings and determine closest
  useEffect(() => {
    const fetchBuildings = async () => {
      try {
        const response = await fetch(`/buildings`);
        const data = await response.json();
        setBuildings(data);

        navigator.geolocation.getCurrentPosition((position) => {
          const closest = data.reduce((prev, curr) => {
            const prevDist = distance(position.coords, prev);
            const currDist = distance(position.coords, curr);
            return currDist < prevDist ? curr : prev;
          }, data[0]);
          setCurrentBuildingID(closest.id);
        });
      } catch (error) {
        console.error('Error fetching buildings:', error);
      }
    };
    fetchBuildings();
  }, []);

  // Fetch open rooms and alerts when building changes
  useEffect(() => {
    const fetchData = async () => {
      if (!currentBuildingID) return;
      
      try {
        const [roomsRes, alertsRes] = await Promise.all([
          fetch(`/openrooms/${currentBuildingID}`),
          fetch(`/getalerts`)
        ]);
        
        const roomsData = await roomsRes.json();
        const alertsData = await alertsRes.json();
        
        setOpenRooms(roomsData);
        setAlerts(alertsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, [currentBuildingID]);

  const distance = (userCoords, building) => {
    console.log(building)
    const R = 6371e3;
    const φ1 = userCoords.latitude * Math.PI/180;
    const φ2 = building.lat * Math.PI/180;
    const Δφ = (building.lat - userCoords.latitude) * Math.PI/180;
    const Δλ = (building.long - userCoords.longitude) * Math.PI/180;

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ/2) * Math.sin(Δλ/2);
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  };

  const handleAlert = async (type, locationName) => {
    try {
      await fetch(`/addalert/${type}`, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: locationName
      });
      const alertsRes = await fetch(`/getalerts`);
      setAlerts(await alertsRes.json());
    } catch (error) {
      console.error('Error adding alert:', error);
    }
  };

  const getAlertText = (locationName) => {
    const roomAlerts = alerts.filter(alert => alert[1] === locationName);
    if (roomAlerts.length === 0) return null;
    
    const latest = roomAlerts.reduce((prev, curr) => 
      new Date(curr[2]) > new Date(prev[2]) ? curr : prev
    );
    console.log(new Date(latest[2]))
    console.log(new Date(Date.now()))
    
    const type = latest[0] === 'locked' ? 'Locked' : 'Taken';
    const time = formatDistanceToNow(new Date(latest[2]), { addSuffix: true });
    return `Reported ${type} ${time}`;
  };

  return (
    <div>
      <div className={classes.fixedSelect}>
        <Select
          fullWidth
          value={currentBuildingID || ''}
          onChange={(e) => setCurrentBuildingID(e.target.value)}
        >
          {buildings.map((b) => (
            <MenuItem key={b.id} value={b.id}>{b.name}</MenuItem>
          ))}
        </Select>
      </div>

      <Container className={classes.content} sx={isDesktop ? { mx: 'auto' } : {}}>
        {openRooms.map((room) => (
          <Card key={room.locationName} className={classes.card}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {room.locationName}
              </Typography>
              <Typography color="textSecondary">
                {room.next ? `Next class: ${new Date(room.next).toLocaleTimeString()}` : 'Free all day'}
              </Typography>

              <Grid container justifyContent="space-between" alignItems="center" mt={2}>
                <Grid item>
                  {getAlertText(room.locationName) && (
                    <Typography color="error">
                      {getAlertText(room.locationName)}
                    </Typography>
                  )}
                </Grid>
                <Grid item>
                  <Select
                    size="small"
                    value=""
                    onChange={(e) => handleAlert(e.target.value, room.locationName)}
                  >
                    <MenuItem value="" disabled>Report</MenuItem>
                    <MenuItem value="usertake">I'm taking this room</MenuItem>
                    <MenuItem value="taken">This room is taken</MenuItem>
                    <MenuItem value="locked">I can't get in</MenuItem>
                  </Select>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        ))}
      </Container>
    </div>
  );
}

export default App;